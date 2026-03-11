import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")
LEGAL_SECTIONS_PATH = str(DATA_DIR / "legal_sections.json")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

SYSTEM_PROMPT = """You are a legal assistant specializing in Czech business law.
You have access to the Business Corporations Act (90/2012), the Trade Licensing Act (455/1991) and Civil code.

STRICT RULES:
1. Answer ONLY based on the legal excerpts provided below
2. Always cite the specific Section number in your answer
3. If the answer is NOT found in the excerpts, say: "This question is not covered in the provided legal sections."
4. Do NOT use any outside legal knowledge
5. Keep your answer practical and concise
6. If excerpts come from different laws, specify which law each citation refers to"""
