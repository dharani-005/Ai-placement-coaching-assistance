from openai import OpenAI
from config import Config
import os
import time
import uuid

client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)


class TTSService:

    def _cleanup_old_audio_files(self, max_age_seconds=300):
        if not os.path.exists("uploads"):
            return

        now = time.time()
        for file_name in os.listdir("uploads"):
            if not file_name.lower().endswith(".mp3"):
                continue
            file_path = os.path.join("uploads", file_name)
            try:
                if now - os.path.getmtime(file_path) > max_age_seconds:
                    os.remove(file_path)
            except OSError:
                pass

    def generate_speech(self, text):
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        self._cleanup_old_audio_files()

        filename = f"tts_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join("uploads", filename)

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )

        with open(output_path, "wb") as f:
            f.write(response.read())

        return f"uploads/{filename}"