from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
Summarize the following educational text.

TEXT:

{text}

Requirements:

- Preserve important information.
- Remove repetition.
- Use simple language.
- Keep the key concepts.
- Make it useful for exam revision.
- Do not introduce information that isn't in the text.
- Use bullet points when appropriate.
"""

    return generate_text(
        prompt
    )