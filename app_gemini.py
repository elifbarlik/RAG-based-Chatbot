# app_gemini.py
import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Gemini API konfigürasyonu
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
DB_DIR = os.getenv("CHROMA_DIR", "vectorstore")
TOP_K = int(os.getenv("TOP_K", 4))

app = FastAPI(title="PDF RAG Chatbot - Gemini", version="1.0")

# Vector store & retriever
emb = GoogleGenerativeAIEmbeddings(
    model=EMBED_MODEL,
    google_api_key=GOOGLE_API_KEY
)
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=emb)
retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})

# LLM - Gemini
llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

# Prompt (kaynakları düzenli gösteren, Türkçe odaklı)
SYSTEM = (
    "Sen bir teknik asistan ve RAG sohbet botusun. Cevaplarını SADE, doğru ve kaynaklı ver. "
    "Soruyla ilgili değilse kaynakları uydurma. Kararsızsan 'elimdeki metinde bu yok' de."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "Soru: {question}\n\nBağlam:\n{context}\n\nYanıtı Türkçe ver ve mümkünse madde madde açıkla.\n")
])

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True, output_key="answer"
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
    return_source_documents=True,
)

class ChatRequest(BaseModel):
    question: str

class Source(BaseModel):
    page: Optional[int]
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = chain.invoke({"question": req.question}) or {}
    answer = result.get("answer") or "Üzgünüm, şu an yanıt üretemedim."
    src_docs: List[Document] = result.get("source_documents", []) or []

    def page_of(doc: Document):
        meta = doc.metadata or {}
        p = meta.get("page")
        return (p + 1) if isinstance(p, int) else None

    sources = [
        Source(page=page_of(d), text=d.page_content[:800])
        for d in src_docs
    ]
    return ChatResponse(answer=answer, sources=sources)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
