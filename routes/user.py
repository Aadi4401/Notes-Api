from fastapi import APIRouter
from config.db import conn,get_db
from sqlalchemy import func
from models.models import NOTE,USER
from schemas.schemas import *
from fastapi import Depends,status
from sqlalchemy.orm.session import Session
from fastapi import WebSocket , FastAPI, Form, Response, status, HTTPException,Depends, APIRouter
from datetime import datetime
import os
from passlib.context import CryptContext
from Token import create_access_token
from oauth2 import get_current_user
import bcrypt
from sqlalchemy.orm.session import Session

current_datetime = datetime.now()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user =APIRouter(tags=['Notes'])
auth_router = APIRouter(tags=["Auth"])

@user.post("/")
async def create_note(user: NoteCreate, db: Session = Depends(get_db),Get_current_user:CreateUseR = Depends(get_current_user)):
    new_note_data = {
        "title": user.title,
        "content": user.content,
        "createdAt": current_datetime,
        "updatedAt": current_datetime,
    }

    db.execute(NOTE.insert().values(new_note_data))
    db.commit()
    return {"message": "Note created successfully"}

from sqlalchemy import update 


@user.put("/update_note/{note_id}")
async def update_note(note_id: int, user: UpdateNotes, db: Session = Depends(get_db),Get_current_user:CreateUseR = Depends(get_current_user)):
    current_datetime = datetime.now()
    existing_note = db.query(NOTE).filter(NOTE.c.noteId == note_id).first()
   
    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    update_query = (
        update(NOTE)
        .where(NOTE.c.noteId == note_id)
        .values(
            title=user.title,
            content=user.content,
            updatedAt=current_datetime
        )
    )

    
    db.execute(update_query)
    db.commit()

    return {"message": "Note updated successfully"}





@user.get("/get_note/{note_id}")
async def get_note(note_id: int, db: Session = Depends(get_db),Get_current_user:CreateUseR = Depends(get_current_user)):
    existing_note = db.query(NOTE).filter(NOTE.c.noteId == note_id).first()
    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    data={
        "noteId": existing_note.noteId,
        "title": existing_note.title,
        "content": existing_note.content,
        "updatedAt": existing_note.updatedAt,
        "createdAt": existing_note.createdAt,
       
    }
    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"data":data} 


from sqlalchemy.exc import IntegrityError

@user.delete("/delete_note/{note_id}", status_code=200)
async def delete_note(note_id: int, db: Session = Depends(get_db),Get_current_user:CreateUseR = Depends(get_current_user)):
    try:
        result = db.query(NOTE).filter(NOTE.c.noteId == note_id).delete()

        if result == 0:
            raise HTTPException(status_code=404, detail="Note not found")

        db.commit()

        return {'message': 'Note deleted successfully'}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the note")

@user.get("/get_all_notes")
async def get_all_notes(db: Session = Depends(get_db),Get_current_user:CreateUseR = Depends(get_current_user)):
    all_notes = db.query(NOTE).all()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the user is not found")
    if not all_notes:
        return {"message": "There are no notes"}

    notes_list = [{"noteId": note.noteId, "title": note.title, "content": note.content,"createdAt":note.createdAt,"updatedAt":note.updatedAt} for note in all_notes]
    return notes_list


@auth_router.post("/createUser")
async def createUser(user:CreateUseR,db:Session = Depends(get_db)):
    existing_user = db.query(USER).filter(USER.c.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")


    hashed_password = pwd_context.hash(user.password)
    new_user = {
        "email": user.email,
        "password": hashed_password,
    }
    db.execute(USER.insert().values(new_user))
    db.commit()
    return {"message": "User created successfully"}


from fastapi.security import OAuth2PasswordRequestForm
@auth_router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(USER).filter(USER.c.email == user.username).first()
    
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
