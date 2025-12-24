from pydantic import BaseModel
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, OpenAIChatCompletionsModel
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

load_dotenv()

app = FastAPI(title="PADH Book RAG Chatbot")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ai-native-book-website.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
collection_name = os.getenv("QDRANT_COLLECTION", "padh_book")

# Embedding function using OpenAI (1536 dimensions)
def embed_query(text: str):
    res = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=1024  # Match Qdrant collection size
    )
    return res.data[0].embedding

# Retrieval function
def retrieve_context(query: str, top_k: int = 5):
    vector = embed_query(query)

    # Check vector dimensions before sending to Qdrant
    if len(vector) != 1024:
        print(f"Warning: Vector dimension mismatch: expected 1024, got {len(vector)}")
        # For now, we'll try to continue but this indicates a configuration issue
        # In production, you might want to handle this differently
        pass

    # Use query_points with proper format to avoid dimension errors
    results_obj = qdrant.query_points(
        collection_name=collection_name,
        query=vector,
        limit=top_k,
        with_payload=True,
    )

    results = results_obj.points
    contexts = [hit.payload["text"] for hit in results]
    sources = [hit.payload["url"] for hit in results]
    return "\n\n".join(contexts), sources

# === AGENT SETUP ===
system_prompt = """
You are an expert assistant for the book "Physical AI and Humanoids".
Answer questions accurately using only the provided context from the book.
If the answer is not in the context, say: "I don't know based on the book content."
Be helpful, concise, and friendly.
When relevant, cite the source URLs at the end.
"""

openai_client = AsyncOpenAI()

model = OpenAIChatCompletionsModel(
    model="gpt-4o-mini",
    openai_client=openai_client
)

agent = Agent(
    name="Book Assistant",
    instructions=system_prompt,
    model=model,
    tools=[],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message.strip()
    if not user_message:
        return StreamingResponse(iter(["Please ask a question about the book!"]), media_type="text/plain")

    try:
        context, sources = retrieve_context(user_message)
    except Exception as e:
        error_msg = str(e)
        # Handle Cohere rate limit errors specifically
        if "429" in error_msg or "rate limit" in error_msg.lower():
            error_msg = "⚠️ Rate limit reached. Please wait a moment and try again."
        else:
            error_msg = f"Retrieval error: {error_msg[:200]}"  # Truncate long errors
        return StreamingResponse(iter([error_msg]), media_type="text/plain")

    full_prompt = f"""
Context from the book:
{context}

Question: {user_message}
"""

    async def stream_response():
        try:
            # 1. Run the agent (await because it's async)
            result = await Runner.run(agent, full_prompt)
            
            # 2. Extract the clean answer
            # We explicitly check 'final_output' first because that's where the answer is hiding.
            if hasattr(result, 'final_output'):
                answer = result.final_output
            elif hasattr(result, 'content'):
                answer = result.content
            elif hasattr(result, 'output'):
                answer = result.output
            else:
                answer = str(result) # Only fallback to string dump if everything fails

            # 3. Stream the answer nicely (character by character effect)
            for char in answer:
                yield char

            # 4. Add sources at the end
            if sources:
                unique_sources = list(dict.fromkeys(sources))
                yield "\n\n**Sources:**\n"
                for url in unique_sources:
                    yield f"• {url}\n"

        except Exception as e:
            print(f"Error generation: {e}")
            yield f"\n\n[System Error]: {str(e)}"

    return StreamingResponse(stream_response(), media_type="text/plain")

@app.get("/")
def health():
    return {"status": "RAG Chatbot API is running!"}