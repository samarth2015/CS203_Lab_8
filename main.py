from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get")
async def get_best_document():
    response = requests.get("http://backend:9567/get")
    return response.json()

@app.post("/insert")
async def insert_document(text: str):
    response = requests.post("http://backend:9567/insert", json={"text": text})
    return response.json()
