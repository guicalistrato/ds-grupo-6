import os
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env.local
load_dotenv(".env.local")

# Obtém a chave da API
api_key = os.getenv("GEMINI_API_KEY")

# Inicializa o cliente da API Gemini
client = genai.Client(api_key=api_key)

# Define um prompt fixo para teste da API
prompt = "Explique de forma simples a lógica para verificar se uma palavra é palíndromo. Não forneça código."

try:
    # Envia o prompt ao modelo Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Exibe a resposta gerada
    print("\nResposta da Gemini:\n")
    print(response.text)

except Exception as error:
    # Trata possíveis erros na chamada da API
    print("Erro ao chamar a API:", error)