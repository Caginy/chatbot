import streamlit as st
from chatbot import AsistanBeyni

st.set_page_config(page_title="AI Asistanım", page_icon="🤖")

st.title("🤖 Akıllı Asistan Paneli")
st.markdown("---")

@st.cache_resource
def asistan_yukle():
    return AsistanBeyni()

asistan = asistan_yukle()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        cevap = asistan.cevap_ver(prompt)
        st.markdown(cevap)
    st.session_state.messages.append({"role": "assistant", "content": cevap})
