// função listas colapsáveis
document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.toggle-button');

    toggles.forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content) {
                content.classList.toggle('open');
            }
        }); 
    });
});

// função resposta da API
window.resposta_API = function() {
    const duvida = document.getElementById('duvida').value;
    const respostaElement = document.getElementById('resposta');

    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duvida: duvida }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.resultado) {
            respostaElement.innerText = data.resultado;
        } else if (data.erro) {
            alert(data.erro);
        }
    })
    .catch(error => console.error('Erro:', error));
};

function enviar_dados() {
    const usuario = document.getElementById('usuario').value;
    const senha = document.getElementById('senha').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ usuario: usuario, senha: senha }),
    })
    .then(response => response.json()) 

    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect; 
        } else if (data.erro) {
            alert(data.erro); 
        }
    })
    .catch(error => console.error('Erro:', error));
    
}

function criar_conta() {
    window.location.href = '/criar-conta';
}


// função suporte tela de login e tela de cadastro (error handling)
window.promptCrieUsuario = () =>{
    const botaoLogin = document.getElementById('botao-login')
    // terminar de fazer após o back incrementar essa parte
    // pensar na situação: usuário tentou login mas nunca se cadastrou;
    
}

// tela de cadastro: se o usuário está disponível ou não