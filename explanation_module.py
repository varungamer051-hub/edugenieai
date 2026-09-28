from gemini_client import generate_text


def explain_concept(text: str) -> str:

    prompt = f"""
You are EduGenie, an AI educational tutor.

Explain the following concept clearly and accurately.

Student level: beginner

Topic:
{text}

Instructions:
- Use simple language.
- Explain the core idea first.
- Give a practical example.
- Use short sections.
- Avoid unnecessary technical jargon.
- Make the explanation useful for a student.
"""

    return generate_text(prompt)