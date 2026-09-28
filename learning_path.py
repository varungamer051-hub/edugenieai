import json

from pydantic import BaseModel, Field

from gemini_client import generate_structured


# =========================================================
# MODELS
# =========================================================

class LearningStep(BaseModel):

    stage: str

    topics: list[str]

    suggested_duration: str

    activities: list[str]

    resources: list[str]


class LearningPath(BaseModel):

    topic: str

    learner_level: str

    goal: str

    steps: list[LearningStep]

    study_tips: list[str]


# =========================================================
# LEARNING PATH GENERATOR
# =========================================================

def get_learning_recommendations(
    topic: str,
    level: str = "beginner"
) -> dict:

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not topic or not topic.strip():

        raise ValueError(
            "Learning topic cannot be empty."
        )

    topic = topic.strip()

    if not level or not level.strip():

        level = "beginner"

    level = level.strip()


    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt = f"""
You are EduGenie, an AI educational learning assistant.

Create a personalized learning path.

TOPIC:
{topic}

LEARNER LEVEL:
{level}

IMPORTANT:

The learning path MUST be specifically about the requested topic.

Do NOT create generic questions or generic recommendations.

For example, if the topic is:

"Learn Python programming from beginner to intermediate"

the learning path should contain topics such as:

- Python basics
- Variables
- Data types
- Operators
- Conditional statements
- Loops
- Functions
- Lists
- Tuples
- Dictionaries
- File handling
- Exception handling
- Object-oriented programming
- Modules
- Practical Python projects

Adapt the topics according to the requested subject.

Create exactly 5 progressive learning stages.

The stages should move from the learner's current level
toward the requested learning goal.

Each stage must contain:

- stage
- topics
- suggested_duration
- activities
- resources

Also provide:

- topic
- learner_level
- goal
- study_tips


IMPORTANT OUTPUT RULE:

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use ```json.

Do NOT add explanations before or after the JSON.

Use exactly this structure:

{{
    "topic": "the requested topic",
    "learner_level": "the learner level",
    "goal": "clear learning goal",
    "steps": [
        {{
            "stage": "Stage 1",
            "topics": [
                "topic 1",
                "topic 2",
                "topic 3"
            ],
            "suggested_duration": "1 week",
            "activities": [
                "activity 1",
                "activity 2"
            ],
            "resources": [
                "resource type 1",
                "resource type 2"
            ]
        }},
        {{
            "stage": "Stage 2",
            "topics": [
                "topic 1",
                "topic 2",
                "topic 3"
            ],
            "suggested_duration": "1 week",
            "activities": [
                "activity 1",
                "activity 2"
            ],
            "resources": [
                "resource type 1",
                "resource type 2"
            ]
        }},
        {{
            "stage": "Stage 3",
            "topics": [
                "topic 1",
                "topic 2",
                "topic 3"
            ],
            "suggested_duration": "1 week",
            "activities": [
                "activity 1",
                "activity 2"
            ],
            "resources": [
                "resource type 1",
                "resource type 2"
            ]
        }},
        {{
            "stage": "Stage 4",
            "topics": [
                "topic 1",
                "topic 2",
                "topic 3"
            ],
            "suggested_duration": "1 week",
            "activities": [
                "activity 1",
                "activity 2"
            ],
            "resources": [
                "resource type 1",
                "resource type 2"
            ]
        }},
        {{
            "stage": "Stage 5",
            "topics": [
                "topic 1",
                "topic 2",
                "topic 3"
            ],
            "suggested_duration": "1 week",
            "activities": [
                "activity 1",
                "activity 2"
            ],
            "resources": [
                "resource type 1",
                "resource type 2"
            ]
        }}
    ],
    "study_tips": [
        "tip 1",
        "tip 2",
        "tip 3"
    ]
}}

Do not invent specific URLs.

Use resource TYPES instead, such as:

- documentation
- textbook
- practice exercises
- coding exercises
- projects
- videos
- notes

Make the learning path practical and suitable for a student.
"""


    # -----------------------------------------------------
    # Call Gemini
    # -----------------------------------------------------

    try:

        # IMPORTANT:
        # Your current generate_structured() accepts
        # only ONE argument.

        raw_response = generate_structured(
            prompt
        )

    except Exception as error:

        raise RuntimeError(
            f"Gemini learning-path generation failed: {error}"
        ) from error


    # -----------------------------------------------------
    # Handle response
    # -----------------------------------------------------

    if isinstance(raw_response, dict):

        data = raw_response

    else:

        if not isinstance(raw_response, str):

            raise RuntimeError(
                "Gemini returned an unsupported response type."
            )

        cleaned = raw_response.strip()


        # -------------------------------------------------
        # Remove Markdown code block if Gemini adds one
        # -------------------------------------------------

        if cleaned.startswith("```"):

            lines = cleaned.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()


        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            data = json.loads(
                cleaned
            )

        except json.JSONDecodeError as error:

            raise RuntimeError(
                "Gemini returned invalid JSON for the learning path.\n"
                f"Raw response:\n{cleaned}"
            ) from error


    # -----------------------------------------------------
    # Validate with Pydantic
    # -----------------------------------------------------

    try:

        learning_path = LearningPath.model_validate(
            data
        )

    except Exception as error:

        raise RuntimeError(
            f"Learning path validation failed: {error}"
        ) from error


    # -----------------------------------------------------
    # Return normal dictionary
    # -----------------------------------------------------

    return learning_path.model_dump()