import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="qr_service/static"), name="static")

templates = Jinja2Templates(directory="qr_service/templates")


@app.on_event("startup")
async def startup_event():
    print(f'Activate the QR code http://localhost:8000/qr')


@app.get("/qr", response_class=HTMLResponse)
async def qr_code(request: Request):
    hash_str = datetime.datetime.now().isoformat()
    return templates.TemplateResponse("index.html", {"request": request, "hash_str": hash_str})
