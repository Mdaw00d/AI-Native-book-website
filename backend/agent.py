# agent.py - RAG Agent for querying the book

import os
from dotenv import load_dotenv

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool

import cohere
from qdrant_client import QdrantClient

load_dotenv()

# -------------------------------------
# Shared Config (same as main.py)
# -------------------------------------
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "padh_book")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY missing")
cohere_client = cohere.Client(COHERE_API_KEY)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT credentials missing")

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY missing")

# -------------------------------------
# Embedding & Retrieval
# -------------------------------------
def get_embedding(text):
    res = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text]
    )
    vector = res.embeddings[0]

    # Check vector dimensions before sending to Qdrant
    if len(vector) != 1024:
        print(f"Warning: Vector dimension mismatch: expected 1024, got {len(vector)}")

    return vector


@function_tool
def retrieve(query: str) -> str:
    """Retrieve relevant sections from the Physical AI & Humanoid Robotics book."""
    embedding = get_embedding(query)

    # Check vector dimensions before sending to Qdrant
    if len(embedding) != 1024:
        print(f"Warning: Vector dimension mismatch: expected 1024, got {len(embedding)}")

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=5,
        with_payload=True
    )
    texts = [hit.payload["text"] for hit in results]
    return "\n\n".join(texts) if texts else "No relevant content found."


# -------------------------------------
# Agent Setup
# -------------------------------------
provider = AsyncOpenAI(api_key=OPENAI_API_KEY)

model = OpenAIChatCompletionsModel(
    model="gpt-4o-mini",  # Fast & cheap; change to gpt-4o if you want better reasoning
    openai_client=provider
)

set_tracing_disabled(True)

agent = Agent(
    name="Padh Book Tutor",
    instructions="""
You are an expert tutor for the textbook "Physical AI & Humanoid Robotics".

Rules:
- Always call the `retrieve` tool first with the user's question.
- Answer using ONLY the content returned by `retrieve`.
- If the information is not in the retrieved text, say: "I don't know based on the book."
- Be clear, educational, and concise.
- Cite key ideas naturally from the source.
""",
    model=model,
    tools=[retrieve]
)


# -------------------------------------
# Query Functions
# -------------------------------------
def ask_question(question: str):
    print(f"\n🤔 Question: {question}")
    result = Runner.run_sync(agent, input=question)
    print(f"\n✅ Answer:\n{result.final_output}\n")


# -------------------------------------
# Interactive Mode
# -------------------------------------
if __name__ == "__main__":
    print("Padh Book Tutor Ready! Ask questions about Physical AI & Humanoid Robotics.")
    print("(Type 'exit' to quit)\n")

    while True:
        try:
            q = input("You: ").strip()
            if q.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break
            if q:
                ask_question(q)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break