from typing import TypedDict


class AgentState(TypedDict):
    question: str
    retrieved_chunks: list[dict]
    answer: str