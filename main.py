from agent.graph_builder import build_graph
from agent.config import VERBOSE


def main():
    app = build_graph()

    if VERBOSE == True:
        print("LangGraph agent is ready.")
        print("Enter your question below.\n")

    question = input("Ask your question: ").strip()

    result = app.invoke(
        {
            "question": question,
            "attempts": 0,
        },
        config={"recursion_limit": 20},
    )

    print("\n" + "=" * 80)
    print(result.get("final_answer", "No final answer returned."))
    print("=" * 80)


if __name__ == "__main__":
    main()