// função fechar sidebar
window.closeSidebar = function() {
    document.getElementById("Sidebar").style.width = "0";
    document.getElementById("chat-container").style.marginLeft = "0";
    document.getElementById("openbtn").style.visibility = 'visible';
};

document.addEventListener('DOMContentLoaded', () => {
    carregarSidebarChats();
});

async function carregarSidebarChats() {
    console.log("1. Iniciando carregamento da sidebar...");
    try {
        const response = await fetch('/api/listar_chats');
        console.log("2. Resposta da API recebida. Status:", response.status);
        
        if (!response.ok) {
            console.error('Falha ao carregar lista de chats');
            return;
        }

        const data = await response.json();
        console.log("3. Dados transformados em JSON:", data);

        const conversationList = document.getElementById('conversation-list');
        if (!conversationList) {
            console.error("ERRO CRÍTICO: Elemento 'conversation-list' não foi encontrado no HTML!");
            return;
        }
        
        conversationList.innerHTML = ''; 
        console.log("4. Lista limpa. Quantidade de chats para renderizar:", data.chats ? data.chats.length : "Nenhum/Indefinido");

        if (data.chats && data.chats.length > 0) {
            data.chats.forEach(chat => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                
                a.href = '/chat/' + chat.id_chat;
                a.textContent = chat.nome_chat || 'Nova Conversa';

                const currentUrlPath = window.location.pathname;
                if (currentUrlPath.includes(chat.id_chat)) {
                    a.classList.add('active-chat');
                }

                li.appendChild(a);
                conversationList.appendChild(li);
            });
            console.log("5. Renderização concluída! Verifique a tela.");
        } else {
            console.warn("Aviso: A lista de chats chegou vazia.");
        }

    } catch (error) {
        console.error("Erro ao montar a sidebar:", error);
    }
}

window.carregarSidebarChats = carregarSidebarChats;

// função listas colapsáveis - em comentário porque nao vai ser necessária na versão atual, mas pode ser util futuramente
//document.addEventListener('DOMContentLoaded', () => {
//    const toggles = document.querySelectorAll('.toggle-button');
//
//    toggles.forEach(btn => {
//      btn.addEventListener('click', function() {
//            this.classList.toggle('active');
//          const content = this.nextElementSibling;
//            if (content) {
//                content.classList.toggle('open');
//            }
//        }); 
//    });
//});