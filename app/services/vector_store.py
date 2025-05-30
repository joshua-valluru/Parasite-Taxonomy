from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load env variables (make sure .env file exists in your project root)
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)

def upsert_to_pinecone(item_id: str, vector: list, metadata: dict):
    index = pc.Index(name=INDEX_NAME)
    index.upsert([(item_id, vector, metadata)])

def search_from_pinecone_with_image(query_vector: list, top_k: int = 5):
    """
    Search Pinecone for images similar to the input image.
    """
    # Query Pinecone
    index = pc.Index(INDEX_NAME)
    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
    )

    # Format and return
    return [
        {
            "id": match["id"],
            "metadata": match.get("metadata", {}),
            "score": match["score"]
        }
        for match in result["matches"]
    ]
