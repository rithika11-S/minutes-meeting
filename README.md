# Antigravity Meeting Minutes Generator

An AI-powered tool to generate professional Minutes of Meeting (MoM) from audio recordings.

## Features
- **Audio Transcription**: Uses OpenAI's Whisper model.
- **AI Analysis**: Uses Groq (Llama 3.3 / Mixtral) for blazingly fast inference.
- **Professional Output**: Generates structured Markdown reports.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a Groq API Key (from console.groq.com).
3. Create a `.env` file and add your key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage
```bash
python main.py <path_to_audio_file>
```

You can optionally pass the API key via CLI:
```bash
python main.py <path_to_audio_file> --api_key your_api_key
```

## Web Interface (Streamlit)
To run the interactive web app:
```bash
streamlit run app.py
```
