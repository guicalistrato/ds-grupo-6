# Boole

## Descrição

Boole é um projeto inicial de integração com a API do modelo de linguagem Gemini. O objetivo desta etapa do projeto foi validar a comunicação entre um sistema local e um modelo de linguagem, criando um protótipo capaz de enviar perguntas e receber respostas geradas pela API.

O sistema permite enviar perguntas e receber respostas geradas pela API, funcionando como um protótipo inicial de um tutor inteligente para apoio ao estudo de programação.

Um dos diferenciais do Boole é sua abordagem pedagógica: o sistema não fornece código ou soluções prontas, mas auxilia o usuário no desenvolvimento do raciocínio lógico e na compreensão dos problemas.

Essa integração será utilizada posteriormente no desenvolvimento de um sistema de recomendação voltado ao aprendizado de programação.

Nesta fase do projeto foram implementadas duas funcionalidades principais:

- teste de chamadas básicas da API com exemplos fixos;
- criação de um código mínimo funcional que gera respostas utilizando a API.
- interface web simples utilizando Streamlit (extensão complementar).

---

## Estrutura do projeto

```text
boole/
├── docs/
│   ├── entregas.md
│   └── requisitos.md
├── .env.local
├── .gitignore
├── app.py
├── run_boole.py
├── test_boole.py
├── requirements.txt
└── README.md
```

---

## Tecnologias utilizadas

- Python
- API Gemini
- biblioteca `google-genai`
- biblioteca `python-dotenv`
- Streamlit

---

## Como executar o projeto

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Criar arquivo `.env.local`

Criar um arquivo `.env.local` na raiz do projeto contendo a chave da API:

```env
GEMINI_API_KEY=sua_chave_aqui
```

### 3. Testar chamada básica da API

```bash
python test_boole.py
```

Esse script envia um prompt fixo para a API e imprime a resposta no terminal.

### 4. Executar o script funcional

```bash
python run_boole.py "Explique o que é um algoritmo"
```

Esse script recebe uma pergunta informada pelo usuário e retorna uma resposta gerada pelo modelo.

---

### 5. Executar interface com Streamlit

```bash
streamlit run app.py
```
Esse comando inicia uma interface web simples para interação com o modelo Gemini.

## Resultado esperado

O sistema envia uma pergunta para o modelo Gemini e retorna uma resposta textual gerada pela API, exibindo o resultado diretamente no terminal. As respostas seguem uma abordagem orientada ao aprendizado, auxiliando o usuário na compreensão do problema sem fornecer código ou solução pronta.

---

## Objetivo desta etapa

Esta etapa do projeto tem como objetivo validar:

- comunicação com uma API de modelo de linguagem;
- uso de variáveis de ambiente para credenciais;
- execução de scripts Python para interação com a API;
- implementação de um código mínimo funcional para geração de respostas.
- possibilidade de evolução para interfaces web e sistemas mais complexos.

## Próximos passos

- aprimorar o controle do comportamento do modelo (prompt engineering);
- implementar histórico de interações;
- evoluir a interface web;