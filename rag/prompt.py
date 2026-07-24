# prompt.py

from langchain_core.prompts import ChatPromptTemplate


class PromptTemplates:
    """
    Contains all prompt templates used in the application.
    """

    @staticmethod
    def rag_prompt():
        return ChatPromptTemplate.from_template(
            """
You are an intelligent AI assistant.

Your task is to answer the user's question using ONLY the information provided in the context.

Instructions:
- Answer only from the provided context.
- Do not use your own knowledge.
- If the answer is not present in the context, respond exactly with:
  "I don't have enough information in the provided documents."
- Keep the answer clear, concise, and well-structured.
- If applicable, answer using bullet points or numbered lists.

Context:
{context}

Question:
{question}

Answer:
"""
        )