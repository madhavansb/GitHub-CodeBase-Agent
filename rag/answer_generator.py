
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

    def generate_answer(self, question, retrieved_chunks):

        if not retrieved_chunks:
            return "I couldn't find relevant code in this repository."

        context = ""

        for index, chunk in enumerate(retrieved_chunks, start=1):

            context += f"""
            CODE CHUNK {index}

            File: {chunk.get('file_path')}
            Symbol: {chunk.get('symbol_name')}
            Lines: {chunk.get('start_line')}-{chunk.get('end_line')}

            Code:
            {chunk.get('code')}

            """

        prompt = f"""
        You are an expert software engineer and codebase analyst.

        Answer the user's question using ONLY the provided repository code.

        Rules:
        1. Do not invent implementation details.
        2. Explain the code in beginner-friendly language.
        3. Mention relevant file paths.
        4. Include line numbers when available.
        5. If the retrieved code is insufficient, clearly say so.
        6. Distinguish confirmed facts from reasonable inferences.

        REPOSITORY CODE:
        {context}

        USER QUESTION:
        {question}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
