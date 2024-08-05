import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.core.config import qa

router = APIRouter()


async def generate_response(query: str):
    try:
        result = qa({"query": query})
        print(result)
        answer = result['result']
        for word in answer.split():
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.1)
        yield "data: [END]\n\n"
    except Exception as e:
        print("exception", str(e))
        yield f"data: [ERROR] {str(e)}\n\n"

@router.get("/query")
async def ask_question(question: str):
    return StreamingResponse(generate_response(question), media_type='text/event-stream')