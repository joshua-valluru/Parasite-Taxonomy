from fastapi import FastAPI
from app.api.routes import store_image, search

app = FastAPI()

# Include routers
app.include_router(store_image.router, prefix="/store-image", tags=["store"])
app.include_router(search.router, prefix="/search", tags=["search"])
