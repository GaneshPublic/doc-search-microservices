from fastapi import FastAPI, HTTPException, Request
from typing import List
import logging
import os
from .db import init_db, add_document, get_document, search
from .models import DocIn, DocOut

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("doc-service")

app = FastAPI(title="Document Service (MongoDB)")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Document Service...")
    # Initialize MongoDB connection and ensure indexes
    await init_db()
    logger.info("MongoDB initialized successfully.")

@app.post("/documents", response_model=DocOut)
async def create_document(doc: DocIn, request: Request):
    logger.info(f"Received request to add document: {doc.dict()}")
    doc_id = await add_document(doc.title, doc.body)
    logger.info(f"Document added with ID: {doc_id}")
    d = await get_document(doc_id)
    logger.info(f"Returning created document: {d}")
    return d

@app.get("/documents/{doc_id}", response_model=DocOut)
async def get_doc(doc_id: str, request: Request):
    logger.info(f"Received request to get document ID: {doc_id}")
    d = await get_document(doc_id)
    if not d:
        logger.warning(f"Document ID {doc_id} not found")
        raise HTTPException(status_code=404, detail="Not found")
    logger.info(f"Returning document: {d}")
    return d

@app.get("/search", response_model=List[DocOut])
async def search_docs(q: str, limit: int = 20, request: Request = None):
    logger.info(f"Received search request. Query: '{q}', Limit: {limit}")
    results = await search(q, limit)
    logger.info(f"Search returned {len(results)} results")
    return results