
from sqlalchemy import Table, Column, String, MetaData,Integer,DateTime
from sqlalchemy import func

metadata = MetaData()

NOTES = Table(
    "notes",
    metadata,
    Column("noteId", Integer,primary_key=True, autoincrement=True),
    Column("title", String),
    Column("content", String),
    Column("createdAt", DateTime, default=func.current_timestamp()),
    Column("updatedAt", DateTime, onupdate=func.current_timestamp()),
)

NOTE = Table(
    "note",
    metadata,
    Column("noteId", Integer),
    Column("title", String),
    Column("content", String),
    Column("createdAt", DateTime, default=func.current_timestamp()),
    Column("updatedAt", DateTime, onupdate=func.current_timestamp()),
)
