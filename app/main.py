from fastapi import FastAPI
from app.routers import user,token
from app.database import Base,engine

app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(user.router)
app.include_router(token.router)
