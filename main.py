import argparse
import os
import warnings
import requests
import shutil
from dotenv import load_dotenv

# Suppress Google Generative AI deprecation warnings for cleaner output
# Must be done BEFORE importing modules that use google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

from src.transcriber import Transcriber
from src.generator import MinutesGenerator

# Load environment variables
load_dotenv()

def download_file(url):
    """Downloads a file from a URL to a temporary location."""
    print(f"Downloading audio from {url}...")
    local_filename = url.split('/')[-1]
    # Handle query parameters in URL if present
    if '?' in local_filename:
        local_filename = local_filename.split('?')[0]
    
    # Fallback name if URL doesn't have a clean filename
    if not local_filename:
        local_filename = "downloaded_audio.mp3"

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        print(f"Download complete: {local_filename}")
        return local_filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Antigravity Meeting Minutes Generator")
    parser.add_argument("audio_path", nargs="?", help="Path or URL to the meeting audio file (optional, checks env var 'AUDIO_SOURCE' if missing)")
    parser.add_argument("--model", default="base", help="Whisper model size (default: base)")
    parser.add_argument("--llm_model", default="llama-3.3-70b-versatile", help="LLM model name (default: llama-3.3-70b-versatile)")
    parser.add_argument("--api_key", default=None, help="Groq API Key (optional if GROQ_API_KEY env var is set)")
    
    args = parser.parse_args()

    # Priority 1: CLI Argument
    audio_source = args.audio_path

    # Priority 2: Environment Variable
    if not audio_source:
        audio_source = os.getenv("AUDIO_SOURCE")
        if audio_source:
            print(f"Using audio source from .env: {audio_source}")

    # Priority 3: Interactive Prompt
    if not audio_source:
        print("No audio source provided (CLI arg or AUDIO_SOURCE in .env).")
        audio_source = input("Please enter the path or URL to the audio file: ").strip("'\"")
        if not audio_source:
            print("No audio source provided. Exiting.")
            return

    # Handle URL
    if audio_source.startswith("http://") or audio_source.startswith("https://"):
        local_path = download_file(audio_source)
        if not local_path:
            return
        args.audio_path = local_path
    else:
        args.audio_path = audio_source

    if not os.path.exists(args.audio_path):
        print(f"Error: File not found at {args.audio_path}")
        return

    # 1. Transcribe Audio
    try:
        transcriber = Transcriber(model_name=args.model)
        transcript = transcriber.transcribe(args.audio_path)
        print("\n--- Transcript Generated ---\n")
        # Print preview
        print(transcript[:200] + "..." if len(transcript) > 200 else transcript)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return

    # 2. Generate Minutes
    try:
        generator = MinutesGenerator(api_key=args.api_key, model=args.llm_model)
        minutes = generator.generate_minutes(transcript)
        
        # Determine output filename
        base_name = os.path.basename(args.audio_path)
        output_filename = os.path.splitext(base_name)[0] + "_minutes.md"
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(minutes)
        
        print(f"\n--- Meeting Minutes Saved to {output_filename} ---")
        print(minutes)
        
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    main()
