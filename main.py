#Para rodar este código, certifique-se de ter as seguintes dependências instaladas:
# - google-genai (para interagir com a API Gemini)
# - python-dotenv (para carregar as variáveis de ambiente do arquivo .env)
# - Flask (opcional, caso queira criar uma interface web)
# - Streamlit (opcional, para uma interface web mais simples)

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa o cliente
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =====================================================================
# CONFIGURAÇÃO DA PERSONA E IDENTIDADES
# =====================================================================
# Perguntar o nome do usuário assim que o programa começa
print("--- Inicializando o Sistema ---")
NOME_USUARIO = input("Por favor, digite o seu nome: ").strip()

# Caso a pessoa dê apenas "Enter" sem digitar nada, definimos um nome padrão
if not NOME_USUARIO:
    NOME_USUARIO = "Usuário"

# A Persona agora pode usar o nome do usuário dinamicamente!
PERSONA = (
    f"Você é o Jarvis, um assistente de inteligência artificial sarcástico, "
    f"mas extremamente inteligente e prestativo. Você está conversando com {NOME_USUARIO}. "
    f"Use respostas concisas."
)

NOME_CHATBOT = "Jarvis"
# =====================================================================

# Configura as opções do chat
config = types.GenerateContentConfig(
    system_instruction=PERSONA,
    max_output_tokens=500
)

# Inicia a sessão de chat
chat = client.chats.create(
    model="gemini-1.5-flash",
    config=config
)

print(f"\n--- Chat Iniciado com {NOME_CHATBOT} (Digite 'sair' para encerrar) ---")

# Mensagem de boas-vindas automática do Jarvis sabendo quem é o usuário
try:
    primeiro_contato = chat.send_message(f"Se apresente para o {NOME_USUARIO} de forma curta.")
    print(f"{NOME_CHATBOT}: {primeiro_contato.text}")
except Exception as e:
    print(f"\n[Erro ao iniciar]: {e}")

# Loop de conversa contínua
while True:
    # Captura a entrada do usuário usando o nome que ele digitou
    texto_usuario = input(f"\n{NOME_USUARIO}: ")
    
    # Condição de parada
    if texto_usuario.lower() in ["sair", "exit", "tchau", "parar"]:
        print(f"\n{NOME_CHATBOT}: Até logo, {NOME_USUARIO}!")
        break
        
    # Garante que o usuário não enviou uma mensagem vazia
    if not texto_usuario.strip():
        continue
        
    try:
        # Envia a mensagem e recebe a resposta mantendo o histórico
        response = chat.send_message(texto_usuario)
        print(f"{NOME_CHATBOT}: {response.text}")
    except Exception as e:
        print(f"\n[Erro ao se comunicar com o Gemini]: {e}")