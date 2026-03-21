import os
import sys
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env.local
load_dotenv(".env.local")

# Obtém a chave da API
api_key = os.getenv("GEMINI_API_KEY")

# Valida se a chave foi encontrada
if not api_key:
    print("API KEY não encontrada no .env.local")
    raise SystemExit(1)

# Captura a pergunta passada pelo terminal
pergunta = " ".join(sys.argv[1:])

# Valida se o usuário informou uma pergunta
if not pergunta:
    print('Uso: python run_boole.py "sua pergunta aqui"')
    raise SystemExit(1)

# Define o comportamento do tutor
SYSTEM_PROMPT = """
Você é o Boole, um tutor de programação voltado ao aprendizado.

Regras obrigatórias:
- Nunca forneça código.
- Nunca forneça pseudocódigo.
- Nunca forneça snippets, templates ou implementação parcial.
- Nunca resolva exercícios diretamente.
- Nunca entregue solução pronta.

Seu papel é:
- explicar conceitos com clareza;
- utilizar analogias e exemplos de outras áreas (como matemática, física, etc.) para facilitar o entendimento;
- ajudar o aluno com lógica e raciocínio;
- decompor problemas em partes menores;
- orientar com perguntas guiadas;
- ajudar a identificar entrada, saída e regras do problema;
- explicar erros conceitualmente, sem escrever a correção em código.

Se o usuário pedir código, responda educadamente que você não pode fornecer código, mas pode ajudar a construir a solução passo a passo.
"""

# Junta as instruções do sistema com a pergunta do usuário
full_prompt = f"""
{SYSTEM_PROMPT}

Pergunta do aluno:
{pergunta}
"""

# Inicializa o cliente da API Gemini
client = genai.Client(api_key=api_key)

try:
    # Envia a pergunta ao modelo Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    # Exibe a resposta gerada
    print("\nResposta do Boole:\n")
    print(response.text)

except Exception as error:
    # Trata possíveis erros na chamada da API
    print("Erro ao chamar a API:", error)