from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    use_smart_retrieval: bool = True
    

class SourceChunk(BaseModel):
    section_id: str
    law_name: str 
    chapter_id: str = ""
    chapter_name: str = ""
    text: str
    distance: float

class AnswerResponse(BaseModel):
    question: str
    answer: str 
    sources: list[SourceChunk] 