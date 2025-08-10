from pydantic import BaseModel

class SentimentBase(BaseModel):
    text: str

class SentimentCreate(SentimentBase):
    pass

class SentimentUpdate(SentimentBase):
    pass

class SentimentResponse(SentimentBase):
    id: int
    sentiment: str

    class Config:
        orm_mode = True
