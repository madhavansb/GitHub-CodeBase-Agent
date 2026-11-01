from rag.chunking import create_code_chunks
from rag.embeddings import EmbeddingGenerator
from rag.vector_store import VectorStore


def main():

    print("Creating code chunks...")

    chunks = create_code_chunks()

    if not chunks:
        print("No code chunks found.")
        return

    print("Generating embeddings...")

    embedding_generator = EmbeddingGenerator()

    texts = [
        (
            f"File: {chunk['file_path']}\n"
            f"Symbol: {chunk['symbol_name']}\n"
            f"Code:\n{chunk['code']}"
        )
        for chunk in chunks
    ]

    embeddings = embedding_generator.generate_embeddings(texts)

    print("Connecting to Qdrant...")

    vector_store = VectorStore(
        collection_name="django_code",
        dimension=embedding_generator.get_dimension()
    )

    print("Saving vectors...")

    vector_store.add(
        embeddings,
        chunks
    )

    print("Indexing completed!")

    vector_store.close()


if __name__ == "__main__":
    main()