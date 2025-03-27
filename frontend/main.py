from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Replace with actual internal IP of Backend VM
BACKEND_URL = "http://10.128.0.6:9567"
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/insert/{text}")  # Changed from POST to PUT
async def insert_document(text):
    response = requests.get(f"{BACKEND_URL}/insert/{text}")  # Ensure JSON format
    print(text)
    if response.status_code == 200:
        return response.json()
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/get/{query}")
async def get_best_document(query: str):
    response = requests.get(f"{BACKEND_URL}/get/{query}")
    print(query)
    if response.status_code == 200:
        return response.json()
    return JSONResponse(status_code=response.status_code, content=response.json())