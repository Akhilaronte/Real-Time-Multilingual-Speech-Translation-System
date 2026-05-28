# backend/main.py
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os, base64

from transcriber import Transcriber
from translator import Translator
from synthesizer import Synthesizer

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

transcriber = Transcriber(model_size="base")
translator = Translator()
synthesizer = Synthesizer()

@app.post("/translate")
async def translate_audio(
    file: UploadFile = File(...),
    target_lang: str = "fr"
):
    # Save uploaded audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Pipeline
    transcription = transcriber.transcribe(tmp_path)
    src_lang = transcription["language"]
    translated_text = translator.translate(
        transcription["text"], src_lang, target_lang
    )
    output_path = tmp_path.replace(".wav", "_out.wav")
    synthesizer.synthesize(translated_text, output_path)

    # Return audio as base64
    with open(output_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    os.unlink(tmp_path)
    os.unlink(output_path)

    return {
        "original_text": transcription["text"],
        "source_language": src_lang,
        "translated_text": translated_text,
        "audio_base64": audio_b64
    }

# Run: uvicorn main:app --reload --port 8000