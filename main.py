from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
INDEX_NAME = "documents"

class Document(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get")
async def get_best_document(query: str):
    search_body = {
        "query": {
            "match": {
                "text": query
            }
        }
    }
    response = es.search(index=INDEX_NAME, body=search_body)
    return response["hits"]["hits"]

@app.post("/insert")
async def insert_document(doc: Document):
    response = es.index(index=INDEX_NAME, body=doc.dict())
    return {"message": "Document inserted", "result": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)