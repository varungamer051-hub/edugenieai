import json
import time

from google import genai

from config import settings


API_KEY = settings.gemini_api_key

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Add GEMINI_API_KEY to your .env file."
    )


client = genai.Client(api_key=API_KEY)

MODEL_NAME = settings.gemini_model


def _model_name(model):
    """
    Convert a model object/name into a usable model ID.
    """
    name = getattr(model, "name", model)

    if isinstance(name, str) and name.startswith("models/"):
        name = name[7:]

    return name


def get_available_models():
    """
    Return Gemini models that advertise generateContent support.
    """

    available = []

    try:
        for model in client.models.list():

            supported = getattr(
                model,
                "supported_actions",
                None
            )

            if supported is None:
                supported = getattr(
                    model,
                    "supported_generation_methods",
                    None
                )

            name = _model_name(model)

            if not name:
                continue

            if supported:
                supported_text = str(supported).lower()

                if (
                    "generatecontent" in supported_text
                    or "generate_content" in supported_text
                ):
                    available.append(name)

            elif "gemini" in name.lower():
                available.append(name)

    except Exception as exc:
        raise RuntimeError(
            f"Unable to retrieve Gemini models: {exc}"
        ) from exc

    return list(dict.fromkeys(available))


def _candidate_models():
    """
    Build a list beginning with the configured model,
    followed by actually available Gemini models.
    """

    candidates = []

    if MODEL_NAME:
        candidates.append(MODEL_NAME)

    try:
        available = get_available_models()

        for model in available:
            if model not in candidates:
                candidates.append(model)

    except Exception:
        # Keep the configured model if model discovery fails.
        pass

    return candidates


def generate_text(
    prompt: str,
    system_instruction: str | None = None
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    last_error = None

    for model in _candidate_models():

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "system_instruction": system_instruction
                } if system_instruction else None,
            )

            if response.text:
                return response.text

            return ""

        except Exception as exc:

            last_error = exc

            print(
                f"Gemini model failed: {model}"
            )
            print(
                f"Reason: {exc}"
            )

            continue

    raise RuntimeError(
        "No available Gemini model could generate a response. "
        f"Last error: {last_error}"
    ) from last_error

def generate_structured(prompt: str) -> dict:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    last_error = None

    for model in _candidate_models():

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                },
            )

            if not response.text:
                return {}

            try:
                return json.loads(response.text)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Gemini returned invalid JSON."
                ) from exc

        except ValueError:
            raise

        except Exception as exc:

            last_error = exc

            print(
                f"Structured Gemini model failed: {model}"
            )
            print(
                f"Reason: {exc}"
            )

            continue

    raise RuntimeError(
        "No available Gemini model could generate structured output. "
        f"Last error: {last_error}"
    ) from last_error