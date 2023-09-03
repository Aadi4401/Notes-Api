from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr



class CreateUseR(BaseModel):
    email:EmailStr
    password:str

class LoginUser(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class Notes(BaseModel):
    noteId :int  
    title:str
    content:str
    createdAt:str
    updatedAt:str
class UpdateNotes(BaseModel):  
    title:str
    content:str
    
class GetNote(BaseModel):
    noteId: int
    title: str
    content: str
    createdAt:datetime
    updatedAt:datetime
class NoteCreate(BaseModel):
    
    title:str
    content:str
    
