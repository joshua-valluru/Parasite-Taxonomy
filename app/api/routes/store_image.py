from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from uuid import uuid4
from app.services.encoder import image_to_vector
from app.services.vector_store import upsert_to_pinecone
from app.services.image_quality import assess_image_quality
from app.services.preprocessing import preprocess_image

router = APIRouter()

@router.post("/")
async def store_image(
    file: UploadFile, 
    parasite_name: str = Form(...),
    concentration: float = Form(...), 
    ):
    try:
        image_bytes = await file.read()

        # Assess image quality
        quality = assess_image_quality(image_bytes)

        if quality["sharpness"] < 100:
            return JSONResponse(status_code=400, content={"error": "Image too blurry"})

        if quality["black_clip"] > 1000 or quality["white_clip"] > 1000:
            return JSONResponse(status_code=400, content={"error": "Image too dark or too bright"})

        if quality["bg_std"] > 25:
            return JSONResponse(status_code=400, content={"error": "Background not uniform"})

        # Obtain a normalized image via preprocessing pipeline
        normalize_img = preprocess_image(image_bytes)

        # Obtain encoded image
        image_vector = image_to_vector(normalize_img)

        # Generate image uuid
        image_id = str(uuid4())

        # Image and text embeddings share the same metadata
        image_metadata = {
            "timestamp" : str(datetime.now(timezone.utc)),
            "parasite_name": parasite_name,
            "concentration" : concentration,
            "filename": file.filename
        }

        upsert_to_pinecone(image_id, image_vector, image_metadata)

        return JSONResponse({
            "image_id": image_id,
            "status": "success"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
