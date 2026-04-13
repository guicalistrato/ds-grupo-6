// --- 1. Sidebar Open/Close Functions (Global Scope) ---
window.openSidebar = function() {
    document.getElementById("Sidebar").style.width = "250px";
    document.getElementById("main-content").style.marginLeft = "250px";
};

window.closeSidebar = function() {
    document.getElementById("Sidebar").style.width = "0";
    document.getElementById("main-content").style.marginLeft = "0";
};

// --- 2. Collapsible Lists (Runs after HTML loads) ---
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

// --- 3. API Response Function (Global Scope) ---
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