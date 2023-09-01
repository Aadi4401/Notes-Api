from fastapi import APIRouter
from config.db import conn,get_db
from sqlalchemy import func
from models.models import NOTE
# from schemas.index import User
from schemas.schemas import *
from fastapi import Depends
from sqlalchemy.orm.session import Session
from fastapi import WebSocket , FastAPI, Form, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from datetime import datetime
current_datetime = datetime.now()
user =APIRouter()

from sqlalchemy.orm.session import Session
@user.post("/")
async def create_note(user: NoteCreate, db: Session = Depends(get_db)):
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
async def update_note(note_id: int, user: UpdateNotes, db: Session = Depends(get_db)):
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
async def get_note(note_id: int, db: Session = Depends(get_db)):
    # Query the database to retrieve the note by noteId
    print(note_id)
    print(note_id)
    print(note_id)
    existing_note = db.query(NOTE).filter(NOTE.c.noteId == note_id).first()
    data={
        "noteId": existing_note.noteId,
        "name": existing_note.title,
        "email_id": existing_note.content,
        "updatedAt": existing_note.updatedAt,
        "createdAt": existing_note.createdAt,
       
    }
    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"data":data} 


from sqlalchemy.exc import IntegrityError

@user.delete("/delete_note/{note_id}", status_code=200)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    try:
        # Delete the note from the database
        result = db.query(NOTE).filter(NOTE.c.noteId == note_id).delete()

        if result == 0:
            raise HTTPException(status_code=404, detail="Note not found")

        db.commit()

        return {'message': 'Note deleted successfully'}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the note")

@user.get("/get_all_notes")
async def get_all_notes(db: Session = Depends(get_db)):
    all_notes = db.query(NOTE).all()

    if not all_notes:
        return {"message": "There are no notes"}

    notes_list = [{"noteId": note.noteId, "title": note.title, "content": note.content} for note in all_notes]
    return notes_list
