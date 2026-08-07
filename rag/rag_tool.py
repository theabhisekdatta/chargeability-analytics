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
        self.QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
        self.QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.JINA_API_KEY = os.getenv("JINA_API_KEY")

        self.embed_model = None
        self.client = None
        self.vector_store = None
        self.retriever = None
        self.prompt = PromptTemplates.rag_prompt()
        self.llm = None
        self.rag_chain = None
        self._missing_config = None
        self._initialize_if_possible()

    def _initialize_if_possible(self):
        required = {
            "QDRANT_ENDPOINT": self.QDRANT_ENDPOINT,
            "QDRANT_API_KEY": self.QDRANT_API_KEY,
            "GROQ_API_KEY": self.GROQ_API_KEY,
            "JINA_API_KEY": self.JINA_API_KEY,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            self._missing_config = ", ".join(missing)
            return

        self.embed_model = JinaAPIEmbeddings(
            api_key=self.JINA_API_KEY,
            model="jina-embeddings-v3",
        )

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
            search_kwargs={"k": 1},
        )

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=self.GROQ_API_KEY,
            temperature=0,
        )

        self.rag_chain = (
            {
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
        )

    def _ensure_ready(self):
        if self._missing_config:
            raise RuntimeError(
                "Missing required RAG environment variables: "
                f"{self._missing_config}."
            )
        if self.retriever is None or self.rag_chain is None:
            raise RuntimeError("RAG tool failed to initialize.")

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, question: str):
        self._ensure_ready()
        docs = self.retriever.invoke(question)
        response = self.rag_chain.invoke(question)

        return {
            "question": question,
            "answer": response.content,
            "sources": [
                {
                    "metadata": doc.metadata,
                    "content": doc.page_content,
                }
                for doc in docs
            ],
        }