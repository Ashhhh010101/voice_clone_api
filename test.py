import requests
import sounddevice as sd
from scipy.io.wavfile import write
import io
import os

# ==== CONFIGURATION ====
API_URL = "#######"  # 🔁 Replace with your actual Render API URL
SAMPLE_RATE = 22050
RECORD_SECONDS = 5
INPUT_FILE = "input_voice.wav"
OUTPUT_FILE = "cloned_voice.wav"

# ==== RECORD VOICE ====
def record_voice():
    print("🎙️ Recording... Speak now!")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(INPUT_FILE, SAMPLE_RATE, audio)
    print(f"✅ Recording saved as {INPUT_FILE}")

# ==== SEND TO API ====
def send_to_api():
    if not os.path.exists(INPUT_FILE):
        print("❌ Input file not found. Please record first.")
        return
    
    print("🚀 Sending audio to API...")
    with open(INPUT_FILE, "rb") as f:
        files = {"file": (INPUT_FILE, f, "audio/wav")}
        try:
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                print("✅ API responded successfully.")
                # Save the cloned audio
                with open(OUTPUT_FILE, "wb") as out:
                    out.write(response.content)
                print(f"🔊 Cloned voice saved as {OUTPUT_FILE}")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"⚠️ Request failed: {e}")

if __name__ == "__main__":
    record_voice()
    send_to_api()
