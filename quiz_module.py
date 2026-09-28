import json

from pydantic import BaseModel, Field, field_validator

from gemini_client import generate_text


# =========================================================
# QUIZ MODELS
# =========================================================

class QuizQuestion(BaseModel):
    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, value, info):

        options = info.data.get("options", [])

        if options and value not in options:
            raise ValueError(
                "correct_answer must exactly match one of the options."
            )

        return value


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


# =========================================================
# JSON CLEANER
# =========================================================

def clean_json(text: str) -> str:

    if not text:
        raise ValueError("Gemini returned an empty response.")

    text = text.strip()

    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.splitlines()

        # Remove first line: ```json or ```
        if lines:
            lines = lines[1:]

        # Remove last ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # Sometimes Gemini adds text before/after JSON.
    # Extract the JSON object.
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


# =========================================================
# QUIZ GENERATOR
# =========================================================

def generate_quiz(text: str) -> dict:

    if not text or not text.strip():
        raise ValueError(
            "Educational material cannot be empty."
        )

    prompt = f"""
Create exactly THREE multiple-choice questions
from the educational material below.

EDUCATIONAL MATERIAL:
{text}

IMPORTANT RULES:

1. Create exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option can be correct.
4. correct_answer MUST exactly match one of the 4 options.
5. Give a short explanation for every answer.
6. Use ONLY information from the supplied material.
7. Do not invent facts.
8. Return ONLY valid JSON.
9. Do NOT use markdown.
10. Do NOT write ```json.
11. Do NOT write any explanation outside the JSON.

Return this exact JSON structure:

{{
    "questions": [
        {{
            "question": "Question 1",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "explanation": "Short explanation."
        }},
        {{
            "question": "Question 2",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option B",
            "explanation": "Short explanation."
        }},
        {{
            "question": "Question 3",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option C",
            "explanation": "Short explanation."
        }}
    ]
}}
"""

    # Use the working Gemini function.
    raw_response = generate_text(prompt)

    print("========== QUIZ GEMINI RESPONSE ==========")
    print(raw_response)
    print("==========================================")

    # Clean Gemini response.
    cleaned = clean_json(raw_response)

    print("========== CLEANED QUIZ JSON =============")
    print(cleaned)
    print("==========================================")

    try:
        data = json.loads(cleaned)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Gemini did not return valid JSON. "
            f"Raw response: {raw_response}"
        ) from error

    try:
        quiz = QuizResponse.model_validate(data)

    except Exception as error:
        raise RuntimeError(
            f"Quiz JSON failed validation: {error}"
        ) from error

    return quiz.model_dump()