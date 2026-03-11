import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, EMBEDDING_MODEL, TOP_K

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(CHROMA_DB_PATH)
        self.collection = {
            "civil": self.client.get_or_create_collection(
                name="civil",
                metadata={"hnsw:space": "cosine"},
            ),
            "business": self.client.get_or_create_collection(
                name="business",
                metadata={"hnsw:space": "cosine"},
            ),
            "trade": self.client.get_or_create_collection(
                name="trade",
                metadata={"hnsw:space": "cosine"},
            ),
        }
        
    def search(self, query: str, top_k: int=TOP_K) -> list[dict]:
        embedding = self.model.encode([query]).tolist()
        retrieved=[]
        for _, collection in self.collection.items():
            results = collection.query(#query here is resp for searching relevant objects in out db 
            query_embeddings=embedding,
            n_results=top_k,
        )
            for i in range(len(results["documents"][0])):
                retrieved.append({
                    "section_id": results["metadatas"][0][i].get("section_id", "Unknown"),
                    "law_name": results["metadatas"][0][i].get("law_name", "Unknown"),
                    "chapter_id": results["metadatas"][0][i].get("chapter_id", ""),
                    "chapter_name": results["metadatas"][0][i].get("chapter_name", ""),
                    "text": results["documents"][0][i],
                    "distance": round(results["distances"][0][i], 4),
                })
        retrieved.sort(key=lambda x: x["distance"])
        return retrieved
    
    def _extract_keywords(self, query: str) -> list[str]:
        stop_words = {
            "what", "is", "the", "a", "an", "how", "do", "does", "can", "i",
            "to", "for", "of", "in", "and", "or", "my", "me", "if", "that",
            "this", "are", "be", "it", "on", "with", "as", "by", "at", "from",
            "was", "were", "been", "being", "have", "has", "had", "will",
            "would", "could", "should", "may", "might", "must", "shall",
            "about", "into", "through", "during", "before", "after", "above",
            "below", "between", "under", "again", "further", "then", "once",
            "there", "when", "where", "why", "which", "who", "whom",
            "need", "required", "specific", "word", "must", "included",
            "minimum", "number", "many", "much",
        }
        words = query.lower().split() #lowercase and separate words
        keywords = [w.strip("?.,!") for w in words if w.strip("?.,!") not in stop_words and len(w) > 2] #1 deleting punctuation marks(?.!,) -> saving word if its not in stop_words

        bigrams = []
        for i in range(len(keywords) - 1):
            bigrams.append(f"{keywords[i]} {keywords[i+1]}")

        return bigrams[:3] + keywords[:3]
    
    def smart_retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        main_result = self.search(query, top_k=top_k)
        seen_ids = {r["section_id"] for r in main_result}

        keywords = self._extract_keywords(query)
        for kw in keywords:
            extra = self.search(kw, top_k=2)
            for r in extra:
                if r["section_id"] not in seen_ids:
                    main_result.append(r)
                    seen_ids.add(r["section_id"])

        main_result.sort(key=lambda x: x["distance"])
        return main_result