import streamlit as st
import os
import shutil
import warnings
import requests
import re
from datetime import datetime
from dotenv import load_dotenv

# Suppress deprecation warnings
# warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

from src.transcriber import Transcriber
from src.generator import MinutesGenerator
from src.styles import get_custom_css
from src.pdf_utils import convert_markdown_to_pdf
from src.ui_components import (
    render_header, 
    render_meta_tags, 
    render_executive_insights, 
    render_discussion_matrix, 
    render_action_matrix
)

# Load env vars
load_dotenv()  # function that loads .env file to the program
 
st.set_page_config(page_title="Orbital Summary", page_icon="⚡", layout="wide")

# Inject Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)#markdown is a function  to render html content 

# No database initialization

# --- Helper Function for Download ---
def download_file(url):
    local_filename = url.split('/')[-1]
    if '?' in local_filename: local_filename = local_filename.split('?')[0]
    if not local_filename: local_filename = "downloaded_audio.mp3"
    
    with st.spinner(f"Downloading audio from {url}..."):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk) #chunk =  read a small part and write to the file , continues it untill the audio file completes
        except Exception as e:
            st.error(f"Error downloading file: {e}")
            return None

def parse_markdown_to_data(markdown_text):
    """
    Simple heuristic parser to extract meaningful sections from the generated markdown.
    Returns a dict with 'summary', 'discussions', 'actions'.
    """
    data = {"summary": "", "discussions": [], "actions": []}
    
    # 0. Extract Title from Metadata Table (Field | Detail)
    # Look for row starting with "| **1. Meeting Title**"
    title_match = re.search(r"\|\s*\*\*1\. Meeting Title\*\*\s*\|\s*(.*?)\s*\|", markdown_text)
    if title_match:
        # We store title in a separate key if needed, or pass it out. 
        # For now, let's keep the dict structure simple, but we can access it via app logic logic
        pass 

    # 1. Extract Summary (Look for "Meeting Summary" header)
    summary_match = re.search(r"###\s*4\.\s*Meeting Summary.*?\n(.*?)(?=\n###|\Z)", markdown_text, re.DOTALL | re.IGNORECASE)
    if summary_match:
        data["summary"] = summary_match.group(1).strip()
    else:
        # Fallback to old regex if ### 4. format misses
        summary_fallback = re.search(r"(?:##|\d+\.|[*]+)\s*Meeting Summary.*?\n(.*?)(?=\n(?:##|\d+\.|[*]+)|\Z)", markdown_text, re.DOTALL | re.IGNORECASE)
        if summary_fallback:
             data["summary"] = summary_fallback.group(1).strip()
        else:
            data["summary"] = markdown_text[:500] + "..."

    # 2. Extract Discussion Points
    discussion_match = re.search(r"###\s*5\.\s*Key Discussion.*?\n(.*?)(?=\n###|\Z)", markdown_text, re.DOTALL | re.IGNORECASE)
    if discussion_match:
        bullet_points = re.findall(r"[-*]\s+(.*)", discussion_match.group(1))
        data["discussions"] = bullet_points[:5] 
    
    # 3. Extract Action Items from TABLE
    # Look for table rows: | Task | Owner | Deadline |
    actions_block = re.search(r"###\s*7\.\s*Action Items.*?\n(.*?)(?=\n###|\Z)", markdown_text, re.DOTALL | re.IGNORECASE)
    if actions_block:
        block_text = actions_block.group(1)
        # Regex for table row: | col1 | col2 | col3 |
        # We skip the header row and separator line
        rows = re.findall(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", block_text)
        
        for r in rows:
            task = r[0].strip()
            owner = r[1].strip()
            due = r[2].strip()
            
            # Skip header or separator rows if regex caught them (usually separators have ---)
            if "---" in task or "Task" in task:
                continue
                
            data["actions"].append({"task": task, "owner": owner, "due_date": due})
            
    # If parsing failed to find anything specific, populate with empty lists
    if not data["discussions"]:
         data["discussions"] = [] 
    if not data["actions"]:
         data["actions"] = []
         
    return data

# No Sidebar History Logic

if st.sidebar.button("New Meeting", type="primary"):
    # Clear session state to go back to upload
    for key in ['minutes', 'transcript', 'processed_data', 'current_title']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# --- Sidebar Settings ---
# No "Advanced" expander needed for API key anymore.
# Just let user confirm model name.
# Removed user_api_key input

# --- Main App Logic ---

# Render Header
render_header()

if 'minutes' not in st.session_state:
    # --- State 1: Input / Upload ---
    st.markdown("## 🎙️ New Session Analysis")
    st.markdown("Upload audio or provide a URL to generate your Orbital Summary.")
    
    col1, col2 = st.columns([1, 1])
    
    audio_path = None
    
    with col1:
        st.markdown("### Upload Audio")
        uploaded_file = st.file_uploader("Supported: mp3, wav, m4a, ogg", type=["mp3", "wav", "m4a", "ogg"])
        if uploaded_file:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            audio_path = uploaded_file.name
            st.audio(audio_path)
    
    with col2:
        st.markdown("### Input URL")
        url_input = st.text_input("Paste Audio URL")
        if url_input:
            if st.button("Download Audio"):
                audio_path = download_file(url_input)
                if audio_path:
                    st.audio(audio_path)

    # Configuration (Technical defaults hidden from UI)
    model_size = "base"
    llm_model = "llama-3.3-70b-versatile"

    if audio_path:
        st.markdown("---")
        if st.button("🚀 Analyze Session", type="primary"):
            progress_bar = st.progress(0)
            status = st.empty()
            
            try:
                # 1. Transcribe
                status.text("Transcribing audio signal...")
                progress_bar.progress(25)
                transcriber = Transcriber(model_name=model_size)
                transcript = transcriber.transcribe(audio_path)
                
                # 2. Generate
                status.text(f"Synthesizing insights with Groq ({llm_model})...")
                progress_bar.progress(75)
                # Key is pulled from .env automatically
                generator = MinutesGenerator(model=llm_model)
                minutes = generator.generate_minutes(transcript)
                
                # 3. Parse Data
                processed_data = parse_markdown_to_data(minutes)
                
                # 4. Save to DB
                title = "Meeting " + datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # Try to extract a better title from the new Metadata Table
                title_match = re.search(r"\|\s*\*\*1\. Meeting Title\*\*\s*\|\s*(.*?)\s*\|", minutes)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    # Fallback to old header extraction just in case
                    title_fallback = re.search(r"# (.*)", minutes)
                    if title_fallback:
                        candidate = title_fallback.group(1).strip()
                        if "Summary" not in candidate:
                            title = candidate

                # Database saving removed
                
                st.session_state['minutes'] = minutes
                st.session_state['transcript'] = transcript
                st.session_state['processed_data'] = processed_data
                st.session_state['current_title'] = title
                
                progress_bar.progress(100)
                st.rerun()
                
            except Exception as e:
                st.error(f"Processing Error: {str(e)}")

else:
    # --- State 2: Result / Orbital Dashboard ---
    
    # Extract data
    data = st.session_state.get('processed_data', {
        "summary": st.session_state.get('minutes', ''),
        "discussions": [], 
        "actions": []
    })
    
    # Helper to clean up rendering if parsing failed
    summary_text = data.get('summary', st.session_state['minutes'])
    current_title = st.session_state.get('current_title', 'Analysis Result')
    
    # Title Section
    st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <div style="color: var(--primary-color); font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                AI ANALYSIS COMPLETE
            </div>
            <h1>{current_title}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Metadata Tags
    render_meta_tags(
        date_str=datetime.now().strftime("%b %d, %Y"),
        duration="N/A", # Placeholder until we parse duration
        members_count="-"
    )
    
    # Action Buttons (Float right in desktop, stacked in mobile)
    col_actions_1, col_actions_2, _ = st.columns([1, 1, 4])
    with col_actions_1:
        st.button("Share", use_container_width=True)
    with col_actions_2:
        # Generate PDF on the fly
        if st.session_state.get('minutes'):
             pdf_bytes = convert_markdown_to_pdf(st.session_state['minutes'], title=current_title)
             if pdf_bytes:
                st.download_button(
                    "Export PDF", 
                    data=pdf_bytes, 
                    file_name=f"{current_title.strip().replace(' ', '_')}.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
             else:
                st.error("PDF Error")
        else:
             st.download_button("Export PDF", data="", disabled=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Content Grid
    # Top Row: Executive Insights & Discussion Matrix
    row1_1, row1_2 = st.columns([1.2, 1])
    
    with row1_1:
         render_executive_insights(summary_text)
         
    with row1_2:
        discussions = data.get('discussions', [])
        if discussions:
            render_discussion_matrix(discussions)
        else:
            st.info("No specific discussion points parsed.")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row: Action Matrix
    # We span full width or use columns
    col_action, col_empty = st.columns([2.2, 0.1])
    with col_action:
        input_actions = data.get('actions', [])
        if input_actions:
            render_action_matrix(input_actions)
        else:
             st.info("No action items parsed.")
