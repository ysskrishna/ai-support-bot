from pydantic import BaseModel

class ChatQuestionSchema(BaseModel):
    question: str