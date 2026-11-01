from agent.graph import agent


def main():

    print("Codebase Intelligence Agent Ready!")

    while True:

        question = input("\nAsk a question (or type exit): ")

        if question.lower() == "exit":
            break

        result = agent.invoke({
            "question": question,
            "retrieved_chunks": [],
            "answer": ""
        })

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(result["answer"])


if __name__ == "__main__":
    main()