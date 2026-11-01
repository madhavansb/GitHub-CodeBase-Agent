from qdrant_client import QdrantClient, models


class VectorStore:

    def __init__(
        self,
        collection_name="code_chunks",
        storage_path="storage/qdrant",
        dimension=384
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            path=storage_path
        )

        collections = self.client.get_collections().collections

        existing = [
            collection.name for collection in collections
        ]

        if collection_name not in existing:

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=dimension,
                    distance=models.Distance.COSINE
                )
            )

    def add(self, embeddings, chunks):

        points = []

        for index, (embedding, chunk) in enumerate(
            zip(embeddings, chunks)
        ):

            points.append(
                models.PointStruct(
                    id=index,
                    vector=embedding.tolist(),
                    payload=chunk
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_embedding, top_k=5):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            with_payload=True
        ).points

        return [
            {
                "score": result.score,
                **result.payload
            }
            for result in results
        ]

    def close(self):

        self.client.close()