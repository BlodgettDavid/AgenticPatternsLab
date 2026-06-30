import os
import logging
from typing import Optional
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext, 
    load_index_from_storage,
    Settings
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Set up clean logging telemetry
logger = logging.getLogger("AgenticLab.IndexManager")

class LocalIndexManager:
    def __init__(self, storage_dir: str = "./storage", embedding_model_name: str = "BAAI/bge-small-en-v1.5"):
        """
        Manages localized document indexing and vector store state persistence.
        """
        self.storage_dir = storage_dir
        self.embedding_model_name = embedding_model_name
        self._configure_settings()

    def _configure_settings(self):
        """
        Global configuration mapping for LlamaIndex components.
        Configures an highly optimized, small local HuggingFace embedder.
        """
        logger.info(f"Initializing local embedding layer: {self.embedding_model_name}")
        # BGE-small is tiny, accurate, fast, and runs entirely locally inside your environment
        Settings.embed_model = HuggingFaceEmbedding(model_name=self.embedding_model_name)
        
        # We leave Settings.llm unassigned here so our orchestrator 
        # can pass its resilient provider managers dynamically later.

    def build_or_load_index(self, data_dir: Optional[str] = None) -> VectorStoreIndex:
        """
        Checks if a persisted vector database index exists. If yes, reloads it instantly.
        If not, reads files from data_dir, creates embeddings, and saves them to disk.
        """
        if os.path.exists(self.storage_dir) and os.listdir(self.storage_dir):
            logger.info(f"Persisted storage index found at '{self.storage_dir}'. Loading state...")
            storage_context = StorageContext.from_defaults(persist_dir=self.storage_dir)
            index = load_index_from_storage(storage_context)
            return index
        
        # Fallback to ingestion if storage doesn't exist
        if not data_dir or not os.path.exists(data_dir):
            raise ValueError(f"No existing index found and data directory '{data_dir}' is unavailable.")

        logger.info(f"No existing index found. Ingesting source files from: {data_dir}")
        
        # Automatically handles directory loading for Markdown, Text, and Code files safely
        documents = SimpleDirectoryReader(input_dir=data_dir).load_data()
        logger.info(f"Successfully loaded {len(documents)} document source items.")

        # Construct vector architecture in memory, translating text to embeddings
        index = VectorStoreIndex.from_documents(documents)
        
        # Commit context vector matrices to disk immediately
        logger.info(f"Persisting vector records to local disk path: {self.storage_dir}")
        index.storage_context.persist(persist_dir=self.storage_dir)
        
        return index