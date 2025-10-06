# ui.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="PDF RAG Chatbot", page_icon="🤖", layout="wide")

st.title("📄 PDF RAG Chatbot (Gemini + LangChain + ChromaDB)")

# Session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sohbet geçmişini göster
for msg in st.session_state["messages"]:
    role, content = msg
    with st.chat_message(role):
        st.markdown(content)

# Kullanıcıdan input
if prompt := st.chat_input("Sorunuzu yazın..."):

    st.session_state["messages"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # API çağrısı
    try:
        resp = requests.post(API_URL, json={"question": prompt})
        data = resp.json()

        answer = data.get("answer", "⚠️ Yanıt alınamadı.")
        sources = data.get("sources", [])

        # Cevap yazdır
        with st.chat_message("assistant"):
            st.markdown(answer)

            if sources:
                st.markdown("**📚 Kaynaklar:**")
                for s in sources:
                    page = s.get("page", "?")
                    text = s.get("text", "")[:200].replace("\n", " ")
                    st.markdown(f"- Sayfa {page}: {text}...")

        st.session_state["messages"].append(("assistant", answer))
    except Exception as e:
        st.error(f"API hatası: {e}")
        st.write("DEBUG:", resp.status_code, resp.text)

