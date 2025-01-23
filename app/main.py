import uvicorn
from fastapi import FastAPI
from app.routers import post, tag
from app.backend.db import engine, Base

app = FastAPI()

@app.get('/')
async def welcome():
    return {'message': "Welcome to Post table"}

app.include_router(post.router)
app.include_router(tag.router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)