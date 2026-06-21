import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega chaves de ambiente
load_dotenv()

# Configura o título da página web no navegador
st.set_page_config(page_title="Jarvis Chat", page_icon="🤖")

# Inicializa o cliente Gemini usando uma função do Streamlit para não refazer o login toda hora
@st.cache_resource
def obter_cliente_gemini():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = obter_cliente_gemini()
NOME_CHATBOT = "Jarvis"

# ---------------------------------------------------------------------
# FASE 1: TELA DE LOGIN (PEDIR O NOME)
# ---------------------------------------------------------------------
if "nome_usuario" not in st.session_state:
    st.title("🤖 Bem-vindo ao Sistema")
    nome_digitado = st.text_input("Por favor, digite o seu nome para iniciar:")
    
    if st.button("Entrar no Chat"):
        if nome_digitado.strip():
            st.session_state.nome_usuario = nome_digitado.strip()
            # Reinicia a página para carregar o chat
            st.rerun()
        else:
            st.warning("Por favor, insira um nome válido.")
            
# ---------------------------------------------------------------------
# FASE 2: TELA DO CHAT
# ---------------------------------------------------------------------
else:
    nome_usuario = st.session_state.nome_usuario
    st.title(f"Conversando com {NOME_CHATBOT}")
    st.write(f"Usuário ativo: **{nome_usuario}**")

    # Configura a Persona e a Sessão de Chat na memória do navegador
    if "chat_session" not in st.session_state:
        persona = (
            f"Você é o {NOME_CHATBOT}, um assistente de inteligência artificial sarcástico, "
            f"mas extremamente inteligente e prestativo. Você está conversando com {nome_usuario}. "
            f"Use respostas concisas."
        )
        config = types.GenerateContentConfig(
            system_instruction=persona,
            max_output_tokens=150
        )
        # Cria o chat e guarda na sessão para não perder o histórico
        st.session_state.chat_session = client.chats.create(
            model="gemini-1.5-flash",
            config=config
        )
        # Lista para mostrar as mensagens na tela
        st.session_state.mensagens = []
        
        # Gera a mensagem de boas-vindas automática
        with st.spinner("Conectando com o Jarvis..."):
            resposta_inicial = st.session_state.chat_session.send_message(
                f"Se apresente para o {nome_usuario} de forma curta e sarcástica."
            )
            st.session_state.mensagens.append({"autor": NOME_CHATBOT, "texto": resposta_inicial.text})

    # Renderiza o histórico de mensagens na tela com o visual nativo de chat do Streamlit
    for msg in st.session_state.mensagens:
        avatar = "🤖" if msg["autor"] == NOME_CHATBOT else "👤"
        with st.chat_message(msg["autor"], avatar=avatar):
            st.write(msg["texto"])

    # Campo de texto para o usuário digitar a mensagem (fica fixo no rodapé automaticamente)
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        
        # Mostra a mensagem do usuário na tela imediatamente
        with st.chat_message(nome_usuario, avatar="👤"):
            st.write(prompt)
        st.session_state.mensagens.append({"autor": nome_usuario, "texto": prompt})

        # Envia para o Gemini e mostra a resposta com efeito de carregamento
        with st.chat_message(NOME_CHATBOT, avatar="🤖"):
            with st.spinner("Pensando..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    st.write(response.text)
                    st.session_state.mensagens.append({"autor": NOME_CHATBOT, "texto": response.text})
                except Exception as e:
                    st.error(f"Erro ao falar com o Gemini: {e}")


