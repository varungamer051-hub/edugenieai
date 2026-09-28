from gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational AI assistant.

Your job is to help students understand academic
and general educational questions.

Rules:

1. Answer accurately.
2. Give the direct answer first.
3. Explain difficult ideas using simple language.
4. Avoid unnecessary complexity.
5. If something is uncertain, clearly say so.
6. Do not invent sources.
7. Use examples when they improve understanding.
"""


def answer_question(
    question: str
) -> str:

    prompt = f"""
Answer the learner's question below.

QUESTION:
{question}

Response requirements:

- Start with the direct answer.
- Explain the answer clearly.
- Use simple language.
- Add an example if useful.
- Keep the response focused.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    )