import streamlit as st
import requests

st.title("Criador de Agentes IA (GRÁTIS)")

nome = st.text_input("Nome do agente")
funcao = st.text_area("Função do agente")
personalidade = st.text_area("Personalidade")
mensagem = st.text_input("Fale com seu agente")

if st.button("Conversar"):
    prompt = f"""
Você é {nome}.
Função: {funcao}
Personalidade: {personalidade}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt + "\nUsuário: " + mensagem,
            "stream": False
        }
    )

    st.write(response.json()["response"])
        