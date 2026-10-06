# ⚖️ Sistema Jurídico IA

Assistente jurídico desenvolvido em **Python + Streamlit**, utilizando a API da **Groq** e o modelo `openai/gpt-oss-120b`.

A aplicação permite realizar consultas jurídicas por meio de uma interface de chat e também enviar documentos em PDF, como petições, contratos e sentenças, para que a IA utilize o conteúdo do documento como contexto durante a análise.

> ⚠️ **Aviso:** este projeto possui finalidade educacional e de apoio à análise de informações. As respostas geradas por IA não substituem a análise de um advogado ou profissional jurídico habilitado.

---

## 📋 Funcionalidades

- 💬 Chat jurídico com inteligência artificial
- 📄 Upload de documentos em PDF
- 🔎 Extração automática de texto dos PDFs
- ⚖️ Análise de documentos jurídicos
- 🧠 Uso do documento enviado como contexto para as respostas
- 🗂️ Histórico de conversas durante a sessão
- 🧹 Limpeza do histórico da conversa
- 🗑️ Remoção do documento carregado
- 👀 Pré-visualização do conteúdo do PDF
- 🎨 Interface personalizada em tema escuro
- 🔐 Uso de variável de ambiente para armazenar a chave da API

---

## 🖥️ Visão geral

O sistema possui duas áreas principais:

### Sidebar

Na barra lateral é possível:

- Enviar um documento PDF;
- Visualizar uma prévia do documento;
- Remover o documento;
- Limpar a conversa;
- Visualizar o modelo utilizado;
- Visualizar o limite de histórico configurado.

### Área principal

Na área principal estão disponíveis:

- Interface de chat;
- Campo para perguntas jurídicas;
- Histórico da conversa;
- Respostas geradas pela inteligência artificial.

---

## 🏗️ Arquitetura

```text
┌──────────────────────┐
│       Usuário        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Streamlit       │
│    Interface Web     │
└──────────┬───────────┘
           │
           ├──────────────► Pergunta jurídica
           │
           ▼
┌──────────────────────┐
│   Documento PDF?     │
└──────────┬───────────┘
           │
       Sim │
           ▼
┌──────────────────────┐
│        pypdf         │
│ Extração do conteúdo │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Construção do        │
│ contexto da conversa │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      API Groq        │
│  openai/gpt-oss-120b │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Resposta jurídica   │
│    gerada pela IA    │
└──────────────────────┘
