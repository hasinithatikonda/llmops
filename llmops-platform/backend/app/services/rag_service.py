from typing import List
from PyPDF2 import PdfReader
from app.services.chroma_service import chroma_service
from app.services.groq_service import groq_service
import io

class RAGService:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def process_pdf(self, file_content: bytes, filename: str) -> dict:
        """Process PDF and store in ChromaDB"""
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            documents = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                chunks = self.chunk_text(text)
                
                for chunk in chunks:
                    documents.append({
                        "text": chunk,
                        "source": filename,
                        "page": page_num + 1
                    })
            
            chroma_service.add_documents(documents)
            
            return {
                "success": True,
                "pages": len(reader.pages),
                "chunks": len(documents),
                "filename": filename
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def query_with_context(self, query: str, n_results: int = 3) -> dict:
        """Query with RAG context"""
        # Retrieve relevant documents
        documents = chroma_service.query_documents(query, n_results)
        
        # Build context
        context = "\n\n".join([doc["text"] for doc in documents])
        
        # Create enhanced prompt
        enhanced_prompt = f"""Context information:
{context}

User question: {query}

Please answer the question based on the context provided. If the context doesn't contain relevant information, say so."""
        
        # Generate response
        response = groq_service.generate_completion(enhanced_prompt)
        
        return {
            "response": response,
            "context": documents,
            "query": query
        }

rag_service = RAGService()
