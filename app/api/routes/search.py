# app/api/routes/search.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.encoder import image_to_vector
from app.services.vector_store import search_from_pinecone_with_image
from typing import List
from pydantic import BaseModel
from app.services.preprocessing import preprocess_image

router = APIRouter()

class SearchResult(BaseModel):
    id: str
    metadata: dict
    score: float

@router.post("/search/image", response_model=List[SearchResult])
async def search(file: UploadFile = File(...), top_k: int = 5):
    """
    Search Pinecone using an uploaded image.
    """
    try:
        image_bytes = await file.read()
        normalize_img = preprocess_image(image_bytes)
        query_vector = image_to_vector(normalize_img)
        results = search_from_pinecone_with_image(query_vector, top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    