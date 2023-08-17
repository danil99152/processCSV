from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from service.routers import router
from settings import settings

services_router = APIRouter(prefix='')

templates = Jinja2Templates(directory=f'{settings.APP_PATH}/templates')

services_router.include_router(router=router)


@services_router.get('/file', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})