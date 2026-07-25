import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough

from rag.embedding import JinaAPIEmbeddings
from rag.prompt import PromptTemplates

load_dotenv()


class RAGTool:

    def __init__(self):
        # Environment
        self.QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.JINA_API_KEY = os.getenv("JINA_API_KEY")

        # Embeddings
        self.embed_model = JinaAPIEmbeddings(
            api_key=self.JINA_API_KEY,
            model="jina-embeddings-v3"
        )

        # Qdrant
        self.client = QdrantClient(
            url=self.QDRANT_ENDPOINT,
            api_key=self.QDRANT_API_KEY,
        )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name="chargeability_analytics_db",
            embedding=self.embed_model,
        )

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        # Prompt
        self.prompt = PromptTemplates.rag_prompt()

        # LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.GROQ_API_KEY,
            temperature=0
        )

        # Chain
        self.rag_chain = (
            {
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
        )

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, question: str):
        docs = self.retriever.invoke(question)

        response = self.rag_chain.invoke(question)

        return {
            "question": question,
            "answer": response.content,
            "sources": [
                {
                    "metadata": doc.metadata,
                    "content": doc.page_content
                }
                for doc in docs
            ]
        }