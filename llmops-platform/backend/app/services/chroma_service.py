import chromadb
from chromadb.config import Settings
from typing import List, Dict
from app.core.config import settings
import hashlib

class ChromaService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name="llmops_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to ChromaDB"""
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            doc_id = hashlib.md5(doc["text"].encode()).hexdigest()
            ids.append(doc_id)
            texts.append(doc["text"])
            metadatas.append({
                "source": doc.get("source", "unknown"),
                "page": doc.get("page", 0)
            })
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """Query similar documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        documents = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "text": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0
                })
        
        return documents
    
    def delete_collection(self):
        """Delete the collection"""
        self.client.delete_collection(name="llmops_documents")

chroma_service = ChromaService()
