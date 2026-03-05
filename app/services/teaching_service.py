from openai import OpenAI
from config import Config

client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)


class TeachingService:

    def generate_explanation(self, topic):

        prompt = f"""
Explain the following interview concept clearly and briefly.

Topic:
{topic}

Requirements:
- Keep explanation under 120 words
- Include a simple example
- Suitable for interview preparation
"""

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a technical interview tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        explanation = response.choices[0].message.content

        return explanation