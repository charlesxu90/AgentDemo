# 

from src.deer_flow.config.tools import SELECTED_RAG_PROVIDER, RAGProvider
from src.deer_flow.rag.ragflow import RAGFlowProvider
from src.deer_flow.rag.retriever import Retriever
from src.deer_flow.rag.vikingdb_knowledge_base import VikingDBKnowledgeBaseProvider


def build_retriever() -> Retriever | None:
    if SELECTED_RAG_PROVIDER == RAGProvider.RAGFLOW.value:
        return RAGFlowProvider()
    elif SELECTED_RAG_PROVIDER == RAGProvider.VIKINGDB_KNOWLEDGE_BASE.value:
        return VikingDBKnowledgeBaseProvider()
    elif SELECTED_RAG_PROVIDER:
        raise ValueError(f"Unsupported RAG provider: {SELECTED_RAG_PROVIDER}")
    return None
