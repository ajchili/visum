from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .routers import summary

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(summary.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="root.html", context={})
