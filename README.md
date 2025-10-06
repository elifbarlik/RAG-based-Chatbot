# PDF RAG Chatbot

Bu proje, PDF belgelerini analiz ederek sorulara yanıt veren bir RAG (Retrieval-Augmented Generation) chatbot uygulamasıdır. Google Gemini API ve LangChain kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- PDF belgelerini otomatik olarak işleme ve vektörleştirme
- Google Gemini API ile doğal dil işleme
- ChromaDB ile vektör veritabanı yönetimi
- FastAPI ile RESTful API
- Streamlit ile kullanıcı arayüzü
- Docker ile kolay dağıtım

## 📋 Gereksinimler

- Python 3.11+
- Google Gemini API anahtarı
- Docker (opsiyonel)

## 🛠️ Kurulum

### 1. Projeyi klonlayın
```bash
git clone <repository-url>
cd ChatBot
```

### 2. Sanal ortam oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Çevre değişkenlerini ayarlayın
`.env` dosyası oluşturun:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
EMBED_MODEL=models/embedding-001
LLM_MODEL=gemini-2.5-flash
CHROMA_DIR=vectorstore
TOP_K=4
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
PDF_PATH=data/impact_of_generativeAI.pdf
```

### 5. PDF'i işleyin
```bash
python ingest.py
```

### 6. Uygulamayı çalıştırın
```bash
# FastAPI backend
python app_gemini.py

# Streamlit frontend (yeni terminal)
streamlit run ui.py
```

## 🐳 Docker ile Çalıştırma

```bash
# Docker image oluştur
docker build -t pdf-rag-chatbot .

# Container çalıştır
docker run -p 8000:8000 -p 8501:8501 --env-file .env pdf-rag-chatbot
```

## 📖 API Kullanımı

### Health Check
```bash
GET http://localhost:8000/health
```

### Chat
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
    "question": "PDF'de ne anlatılıyor?"
}
```

## 🎯 Kullanım

1. Web arayüzüne `http://localhost:8501` adresinden erişin
2. PDF ile ilgili sorularınızı yazın
3. Bot, PDF içeriğine dayalı yanıtlar verecektir

## 📁 Proje Yapısı

```
ChatBot/
├── app_gemini.py          # FastAPI backend (Gemini)
├── app.py                 # FastAPI backend (Ollama)
├── ui.py                  # Streamlit frontend
├── ingest.py              # PDF işleme scripti
├── requirements.txt       # Python bağımlılıkları
├── Dockerfile            # Docker konfigürasyonu
├── .gitignore            # Git ignore dosyası
├── data/                 # PDF dosyaları
└── vectorstore/          # ChromaDB veritabanı
```

## 🔧 Konfigürasyon

- `TOP_K`: Her sorgu için döndürülecek maksimum kaynak sayısı
- `CHUNK_SIZE`: PDF metninin bölüneceği parça boyutu
- `CHUNK_OVERLAP`: Parçalar arasındaki örtüşme miktarı

## 📝 Notlar

- İlk çalıştırmada PDF işleme işlemi biraz zaman alabilir
- Google Gemini API kullanımı için geçerli bir API anahtarı gereklidir
- Vector store otomatik olarak `vectorstore/` dizininde saklanır
