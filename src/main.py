from fastapi import FastAPI

from .routers import summary

app = FastAPI()

app.include_router(summary.router)


@app.get("/")
def root():
    return {"Hello": "World"}
