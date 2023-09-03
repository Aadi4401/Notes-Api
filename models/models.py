
from sqlalchemy import Table, Column, String, MetaData,Integer,DateTime
from sqlalchemy import func

metadata = MetaData()

USER = Table(
    "tbl_user",
    metadata,
    Column("id", Integer,primary_key=True, autoincrement=True),
    Column("email", String,unique=True),
    Column("password", String),
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
