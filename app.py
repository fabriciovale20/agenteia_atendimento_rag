import os
import base64
import warnings
import streamlit as st
import ollama

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)

# ========= CONFIGURAÇÕES =========
PASTA_BASE = "base_conhecimento" # Nome da pasta da base de conhecimento
FAISS_PATH = "faiss_index"
MODELO_EMBEDDING = "all-MiniLM-L6-v2"
MODELO_LLM = "gemma3:1b" # Modelo de Linguagem
IMG_PATH = "images/profile.png" # Imagem do Agente

# ========= INTERFACE =========
st.set_page_config(page_title="Agende IA - Fabrício Vale", layout="centered")

def imagem_base64(caminho):
    with open(caminho, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

if os.path.exists(IMG_PATH):
    img_base64 = imagem_base64(IMG_PATH)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{img_base64}" width="100" style="border-radius: 50%;">
            </div>
            """,
            unsafe_allow_html=True
        )

st.title("🤖 Agente IA - Fabrício Vale")

# ========= HISTÓRICO =========
for chave in ["historico", "carregando", "pergunta_enviada", "responder", "input_text", "limpar_input"]:
    if chave not in st.session_state:
        st.session_state[chave] = [] if chave == "historico" else False if "carregando" in chave or "responder" in chave or "limpar" in chave else ""

# ========= CARREGA BASE E MODELOS =========
@st.cache_resource
def setup_base():
    embeddings = HuggingFaceEmbeddings(model_name=MODELO_EMBEDDING)

    if os.path.exists(FAISS_PATH):
        vectorstore = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        if not os.path.exists(PASTA_BASE):
            raise FileNotFoundError(f"A pasta '{PASTA_BASE}' não existe.")

        arquivos_txt = [f for f in os.listdir(PASTA_BASE) if f.endswith(".txt")]
        if not arquivos_txt:
            raise FileNotFoundError(f"Nenhum arquivo .txt encontrado em '{PASTA_BASE}'.")

        documentos = []
        for nome in arquivos_txt:
            caminho = os.path.join(PASTA_BASE, nome)
            loader = TextLoader(caminho, encoding="utf-8")
            documentos.extend(loader.load())

        vectorstore = FAISS.from_documents(documentos, embeddings)
        vectorstore.save_local(FAISS_PATH)

    retriever = vectorstore.as_retriever()
    llm = OllamaLLM(model=MODELO_LLM, temperature=0)
    llm.invoke("Olá")

    return retriever, llm, vectorstore  # <-- removido 'documentos'


try:
    retriever, llm, vectorstore = setup_base()
except Exception as e:
    st.error(f"Erro ao carregar base: {e}")
    st.stop()

# ========= GERA RESPOSTA =========
def gerar_resposta(pergunta):
    docs_similares = vectorstore.similarity_search(pergunta, k=5) # K é o número de documentos similares a serem recolhidos
    contexto = "\n".join([doc.page_content for doc in docs_similares])

    prompt = f"""
# Prompt Mestre - Agente de IA (Secretário Pessoal)

Você é um **Agente de IA** que atua como **secretário pessoal digital** de qualquer pessoa cujas informações estão contidas em um **arquivo TXT fornecido**.  
Sua única fonte de conhecimento é o **arquivo TXT**, que contém informações estruturadas sobre a pessoa.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}


## EXEMPLOS DE COMPORTAMENTO:

- Pergunta: *"Quem é você?"*  
  Resposta:  
  "**Eu sou [NOME DA PESSOA], conforme descrito no arquivo fornecido.**"

- Pergunta: *"Quais são suas experiências profissionais?"*  
  Resposta:  
  "**Experiência de [NOME DA PESSOA]:**  
   - (Listar conforme consta no arquivo TXT)"  

- Pergunta: *"Você fala inglês?"*  
  Resposta:  
  "**Sim, [NOME DA PESSOA] possui o nível de inglês conforme informado no arquivo TXT.**"

- Pergunta: *"Qual seu LinkedIn?"*  
  Resposta:  
  "**LinkedIn de [NOME DA PESSOA]:** (informação conforme arquivo TXT)"

---

