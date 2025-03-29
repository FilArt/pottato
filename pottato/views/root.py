from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

TEMPLATES_DIR = Path("pottato/views/templates")

router = APIRouter(prefix="", tags=["root"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
