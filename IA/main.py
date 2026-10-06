import os
from typing import Dict, List

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Sistema Jurídico IA",
    page_icon="⚖️",
    layout="wide",
)

load_dotenv()

MODELO = "openai/gpt-oss-120b"
LIMITE_PDF = 25_000
LIMITE_HISTORICO = 10


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1220;
        color: #e6edf7;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #f5c451;
    }

    .stChatMessage {
        background: #131c2e;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        border: 1px solid #1f2b45;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: #131c2e;
        color: #e6edf7;
        border: 1px solid #1f2b45;
    }

    section[data-testid="stSidebar"] {
        background: #0f1829;
        border-right: 1px solid #1f2b45;
    }

    .stButton > button {
        background: #f5c451;
        color: #0b1220;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        background: #ffd76b;
        color: #0b1220;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CLIENTE GROQ
# ============================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ A variável GROQ_API_KEY não foi encontrada. Crie um arquivo .env com: GROQ_API_KEY=sua_chave")
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def extrair_texto_pdf(arquivo) -> str:
    """Extrai o texto de um PDF carregado pelo usuário."""
    try:
        leitor = PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto += conteudo + "\n"
        return texto.strip()
    except Exception as e:
        st.error(f"Erro ao ler o PDF: {e}")
        return ""


def construir_contexto(documento: str, historico: List[Dict]) -> List[Dict]:
    """Monta a lista de mensagens enviadas ao modelo."""
    system_prompt = (
        "Você é um assistente jurídico especializado. "
        "Responda de forma técnica, clara e objetiva, sempre citando os dispositivos legais "
        "pertinentes quando possível. Se o usuário fornecer um documento, baseie suas "
        "respostas prioritariamente nele. Nunca invente artigos, súmulas ou jurisprudências."
    )

    mensagens: List[Dict] = [{"role": "system", "content": system_prompt}]

    if documento:
        contexto = documento[:LIMITE_PDF]
        mensagens.append(
            {
                "role": "system",
                "content": f"Documento fornecido pelo usuário:\n\n{contexto}",
            }
        )

    # Limita o histórico às últimas N mensagens
    mensagens.extend(historico[-LIMITE_HISTORICO:])

    return mensagens


def consultar_modelo(mensagens: List[Dict]) -> str:
    """Chama a API da Groq e retorna a resposta."""
    try:
        resposta = client.chat.completions.create(
            model=MODELO,
            messages=mensagens,
            temperature=0.3,
            max_tokens=2048,
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"❌ Erro ao consultar o modelo: {e}"


# ============================================================
# ESTADO DA SESSÃO
# ============================================================

if "historico" not in st.session_state:
    st.session_state.historico: List[Dict] = []

if "documento" not in st.session_state:
    st.session_state.documento: str = ""

if "nome_documento" not in st.session_state:
    st.session_state.nome_documento: str = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("⚖️ Sistema Jurídico IA")
    st.caption("Análise de documentos e consultas jurídicas com IA")

    st.divider()

    st.subheader("📄 Documento")
    arquivo_pdf = st.file_uploader(
        "Envie um PDF jurídico",
        type=["pdf"],
        accept_multiple_files=False,
    )

    if arquivo_pdf is not None:
        if arquivo_pdf.name != st.session_state.nome_documento:
            with st.spinner("Lendo PDF..."):
                texto = extrair_texto_pdf(arquivo_pdf)
                if texto:
                    st.session_state.documento = texto
                    st.session_state.nome_documento = arquivo_pdf.name
                    st.success(f"✅ {arquivo_pdf.name} carregado")
                else:
                    st.warning("Não foi possível extrair texto do PDF.")

    if st.session_state.documento:
        with st.expander("Prévia do documento"):
            st.text(st.session_state.documento[:1500] + "...")

        if st.button("🗑️ Remover documento"):
            st.session_state.documento = ""
            st.session_state.nome_documento = ""
            st.rerun()

    st.divider()

    if st.button("🧹 Limpar conversa"):
        st.session_state.historico = []
        st.rerun()

    st.divider()
    st.caption(f"Modelo: `{MODELO}`")
    st.caption(f"Histórico máximo: {LIMITE_HISTORICO} mensagens")


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

st.title("⚖️ Assistente Jurídico com IA")
st.caption(
    "Faça perguntas jurídicas ou envie um PDF (petição, contrato, sentença) "
    "para análise e esclarecimento de dúvidas."
)

# Exibe histórico
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Campo de entrada
pergunta = st.chat_input("Digite sua pergunta jurídica...")

if pergunta:
    # Mostra a pergunta do usuário
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Gera a resposta
    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            mensagens = construir_contexto(
                st.session_state.documento,
                st.session_state.historico,
            )
            resposta = consultar_modelo(mensagens)
            st.markdown(resposta)

    st.session_state.historico.append(
        {"role": "assistant", "content": resposta}
    )