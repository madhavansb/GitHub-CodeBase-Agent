
from rag.retriever import CodeRetriever
from rag.answer_generator import AnswerGenerator


def main():

    retriever = CodeRetriever()
    answer_generator = AnswerGenerator()

    print("GitHub Codebase Intelligence Agent Ready!")

    try:
        while True:

            question = input("\nAsk about the repository (or type exit): ")

            if question.lower() == "exit":
                break

            print("\nSearching repository...")

            retrieved_chunks = retriever.retrieve(
                question,
                top_k=5
            )

            print("\nGenerating answer...")

            answer = answer_generator.generate_answer(
                question,
                retrieved_chunks
            )

            print("\n" + "=" * 60)
            print("ANSWER")
            print("=" * 60)

            print(answer)

    finally:
        retriever.close()


if __name__ == "__main__":
    main()
