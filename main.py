from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import uvicorn

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get")
async def get_best_document():
    response = requests.get("http://0.0.0.0:9567/get")
    return response.json()

@app.post("/insert")
async def insert_document(text: str):
    response = requests.post("http://0.0.0.0:9567/get", json={"text": text})
    return response.json()

if(__name__ == "__main__"):
    uvicorn.run(app, host="0.0.0.0", port=9567)