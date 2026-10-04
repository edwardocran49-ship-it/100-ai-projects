import streamlit as st
from portfolio_core.deployment import ollama_reply
st.title("Local Ollama Chat")
p=st.chat_input("Ask a question")
if p:st.chat_message("assistant").write(ollama_reply(p,False))
