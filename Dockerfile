# Python tabanlı imaj kullan
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Gerekli paketler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projeyi kopyala
COPY . .

# Portlar: FastAPI (8000) + Streamlit (8501)
EXPOSE 8000 8501

# Aynı anda hem FastAPI hem Streamlit çalıştır
CMD ["sh", "-c", "uvicorn app_gemini:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"]
