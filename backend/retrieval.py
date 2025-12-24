from openai import OpenAI
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client from environment
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
openai_client = OpenAI(api_key=openai_api_key)

# Connect to Qdrant from environment
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def get_embedding(text):
    """Get embedding vector from OpenAI"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=1024  # Match Qdrant collection size
    )
    return response.data[0].embedding

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