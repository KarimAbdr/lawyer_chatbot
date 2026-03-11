from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT

class Generator:
    def __init__(self):
        self.client=genai.Client(api_key=GEMINI_API_KEY)
        self.model=GEMINI_MODEL

    def generate(self, query: str, context_chunks: list[dict]) -> str:
        context = ""
        for c in context_chunks:
            law = c.get("law_name", "Unknown")
            section = c.get("section_id", "Unknown")
            chapter = c.get("chapter_id", "")
            label = f"{law} — {chapter}, {section}" if chapter else f"{law} — {section}"
            context += f"\n[{label}]\n{c['text']}\n"

        prompt = f"""{SYSTEM_PROMPT}

LEGAL EXCERPTS:
{context}

USER QUESTION: {query}"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
