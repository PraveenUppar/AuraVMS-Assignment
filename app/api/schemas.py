from pydantic import BaseModel

class CreatePostRequest(BaseModel):
    text: str
    author: str

class ReviewActionRequest(BaseModel):
    action: str 
