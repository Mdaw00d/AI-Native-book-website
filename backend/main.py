# main.py - Book Ingestion Pipeline

import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere
from dotenv import load_dotenv

from db import save_metadata_sync  # Your Neon DB metadata saver

load_dotenv()

# -------------------------------------
# CONFIG from .env
# -------------------------------------
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-native-book-website.vercel.app/sitemap.xml")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "padh_book")

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "").strip()
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY missing")

cohere_client = cohere.Client(COHERE_API_KEY)
EMBED_MODEL = "embed-english-v3.0"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY missing")

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


# -------------------------------------
# Helpers
# -------------------------------------
def extract_clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "footer", "header", "nav"]):
        tag.extract()
    return " ".join(soup.get_text(separator=" ").split())


def get_all_urls(sitemap_url):
    try:
        xml = requests.get(sitemap_url, timeout=10).text
        root = ET.fromstring(xml)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [loc.text for loc in root.findall(f".//{ns}loc")]
        print("\nFOUND URLS:")
        for u in urls: print(" -", u)
        return urls
    except Exception as e:
        print("❌ Sitemap error:", e)
        return []


def extract_text_from_url(url):
    try:
        html = requests.get(url, timeout=15).text
    except Exception as e:
        print(f"❌ Fetch failed {url}: {e}")
        return ""

    text = extract_clean_text(html)
    if len(text) > 50_000:
        print(f"⚠️ Skipping huge page: {url}")
        return ""
    return text


def chunk_text(text, max_chars=1200):
    if not text.strip():
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def embed(text):
    res = cohere_client.embed(model=EMBED_MODEL, input_type="search_document", texts=[text])
    vector = res.embeddings[0]

    # Check vector dimensions before storing to Qdrant
    if len(vector) != 1024:
        print(f"Warning: Ingestion: Vector dimension mismatch: expected 1024, got {len(vector)}")

    return vector


def recreate_collection():
    print(f"\nRecreating collection '{COLLECTION_NAME}'...")
    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
    )


# -------------------------------------
# Main Ingestion
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)
    if not urls:
        return

    recreate_collection()

    chunk_id = 1
    for url in urls:
        print(f"\nProcessing: {url}")
        text = extract_text_from_url(url)
        if not text:
            continue

        print(f"   → {len(text)} chars")
        for chunk in chunk_text(text):
            try:
                vector = embed(chunk)
                qdrant.upsert(
                    collection_name=COLLECTION_NAME,
                    points=[PointStruct(
                        id=chunk_id,
                        vector=vector,
                        payload={"url": url, "text": chunk, "chunk_id": chunk_id}
                    )]
                )
                save_metadata_sync(url, len(chunk))
                print(f"   → Saved chunk {chunk_id}")
                chunk_id += 1
            except Exception as e:
                print(f"❌ Error on chunk {chunk_id}: {e}")

    print(f"\n✔️ Ingestion complete! {chunk_id - 1} chunks stored.")


if __name__ == "__main__":
    ingest_book()