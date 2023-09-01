from pydantic import BaseModel
from datetime import datetime


class Notes(BaseModel):
    noteId :int  
    title:str
    content:str
    createdAt:str
    updatedAt:str
class UpdateNotes(BaseModel):  
    title:str
    content:str
    createdAt:datetime
    updatedAt:datetime
    
class GetNote(BaseModel):
    noteId: int
    title: str
    content: str
    createdAt:datetime
    updatedAt:datetime
class NoteCreate(BaseModel):
    
    title:str
    content:str
    createdAt:datetime
    updatedAt:datetime
    
