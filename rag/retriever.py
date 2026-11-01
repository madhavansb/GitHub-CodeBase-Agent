from rag.embeddings import EmbeddingGenerator
from rag.vector_store import VectorStore


class CodeRetriever:

    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore(
            collection_name="django_code",
            dimension=self.embedding_generator.get_dimension()
        )

    def retrieve(self, question, top_k=5):

        query_embedding = (
            self.embedding_generator.generate_embeddings(
                [question]
            )[0]
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results

    def close(self):
        self.vector_store.close()