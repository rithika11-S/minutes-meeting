import streamlit as st
import datetime

def render_header():
    st.markdown("""
        <div class="orbital-header">
            <div class="orbital-logo">
                <span>⚡</span> ORBITAL SUMMARY
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <input type="text" class="search-bar" placeholder="Search meetings...">
                <div class="user-profile">
                    <div class="user-avatar">R</div>
                    <span style="font-weight: 500; font-size: 0.9rem;">Rithika</span>
                </div>
                <button style="background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.5rem; cursor: pointer;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_meta_tags(date_str, duration, members_count):
    st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
            <div class="meta-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                {date_str}
            </div>
            <div class="meta-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {duration}
            </div>
            <div class="meta-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
                {members_count} Members
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_executive_insights(text):
    # Convert newlines to breaks for HTML display
    import html
    safe_text = html.escape(text).replace('\n', '<br>')
    
    # We use a flat string to completely avoid Markdown indentation issues
    html_content = f"""
<div class="orbital-card" style="height: 100%; overflow-y: auto;">
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="2">
<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
<polyline points="14 2 14 8 20 8"></polyline>
<line x1="16" y1="13" x2="8" y2="13"></line>
<line x1="16" y1="17" x2="8" y2="17"></line>
<polyline points="10 9 9 9 8 9"></polyline>
</svg>
<h3 style="margin:0 !important; color: #000000 !important;">Executive Insights</h3>
</div>
<div style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">
{safe_text}
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_discussion_matrix(points):
    items_html = ""
    for point in points:
        items_html += f"""
<li style="margin-bottom: 0.75rem; color: #4b5563;">
<span style="color: var(--primary-color); font-weight: bold; margin-right: 0.5rem;">•</span>
{point}
</li>"""
    
    html_content = f"""
<div class="orbital-card" style="height: 100%;">
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="2">
<circle cx="12" cy="12" r="10"></circle>
<polyline points="12 6 12 12 16 14"></polyline>
</svg>
<h3 style="color: #000000 !important;">Key Discussion Matrix</h3>
</div>
<ul style="list-style: none; padding: 0; margin: 0;">
{items_html}
</ul>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_action_matrix(actions):
    cards_html = ""
    for action in actions:
        cards_html += f"""
<div style="background: #f9fafb; border-radius: 0.75rem; padding: 1rem; margin-bottom: 0.75rem; border-left: 3px solid var(--primary-color);">
<div style="font-weight: 600; color: #111827; margin-bottom: 0.5rem;">{action.get('task', '')}</div>
<div style="display: flex; gap: 0.5rem; font-size: 0.75rem;">
<div style="background: #e0e7ff; color: #3730a3; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500;">
{action.get('owner', 'Unassigned')}
</div>
<div style="background: #fee2e2; color: #991b1b; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500;">
Due {action.get('due_date', 'TBD')}
</div>
</div>
</div>"""

    html_content = f"""
<div class="orbital-card" style="height: 100%;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
<h3 style="color: #000000 !important;">ACTION MATRIX</h3>
<span style="color: var(--primary-color);">⚡</span>
</div>
{cards_html}
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

