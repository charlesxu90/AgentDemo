# 

from src.deep_research.config.tools import SELECTED_RAG_PROVIDER, RAGProvider
from src.deep_research.rag.ragflow import RAGFlowProvider
from src.deep_research.rag.retriever import Retriever
from src.deep_research.rag.vikingdb_knowledge_base import VikingDBKnowledgeBaseProvider


def build_retriever() -> Retriever | None:
    if SELECTED_RAG_PROVIDER == RAGProvider.RAGFLOW.value:
        return RAGFlowProvider()
    elif SELECTED_RAG_PROVIDER == RAGProvider.VIKINGDB_KNOWLEDGE_BASE.value:
        return VikingDBKnowledgeBaseProvider()
    elif SELECTED_RAG_PROVIDER:
        raise ValueError(f"Unsupported RAG provider: {SELECTED_RAG_PROVIDER}")
    return None
