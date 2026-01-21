import whisper
import os

class Transcriber:
    def __init__(self, model_name="base"):
        """
        Initialize the Transcriber with a specific Whisper model.
        Args:
            model_name (str): The name of the Whisper model to load (e.g., "base", "small", "medium").
        """
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
        print("Model loaded successfully.")

    def transcribe(self, audio_path):
        """
        Transcribe the audio file at the given path.
        Args:
            audio_path (str): Path to the audio file.
        Returns:
            str: The transcribed text.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing audio: {audio_path}...")
        # fp16=False to ensure compatibility with CPU if GPU is not available/supported for fp16
        result = self.model.transcribe(audio_path, fp16=False)
        return result["text"].strip()
