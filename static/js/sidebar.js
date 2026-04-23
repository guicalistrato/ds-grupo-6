// funções sidebar

window.closeSidebar = function() {
    document.getElementById("Sidebar").style.width = "0";
    document.getElementById("main-content").style.marginLeft = "0";
};

// função listas colapsáveis - em comentário porque na versão atual não é necessária
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