from openai import OpenAI
from app.services.interview_db_service import get_asked_questions, store_question
from config import Config
client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)

class InterviewAgent:

    def detect_topic(self, text):

        text = text.lower()

        if "oop" in text or "object" in text:
            return "Object Oriented Programming"

        if "dbms" in text:
            return "Database Management Systems"

        if "self intro" in text or "introduce" in text:
            return "HR introduction"

        return "Object Oriented Programming"


    def generate_question(self, user_prompt):

        topic = self.detect_topic(user_prompt)

        asked_questions = get_asked_questions()

        prompt = f"""
You are a professional technical interviewer.

Generate ONE natural interview question for a candidate.

Topic: {topic}

Rules:
- Ask only ONE question
- Keep it short
- Make it sound natural like a real interviewer
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