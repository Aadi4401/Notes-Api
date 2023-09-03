from fastapi import FastAPI
from routes.user import user,auth_router
app = FastAPI()


app.include_router(user)
app.include_router(auth_router)
