from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import summary

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(summary.router)


@app.get("/")
def root():
    return {"Hello": "World"}
