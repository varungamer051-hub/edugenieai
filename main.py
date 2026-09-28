from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="AI-powered educational learning assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files and templates
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

   return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"request": request}
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": settings.app_name,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "explanation_backend": settings.explanation_backend
    }


# ---------------------------------------------------------
# Question Answering
# ---------------------------------------------------------

@app.post("/qa")
async def qa(payload: QARequest):

    answer = answer_question(
        payload.question
    )

    return {
        "answer": answer
    }


# ---------------------------------------------------------
# Concept Explanation
# ---------------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    try:
        explanation = explain_concept(payload.text)

        return {
            "explanation": explanation
        }

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {
            "error": str(e),
            "error_type": type(e).__name__
        }

# ---------------------------------------------------------
# Quiz Generation
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    return generate_quiz(
        payload.text
    )


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# ---------------------------------------------------------
# Learning Recommendations
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: LearningPathRequest
):

    try:

        result = get_learning_recommendations(
            payload.topic,
            payload.level
        )

        return result

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "error": str(e),
            "error_type": type(e).__name__
        }