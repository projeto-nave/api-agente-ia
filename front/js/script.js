// --- Lógica do Pop-up de Login ---
const openLoginBtn = document.getElementById('openLogin');
const closeLoginBtn = document.getElementById('closeLogin');
const loginModal = document.getElementById('loginModal');
const formLogin = document.getElementById('formLogin');

openLoginBtn.addEventListener('click', () => {
    loginModal.classList.add('active');
});

closeLoginBtn.addEventListener('click', () => {
    loginModal.classList.remove('active');
});

// Fecha o modal se clicar fora da caixinha branca
loginModal.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.classList.remove('active');
    }
});

formLogin.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Simulação de login feita com sucesso!');
    loginModal.classList.remove('active');
});


// --- Lógica do Totem de Chat ---
const toggleChatBtn = document.getElementById('toggleChat');
const minimizeChatBtn = document.getElementById('minimizeChat');
const chatBox = document.getElementById('chatBox');
const chatInput = document.getElementById('chatInput');
const sendChatBtn = document.getElementById('sendChat');
const chatMessages = document.getElementById('chatMessages');

// Abre / Fecha a janela de chat
toggleChatBtn.addEventListener('click', () => {
    chatBox.classList.toggle('active');
});

minimizeChatBtn.addEventListener('click', () => {
    chatBox.classList.remove('active');
});

// Função para enviar mensagem no chat
function sendMessage() {
    const text = chatInput.value.trim();
    if (text !== '') {
        // Mensagem do usuário
        chatMessages.innerHTML += `<p style="margin-top:8px;"><strong>Você:</strong> ${text}</p>`;
        chatInput.value = '';

        // Rolagem automática para o final do chat
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Simulação de resposta da IA (Apenas fictício por enquanto)
        setTimeout(() => {
            chatMessages.innerHTML += `<p style="margin-top:8px; color:#28a745;"><strong>IA:</strong> Entendi seu ponto sobre "${text}". Estou processando...</p>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
}

sendChatBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});