## OBJETIVO FINAL
Atuar como **secretário digital da pessoa descrita no arquivo TXT**, respondendo perguntas de forma precisa, confiável e baseada **exclusivamente no conteúdo do arquivo fornecido**.
"""


    try:
        response = ollama.generate(
            model=MODELO_LLM,
            prompt=prompt,
            stream=False,
            options={
                "temperature": 0.0,
                "num_ctx": 4096,        # reduz o número de tokens de contexto
                "num_thread": 8         # controla melhor o uso de CPU
            }
        )
        return response['response'].strip()
    except Exception as e:
        st.error(f"Erro ao comunicar com o modelo: {e}")
        return "Ocorreu um erro ao tentar gerar a resposta."

# ========= EXIBE CONVERSA =========
with st.container():
    for entrada in st.session_state.historico:
        st.markdown(f"**🧑‍💻 Pergunta:** {entrada['pergunta']}")
        st.markdown(f"**🤖 Agente IA:** {entrada['resposta']}")
        st.markdown("---")

# ========= ENVIA PERGUNTA =========
def enviar_pergunta():
    if st.session_state.input_text.strip():
        st.session_state.pergunta_enviada = st.session_state.input_text
        st.session_state.carregando = True
        st.session_state.responder = True
        st.session_state.limpar_input = False

# ========= INPUT DE PERGUNTA =========
if st.session_state.limpar_input:
    st.session_state.input_text = ""
    st.session_state.limpar_input = False

st.text_input(
    "Digite sua pergunta:",
    placeholder="Ex: Qual seu nome?",
    key="input_text",
    disabled=st.session_state.carregando,
    on_change=enviar_pergunta
)

col_esq, col_meio, col_dir = st.columns([1, 2, 1])

with col_esq:
    st.button("Perguntar", on_click=enviar_pergunta, disabled=st.session_state.carregando)

# ========= PROCESSA RESPOSTA =========
if st.session_state.responder:
    # Captura o momento atual 🟡
    hora_pergunta = datetime.now()
    # Formata a data e a hora no formato desejado 🟡
    data_pergunta = hora_pergunta.strftime("%d/%m/%Y %H:%M:%S")
    print(f'Pergunta: {data_pergunta}')
    with st.spinner("Pnsando..."):
        resposta = gerar_resposta(st.session_state.pergunta_enviada)
        hora_resposta = datetime.now()
        data_resposta = hora_resposta.strftime("%d/%m/%Y %H:%M:%S")
        print(f'Resposta: {data_resposta}')

        # Calcular tempo de resposta
        formato = "%d/%m/%Y %H:%M:%S"
        data_pergunta_dt = datetime.strptime(data_pergunta, formato)
        data_resposta_dt = datetime.strptime(data_resposta, formato)
        diferenca = data_resposta_dt - data_pergunta_dt
        segundos = int(diferenca.total_seconds())

        # Adiciona resposta com tempo ao histórico
        # resposta_com_tempo = f"{resposta}\n\n⏱️ Tempo de resposta: {segundos} segundos"
        resposta_com_tempo = f'{resposta}'
        st.session_state.historico.append({
            "pergunta": st.session_state.pergunta_enviada,
            "resposta": resposta_com_tempo
    })

    st.session_state.pergunta_enviada = ""
    st.session_state.carregando = False
    st.session_state.responder = False
    st.session_state.limpar_input = True
    # Captura o momento atual 🟡
    hora_resposta = datetime.now()
    # Formata a data e a hora no formato desejado 🟡
    data_resposta = hora_resposta.strftime("%d/%m/%Y %H:%M:%S")
    print(f'Resposta: {data_resposta}')
    
    # Converter strings para objetos datetime
    formato = "%d/%m/%Y %H:%M:%S"
    
    data_pergunta = datetime.strptime(data_pergunta, formato)
    data_resposta = datetime.strptime(data_resposta, formato)
        
    # Calcular a diferença
    diferenca = data_resposta - data_pergunta

    # Obter a diferença em segundos e minutos
    segundos = int(diferenca.total_seconds())
    minutos = diferenca.total_seconds() / 60

    print(f"Temp de resposta: {segundos} segundos ({minutos:.2f} minutos)")
    st.rerun()