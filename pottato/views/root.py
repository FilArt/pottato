from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from pottato.services.db.models import FileModel
from pydantic import BaseModel

TEMPLATES_DIR = Path("pottato/views/templates")

router = APIRouter(prefix="", tags=["root"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


class CodeSchema(BaseModel):
    code: str


@router.post("/run-code")
async def run_code(code: CodeSchema):
    """
    Evaluates python code and returns the result
    """
    try:
        result = str(eval(code.code))
    except Exception as e:
        result = str(e)
    return {"result": result}


@router.get("/files", response_class=FileModel)
async def get_files():
    files = await FileModel.all()
    return {"files": files}
