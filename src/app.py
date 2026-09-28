import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
from dotenv import load_dotenv

#carrega a chave de API 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

#Configuração do streamlit
st.set_page_config(page_title="Lumi - Assistente Financeira", page_icon="🤖")
st.title("🤖 Lumi - Atendimento de Cartões")
st.caption("Sua assistente inteligente para faturas, limites e contestações.")

#carregamento de dados mockados
@st.cache_data
def carregar_dados():
    try:
        df_transacoes = pd.read_csv("../data/transacoes.csv")
        df_historico = pd.read_csv("../data/historico_atendimento.csv")
        with open("../data/perfil_cliente.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)
        with open("../data/regras_cartao.json", "r", encoding="utf-8") as f:
            regras = json.load(f)
        
        contexto_dados = f"""
        [DADOS DO CLIENTE]
        {json.dumps(perfil, ensure_ascii=False, indent=2)}
        
        [TRANSAÇÕES DA FATURA ATUAL]
        {df_transacoes.to_string(index=False)}
        
        [HISTÓRICO DE ATENDIMENTO]
        {df_historico.to_string(index=False)}
        
        [REGRAS DE NEGÓCIO DO BANCO]
        {json.dumps(regras, ensure_ascii=False, indent=2)}
        """
        return contexto_dados
    except Exception as e:
        st.error(f"Erro ao carregar dados. Verifique a pasta 'data'. Erro: {e}")
        return ""

#carrega os dados para o contexto
contexto = carregar_dados()

system_prompt = f"""
Você é a Lumi, uma agente financeira inteligente especializada em atendimento de faturas, limites e contestação de cartão de crédito.
Sua personalidade é simpática e resolutiva. Você é paciente e amigável, porém direta e focada em transmitir segurança ao cliente.

SEU OBJETIVO: 
Ajudar os clientes a entenderem suas faturas, tirar dúvidas sobre o cartão e auxiliar em processos de contestação, utilizando EXCLUSIVAMENTE os dados abaixo.

CONTEXTO DE DADOS (BASE DE CONHECIMENTO):
{contexto}

REGRAS ESTABELECIDAS:
1. Baseie-se APENAS no contexto de dados acima.
2. NUNCA invente transações, valores, datas ou regras que não estejam no contexto.
3. Se o cliente relatar uma fraude, oriente-o imediatamente sobre o bloqueio preventivo do cartão.
4. NUNCA solicite dados sensíveis como senha do cartão ou CVV.
5. Se não souber responder, informe de maneira educada que irá transferir para um especialista humano.
"""

#inicialização do modelo Gemini
modelo = genai.GenerativeModel(
    model_name="gemini-3.8-flash", 
    system_instruction=system_prompt
)

#gerencia o histórico do chat na sessão do Streamlit
if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = modelo.start_chat(history=[])

#mostra as mensagens antigas na tela
for msg in st.session_state.chat_session.history:
    role = "user" if msg.role == "user" else "assistant"
    st.chat_message(role).write(msg.parts[0].text)

#captura a nova mensagem do usuário
if prompt := st.chat_input("Como posso ajudar com seu cartão hoje?"):
    st.chat_message("user").write(prompt)
    
    #envia para o Gemini e exibe a resposta
    with st.spinner("Lumi está digitando..."):
        response = st.session_state.chat_session.send_message(prompt)
        st.chat_message("assistant").write(response.text)