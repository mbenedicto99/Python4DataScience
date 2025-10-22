import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class AdvancedkNN_RAG:
    def __init__(self, k=5, model_name='all-MiniLM-L6-v2'):
        self.k = k
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.metadata = []
        
    def add_documents(self, documents: List[str], metadata: List[dict] = None):
        """Adiciona documentos com metadados opcionais"""
        self.documents.extend(documents)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(documents))
            
        # Atualiza embeddings
        embeddings = self.model.encode(documents)
        
        if self.index is None:
            # Cria índice pela primeira vez
            self.index = faiss.IndexFlatIP(embeddings.shape[1])  # Similaridade cosseno
            
        # Normaliza para similaridade cosseno
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
        
    def hybrid_retrieve(self, query: str, k: int = None, score_threshold: float = 0.7):
        """Recuperação híbrida com limiar de score"""
        if k is None:
            k = self.k
            
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Busca com k maior para filtrar depois
        scores, indices = self.index.search(query_embedding.astype('float32'), k * 2)
        
        # Filtra por limiar de similaridade
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= score_threshold and idx < len(self.documents):
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': float(score)
                })
                
        return results[:k]  # Retorna apenas os k melhores
    
    def generate_context(self, retrieved_results: List[dict]) -> str:
        """Gera contexto para o LLM baseado nos resultados"""
        context_parts = []
        
        for i, result in enumerate(retrieved_results):
            doc = result['document']
            score = result['score']
            context_parts.append(f"[Documento {i+1} - Similaridade: {score:.3f}]\n{doc}")
            
        return "\n\n".join(context_parts)

# Exemplo de uso com dados mais complexos
rag_advanced = AdvancedkNN_RAG(k=3)

# Documentos com metadados
knowledge_base = [
    {
        "content": "kNN é um algoritmo de machine learning usado para classificação e regressão",
        "metadata": {"topic": "machine learning", "type": "algorithm"}
    },
    {
        "content": "RAG systems improve AI responses by retrieving relevant information",
        "metadata": {"topic": "AI", "type": "architecture"}
    },
    {
        "content": "Python scikit-learn provides kNN implementation with various metrics",
        "metadata": {"topic": "programming", "type": "library"}
    },
    {
        "content": "Embeddings transform text into numerical vectors for similarity search",
        "metadata": {"topic": "NLP", "type": "technique"}
    }
]

# Adiciona documentos ao sistema
for item in knowledge_base:
    rag_advanced.add_documents(
        [item["content"]], 
        [item["metadata"]]
    )

# Consulta
query = "Como funciona kNN no machine learning?"
results = rag_advanced.hybrid_retrieve(query, score_threshold=0.6)

print(f"Consulta: {query}")
print(f"\nEncontrados {len(results)} documentos relevantes:\n")

for i, result in enumerate(results):
    print(f"Documento {i+1}:")
    print(f"  Conteúdo: {result['document']}")
    print(f"  Metadados: {result['metadata']}")
    print(f"  Score: {result['score']:.3f}")
    print()

# Gera contexto para LLM
context = rag_advanced.generate_context(results)
print("Contexto para LLM:")
print(context)
