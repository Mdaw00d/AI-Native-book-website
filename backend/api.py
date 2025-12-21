from pydantic import BaseModel
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, OpenAIChatCompletionsModel
from qdrant_client import QdrantClient
import cohere
from dotenv import load_dotenv
from openai import AsyncOpenAI

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
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
collection_name = os.getenv("QDRANT_COLLECTION", "padh_book")

# Embedding function
def embed_query(text: str):
    res = cohere_client.embed(model="embed-english-v3.0", input_type="search_query", texts=[text])
    return res.embeddings[0]

# Retrieval function
def retrieve_context(query: str, top_k: int = 5):
    vector = embed_query(query)
    
    # Use query_points to avoid attribute errors
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
        return StreamingResponse(iter([f"Retrieval error: {str(e)}"]), media_type="text/plain")

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