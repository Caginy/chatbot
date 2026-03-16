import streamlit as st
from chatbot import AsistanBeyni

# Sayfa Ayarları
st.set_page_config(page_title="AI Asistanım", page_icon="🤖")

st.title("🤖 Veri Madenciliği Ödevi: Akıllı Asistan")
st.markdown("---")

# Asistanın beynini yükleyelim
@st.cache_resource
def asistan_yukle():
    return AsistanBeyni()

asistan = asistan_yukle()

# Sohbet geçmişini saklamak için
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Mesajınızı yazın..."):
    # Kullanıcı mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Asistandan cevap al
    with st.chat_message("assistant"):
        cevap = asistan.cevap_ver(prompt)
        st.markdown(cevap)
    
    # Cevabı geçmişe kaydet
    st.session_state.messages.append({"role": "assistant", "content": cevap})