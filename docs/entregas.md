# Entregas

## Entrega 1 – Testar chamadas básicas da API com exemplos fixos

Para validar a comunicação inicial com a API do modelo Gemini foi implementado o script:

`test_boole.py`

Esse script realiza uma chamada simples à API utilizando um prompt fixo e imprime a resposta retornada pelo modelo no terminal.

O objetivo dessa etapa é verificar se o sistema consegue:

- autenticar utilizando a chave da API;
- enviar uma requisição ao modelo;
- receber e exibir a resposta gerada.

### Execução

```bash
python test_boole.py
```

---

## Entrega 2 – Código mínimo funcional

Para implementar um exemplo funcional de interação com a API foi desenvolvido o script:

`run_boole.py`

Esse script permite que o usuário informe uma pergunta diretamente pelo terminal. A pergunta é enviada ao modelo Gemini, que gera uma resposta textual exibida no terminal.

Diferentemente do teste realizado na entrega anterior, esse script permite **entrada dinâmica do usuário**, caracterizando um código mínimo funcional capaz de receber dados, processá-los por meio da API e retornar uma resposta.

### Execução

```bash
python run_boole.py "Explique o que é uma variável"
```

Esse componente representa um protótipo simples de interação com o modelo de linguagem e pode ser posteriormente integrado a uma interface web do sistema.

---

## Extensão complementar – Interface com Streamlit

Como evolução da implementação, foi adicionada uma interface web simples utilizando Streamlit, permitindo interação com o modelo de linguagem de forma mais intuitiva.

O arquivo responsável por essa funcionalidade é:

`app.py`

A interface permite que o usuário insira perguntas em um campo de texto e visualize as respostas geradas pelo modelo diretamente no navegador.

Essa extensão não altera a lógica principal do sistema, mas demonstra a possibilidade de integração futura com uma interface web.

### Execução

```bash
streamlit run app.py
```