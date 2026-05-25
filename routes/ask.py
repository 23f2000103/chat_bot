from fastapi import APIRouter
from pydantic import BaseModel
from generator.response_generator import generate_response

from reviewer.review_agent import review_response


router = APIRouter()

class Query(BaseModel):

    question: str

@router.post("/ask")
def ask(query: Query):

    try:

        response = generate_response(query.question)

        review = review_response(query=query.question, response=response)

        escalated = (review["decision"]== "ESCALATE")

        return {
            "status": "success",
            "question": query.question,
            "response": response,
            "review": review,
            "human_escalation": escalated
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }