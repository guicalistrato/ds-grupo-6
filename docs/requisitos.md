# Requisitos

## Requisitos funcionais

O sistema deve:

- realizar chamadas para a API do modelo de linguagem Gemini;
- enviar uma pergunta textual ao modelo;
- receber e exibir uma resposta textual gerada pela API;
- permitir a execução de um teste utilizando um prompt fixo para validar a comunicação com a API;
- permitir que o usuário informe uma pergunta pelo terminal.
- permitir interação por meio de uma interface web simples utilizando Streamlit (extensão complementar);
- orientar o usuário na resolução de problemas sem fornecer código ou solução pronta.


---

## Requisitos não funcionais

O sistema deve:

- armazenar a chave da API utilizando variável de ambiente;
- utilizar bibliotecas oficiais ou recomendadas para acesso à API Gemini;
- possuir código simples e organizado para facilitar manutenção e evolução do projeto;
- permitir execução direta a partir do terminal;
- permitir execução de interface web local via Streamlit;
- possuir documentação básica para execução e compreensão do sistema.
- garantir que as respostas do modelo sigam restrições pedagógicas (ex: não fornecer código).