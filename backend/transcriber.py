# backend/transcriber.py
import whisper
import torch

class Transcriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        # model sizes: tiny, base, small, medium, large
        # Start with "base" for speed

    def transcribe(self, audio_path: str, language: str = None):
        result = self.model.transcribe(
            audio_path,
            language=language,  # None = auto-detect
            fp16=torch.cuda.is_available()
        )
        return {
            "text": result["text"],
            "language": result["language"],
            "segments": result["segments"]  # timestamps!
        }