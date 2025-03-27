from fastapi import FastAPI
from elasticsearch import Elasticsearch
from uuid import uuid4
import uvicorn
import os

app = FastAPI()

# Elasticsearch running inside the backend VM
ES_HOST = os.getenv("ES_HOST", "http://localhost:9567/es/")  # Default to localhost for local runs
es = Elasticsearch(ES_HOST)
INDEX_NAME = "documents"


def add_initial():
    """Ensure index exists"""
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "text": {"type": "text"}
                }
            }
        })
add_initial()


@app.get("/get/{query}")
async def get_best_document(query: str):
    print(query)
    response = es.search(index=INDEX_NAME, body={
        "query": {"match": {"text": query}}
    })
    return {"hits": response["hits"]["hits"]}
    


@app.get("/insert/{text}")
async def insert_document(text: str):
    print(text)
    doc_id = str(uuid4())
    doc = {"id": doc_id, "text": text}
    response = es.index(index=INDEX_NAME, id=doc_id, document=doc)
    return {"result": response["result"], "id": doc_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9567)
