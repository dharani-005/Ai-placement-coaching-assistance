from openai import OpenAI
from config import Config

client = OpenAI(
    api_key=Config.NAVIGATE_API_KEY,
    base_url=Config.NAVIGATE_BASE_URL
)

class EvaluationService:

    def evaluate_answer(self, question, transcript):

        prompt = f"""
You are an interview evaluator.

Evaluate the candidate's answer based on the following criteria.

Question:
{question}

Candidate Answer:
{transcript}

Return scores ONLY in JSON format.

Scoring Criteria:
1. relevance (0-30): How relevant the answer is to the question.
2. keyword_coverage (0-20): Coverage of important technical keywords.
3. structure_clarity (0-15): Logical structure and clarity.

Example Output:
{{
  "relevance": 25,
  "keyword_coverage": 15,
  "structure_clarity": 12
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        import json
        return json.loads(content)
    def generate_feedback(self, question, answer, score, evaluation):

        prompt = f"""
You are a professional technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluation Metrics:
Relevance: {evaluation['relevance']}
Keyword Coverage: {evaluation['keyword_coverage']}
Structure Clarity: {evaluation['structure_clarity']}
Final Score: {score['final_score']}

Provide a short, professional feedback response in 2-3 sentences.
Do not say "correct" or "wrong".
Do not mention numeric scores.
Keep the tone concise and focused on what was good and what can be improved.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are an experienced technical interviewer."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content