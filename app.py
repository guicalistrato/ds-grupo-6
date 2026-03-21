import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv(".env.local")

# Obtém a chave da API
api_key = os.getenv("GEMINI_API_KEY")

# Valida se a chave existe
if not api_key:
    st.error("API KEY não encontrada no .env.local")
    st.stop()

# Inicializa cliente da API
client = genai.Client(api_key=api_key)

# Define comportamento do tutor
SYSTEM_PROMPT = """
Você é o Boole, um tutor de programação voltado ao aprendizado.

Regras obrigatórias:
- Nunca forneça código.
- Nunca forneça pseudocódigo.
- Nunca forneça snippets, templates ou implementação parcial.
- Nunca resolva exercícios diretamente.
- Nunca entregue solução pronta.
- Você pode analisar enunciados e trechos de código enviados pelo usuário, mas deve responder apenas de forma conceitual.

Seu papel é:
- explicar conceitos com clareza;
- utilizar analogias e exemplos de outras áreas para facilitar o entendimento;
- ajudar o aluno com lógica e raciocínio;
- decompor problemas em partes menores;
- orientar com perguntas guiadas;
- ajudar a identificar entrada, saída e regras do problema;
- explicar erros conceitualmente, sem escrever a correção em código.

Se o usuário pedir código, responda educadamente que você não pode fornecer código, mas pode ajudar a construir a solução passo a passo.
"""

# Detecta respostas que parecem código real
def contem_codigo(texto: str) -> bool:
    texto_lower = texto.lower()

    if "```" in texto_lower:
        return True

    padroes_fortes = [
        "def ",
        "class ",
        "return ",
        "print(",
        "while ",
        "for ",
        "if ",
        "else:",
        "elif ",
        "import ",
        "{",
        "}",
        ";"
    ]

    contador = sum(1 for p in padroes_fortes if p in texto_lower)
    return contador >= 3

# Interface
st.title("Boole - Tutor de Programação")
st.write("Este tutor ajuda você a resolver problemas com lógica e raciocínio, sem fornecer código pronto.")

pergunta = st.text_input("Digite sua pergunta:")

if st.button("Perguntar"):
    if pergunta.strip():
        full_prompt = f"""
{SYSTEM_PROMPT}

Pergunta do aluno:
{pergunta}
"""

        with st.spinner("Pensando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )

                resposta = response.text if hasattr(response, "text") else ""

                if not resposta:
                    st.warning("A API respondeu, mas não retornou texto.")
                elif contem_codigo(resposta):
                    st.subheader("Resposta:")
                    st.write("Não posso fornecer código, mas posso te ajudar a pensar na solução.")
                    st.write("Comece identificando qual é a entrada do problema, qual é a saída esperada e quais condições precisam ser verificadas para chegar ao resultado.")
                else:
                    st.subheader("Resposta:")
                    st.write(resposta)

            except Exception as error:
                st.error(f"Erro ao chamar a API: {error}")
    else:
        st.warning("Digite uma pergunta antes de enviar.")