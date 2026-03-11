from src.rag.retriever import Retriever
from src.rag.generator import Generator


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, question: str, use_smart_retrieval: bool = True) -> dict:
        if use_smart_retrieval:
            sources = self.retriever.smart_retrieve(question)
        else:
            sources = self.retriever.search(question)

        answer = self.generator.generate(question, sources)

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "section_id": s["section_id"],
                    "law_name": s["law_name"],
                    "chapter_id": s.get("chapter_id", ""),
                    "text": s["text"][:200] + "..." if len(s["text"]) > 200 else s["text"],
                    "distance": s["distance"],
                }
                for s in sources
            ],
        }
