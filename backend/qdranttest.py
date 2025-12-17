from qdrant_client import QdrantClient

qdrant = QdrantClient(
    url="https://56707107-2e68-459d-a7e9-3733be6a8a17.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.lK2J8SHa4r4pyy_rfGnlikJyGYVkPHHta8Y68n6LyoU"
)

print(qdrant.get_collections())
