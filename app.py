from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
from pydub import AudioSegment
import os
import uuid

app = FastAPI(
    title="Voice Cloning API",
    description="Clones a voice and narrates the given script using Coqui YourTTS",
    version="1.0"
)

# --- Ensure folders exist ---
os.makedirs("samples", exist_ok=True)
os.makedirs("output", exist_ok=True)

# --- Load the Coqui TTS model ---
# (~1.5GB download the first time)
print("🔄 Loading Coqui YourTTS model...")
tts_model = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)
print("✅ Model loaded successfully!")


@app.post("/clone/")
async def clone_voice(audio_file: UploadFile, script: str = Form(...)):
    """
    Upload a short voice sample and a text script.
    The API will clone the voice and synthesize speech in that style.
    """
    # --- Save uploaded voice ---
    input_ext = os.path.splitext(audio_file.filename)[1].lower()
    ref_path = f"samples/ref_{uuid.uuid4().hex}{input_ext}"
    with open(ref_path, "wb") as f:
        f.write(await audio_file.read())

    # --- Convert to WAV if not already ---
    wav_path = ref_path
    if input_ext != ".wav":
        sound = AudioSegment.from_file(ref_path)
        wav_path = ref_path.replace(input_ext, ".wav")
        sound.export(wav_path, format="wav")

    # --- Generate cloned voice output ---
    out_path = f"output/cloned_{uuid.uuid4().hex}.wav"

    print("🗣️ Generating cloned speech...")
    tts_model.tts_to_file(
        text=script,
        file_path=out_path,
        speaker_wav=wav_path,
        language="en"
    )

    print("✅ Cloned speech saved:", out_path)
    return FileResponse(out_path, media_type="audio/wav", filename=os.path.basename(out_path))


@app.get("/")
def home():
    return {"message": "Welcome to Voice Cloning API! Use /clone/ endpoint to synthesize."}
