from rag.retriever import CodeRetriever
from rag.answer_generator import AnswerGenerator


retriever = CodeRetriever()
answer_generator = AnswerGenerator()


def retrieve_code(state: dict) -> dict:
    """Retrieve relevant code from Qdrant."""

    question = state["question"]

    chunks = retriever.retrieve(
        question,
        top_k=5
    )

    return {
        "retrieved_chunks": chunks
    }


def generate_answer(state: dict) -> dict:
    """Generate an answer grounded in retrieved code."""

    answer = answer_generator.generate_answer(
        state["question"],
        state["retrieved_chunks"]
    )

    return {
        "answer": answer
    }