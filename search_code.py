from rag.retriever import CodeRetriever


def main():

    retriever = CodeRetriever()

    print("Codebase Search Ready!")

    while True:

        question = input("\nAsk about the repository (or type exit): ")

        if question.lower() == "exit":
            break

        results = retriever.retrieve(question)

        print("\nRelevant Code:\n")

        for index, result in enumerate(results, start=1):

            print(f"\nResult {index}")
            print("File:", result.get("file_path"))
            print("Symbol:", result.get("symbol_name"))
            print(
                "Lines:",
                result.get("start_line"),
                "-",
                result.get("end_line")
            )
            print("Score:", result.get("score"))
            print("\nCode:")
            print(result.get("code"))

    retriever.close()


if __name__ == "__main__":
    main()