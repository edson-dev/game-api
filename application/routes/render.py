
from fastapi.responses import HTMLResponse, Response
from starlette.requests import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()
template = Jinja2Templates(directory="./templates")
template.env.block_start_string = "[%"
template.env.block_end_string = "%]"
template.env.variable_start_string = "[["
template.env.variable_end_string = "]]"

@router.get("", response_class=HTMLResponse)
async def index(request: Request):
    data = {}
    print(f"data-load-page:{data}")
    return template.TemplateResponse("index.html", {"request": request,
                                                     "data_link": ['http://127.0.0.1:8080/index-data','http://127.0.0.1:8080/index-data2']})
