from openai import OpenAI
from app.services.interview_db_service import get_asked_questions, store_question
from config import Config
client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)

class InterviewAgent:

    def generate_question(self, topic, difficulty):

        asked_questions = get_asked_questions()

        prompt = f"""
You are a professional technical interviewer.

Generate ONE natural interview question for a candidate.

Topic: {topic}
Difficulty: {difficulty}

Rules:
- Ask only ONE question
- Keep it short
- Make it sound natural like a real interviewer
- Keep the difficulty aligned with the given level
- Do NOT repeat these questions: {asked_questions}

Example style:
"Can you explain what polymorphism is in object oriented programming?"
"""

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a professional interviewer."},
                {"role": "user", "content": prompt}
            ]
        )

        question = response.choices[0].message.content.strip()

        store_question(question)

        return question