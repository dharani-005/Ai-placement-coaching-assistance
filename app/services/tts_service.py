from openai import OpenAI
from config import Config

client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)


class TTSService:

    def generate_speech(self, text):

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )

        output_path = "uploads/teaching_output.mp3"

        with open(output_path, "wb") as f:
            f.write(response.read())

        return output_path