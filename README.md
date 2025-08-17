# Agente IA RAG <img src="./images/profile.png" width="30px;" alt="Foto do Fabrício Vale"/><br>

## **Assistente Virtual com Base em Arquivo TXT (RAG)**
*Aplicação Web que funciona como um agente de IA, respondendo apenas perguntas relacionadas às informações de um arquivo TXT definido pelo usuário atrvés da tecnologia RAG (Retrieval-Augmented Generation).*

## Ferramentas:
<div style="display: inline_block">
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/-HuggingFace-FDEE21?style=for-the-badge&logo=HuggingFace&logoColor=black" />
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
</div>

## Instruções para rodar o projeto:
1. Clone o repositório
```
git clone https://github.com/fabriciovale20/agenteia-atendimento-simples.git
```

2. Acesse a pasta do projeto

3. Crie um ambiente virtual
```
python -m venv .venv
```

4. Ative o Virtualenv
```
.venv\Scripts\activate
```

5. Instale as dependências
```
pip install -r requirements.txt
```

6. Atualize o arquivo **base.txt** com as informações de interesse  
(O agente responderá apenas com base nesse conteúdo).

7. Instale o [Ollama](https://ollama.com/download/linux) no seu computador

8. Instale o LLM que será utilizado, por exemplo, `gemma3:1b`.<br>
*Obs.: Quanto melhor o LLM - mais parâmetros - melhor será o desempenho do agente.*

9. Execute a aplicação
```
streamlit run app.py
```

## ⚠️ Bug conhecido (PyTorch no Streamlit)
Caso apareça erro relacionado a `torch._classes` ou `fileWatcherType`, siga os passos:

1. Vá até a pasta:
```
C:\Users\\"seu-usuario"\\.streamlit\
```

2. Crie o arquivo `config.toml`
3. Insira nele:
```toml
[server]
fileWatcherType = "none"
```

<br>
<div style="display: inline_block">
<a href="https://portfolio-fabriciovale.vercel.app" target="_blank">
  <img src="https://img.shields.io/badge/-Portf%C3%B3lio-brown?style=for-the-badge&logo=true" target="_blank">
</a>
<a href="https://www.linkedin.com/in/fabrício-vale-6713b998/" target="_blank">
  <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank">
</a>
<a href="https://github.com/fabriciovale20" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank">
</a>
</div>
<br>
<br>

# Créditos
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/fabriciovale20">
        <img src="./images/photo-profile.png" width="100px;" alt="Foto do Fabrício Vale"/><br>
        <sub>
          <b>Fabrício Vale</b>
        </sub>
      </a>
    </td>
  </tr>
</table>