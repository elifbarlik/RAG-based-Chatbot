# ingest.py
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# Konfigürasyon
PDF_PATH = os.getenv("PDF_PATH", "data/impact_of_generativeAI.pdf")
DB_DIR = os.getenv("CHROMA_DIR", "vectorstore")
EMBED_MODEL = os.getenv("EMBED_MODEL", "models/embedding-001")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# API anahtarı kontrolü
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable gerekli!")

# Veritabanı dizinini oluştur
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

print(f"PDF yükleniyor: {PDF_PATH}")
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

# Metni parçalara böl
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", " ", ""],
)
chunks = splitter.split_documents(docs)
print(f"Oluşturulan parça sayısı: {len(chunks)}")

# Gemini embedding modeli
embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBED_MODEL,
    google_api_key=GOOGLE_API_KEY
)

# ChromaDB'yi oluştur veya güncelle
print("Vector store oluşturuluyor...")
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_DIR,
)

# Değişiklikleri kaydet
vectordb.persist()
print("✅ İşlem tamamlandı → ChromaDB kaydedildi.")