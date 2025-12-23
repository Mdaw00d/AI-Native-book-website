import cohere
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Cohere client from environment
cohere_api_key = os.getenv("COHERE_API_KEY", "").strip()
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY not found in environment")
cohere_client = cohere.Client(cohere_api_key)

# Connect to Qdrant from environment
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query):
    embedding = get_embedding(query)

    # Check vector dimensions before sending to Qdrant
    if len(embedding) != 1024:
        print(f"Warning: Vector dimension mismatch: expected 1024, got {len(embedding)}")

    result = qdrant.query_points(
        collection_name="padh_book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]

# Test
print(retrieve("What data do you have?"))