// =============================================
// CONFIGURAÇÃO
// =============================================

// ⚠️ O front roda no Live Server (porta 5500) e o backend FastAPI
// roda em outra porta (8000). Por isso TODA chamada precisa da URL
// completa do backend — caminhos relativos ("/auth/login-form")
// vão sempre bater no próprio Live Server, que não tem essas rotas.
const API_BASE_URL = 'http://127.0.0.1:8000';

// =============================================
// UTILITÁRIOS
// =============================================

function getAuthHeaders(isJson = true) {
    const token = localStorage.getItem('access_token');
    const headers = {};
    if (isJson) headers['Content-Type'] = 'application/json';
    if (token)  headers['Authorization'] = `Bearer ${token}`;
    return headers;
}

function adicionarMensagemNaView(remetente, conteudo, cor) {
    const p = document.createElement('p');
    p.style.cssText = `margin-top:8px; color:${cor};`;
    p.innerHTML = `<strong>${remetente}:</strong> ${conteudo}`;
    chatMessages.appendChild(p);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function exibirErroLogin(mensagem) {
    let errDiv = document.getElementById('loginError');
    if (!errDiv) {
        errDiv = document.createElement('p');
        errDiv.id = 'loginError';
        errDiv.style.cssText = 'color:red;font-size:0.85rem;margin-top:8px;text-align:center;';
        formLogin.appendChild(errDiv);
    }
    errDiv.textContent = '⚠ ' + mensagem;
}

// =============================================
// ELEMENTOS DO DOM
// =============================================

const openLoginBtn    = document.getElementById('openLogin');
const closeLoginBtn   = document.getElementById('closeLogin');
const loginModal      = document.getElementById('loginModal');
const formLogin       = document.getElementById('formLogin');
const logoutBtn       = document.getElementById('logoutBtn');
const toggleChatBtn   = document.getElementById('toggleChat');
const minimizeChatBtn = document.getElementById('minimizeChat');
const chatBox         = document.getElementById('chatBox');
const chatInput       = document.getElementById('chatInput');
const sendChatBtn     = document.getElementById('sendChat');
const chatMessages    = document.getElementById('chatMessages');

// =============================================
// AUTENTICAÇÃO — Login / Logout
// =============================================

openLoginBtn.addEventListener('click', () => {
    if (localStorage.getItem('access_token')) return;
    loginModal.classList.add('active');
});

closeLoginBtn.addEventListener('click', () => {
    loginModal.classList.remove('active');
});

loginModal.addEventListener('click', (e) => {
    if (e.target === loginModal) loginModal.classList.remove('active');
});

['email', 'password'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
        const err = document.getElementById('loginError');
        if (err) err.textContent = '';
    });
});

// -----------------------------------------------
// POST {API_BASE_URL}/auth/login-form (OAuth2PasswordRequestForm)
// -----------------------------------------------
formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = formLogin.querySelector('button[type="submit"]');

    submitBtn.disabled    = true;
    submitBtn.textContent = 'Entrando...';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login-form`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: email, password: password }),
            credentials: 'include',
        });

        const text = await response.text();
        let data;
        try {
            data = text ? JSON.parse(text) : {};
        } catch {
            throw new Error('Resposta inesperada do servidor: ' + text.substring(0, 80));
        }

        if (!response.ok) {
            throw new Error(data.detail || `Erro ${response.status}`);
        }

        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_email', email);

        loginModal.classList.remove('active');
        formLogin.reset();
        atualizarUI(email);

        if (chatBox.classList.contains('active')) {
            await carregarHistorico();
        }

    } catch (error) {
        exibirErroLogin(error.message);
    } finally {
        submitBtn.disabled    = false;
        submitBtn.textContent = 'Entrar';
    }
});

function atualizarUI(email) {
    if (email) {
        const nome = email.split('@')[0];
        openLoginBtn.textContent      = `👤 ${nome}`;
        openLoginBtn.style.background = '#28a745';
        openLoginBtn.style.cursor     = 'default';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
    } else {
        openLoginBtn.textContent      = 'Acessar Conta';
        openLoginBtn.style.background = '';
        openLoginBtn.style.cursor     = 'pointer';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
}

function fazerLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    atualizarUI(null);
    chatMessages.innerHTML = '<p style="color:#888;">💬 Nenhuma mensagem ainda. Comece a conversar!</p>';
}

if (logoutBtn) {
    logoutBtn.addEventListener('click', fazerLogout);
}

// =============================================
// CHAT — Histórico / Mensagens
// =============================================

toggleChatBtn.addEventListener('click', () => {
    chatBox.classList.toggle('active');
    if (chatBox.classList.contains('active')) {
        carregarHistorico();
    }
});

minimizeChatBtn.addEventListener('click', () => {
    chatBox.classList.remove('active');
});

// -----------------------------------------------
// GET {API_BASE_URL}/messages/historico
// -----------------------------------------------
async function carregarHistorico() {
    try {
        const response = await fetch(`${API_BASE_URL}/messages/historico`, {
            credentials: 'include',
            headers: getAuthHeaders(),
        });

        if (!response.ok) throw new Error(`Erro ${response.status}`);

        const data = await response.json();
        chatMessages.innerHTML = '';

        if (data.mensagens && data.mensagens.length > 0) {
            data.mensagens.forEach(msg => {
                if (Array.isArray(msg)) {
                    msg.forEach(turno => renderizarMensagem(turno));
                } else {
                    renderizarMensagem(msg);
                }
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else {
            chatMessages.innerHTML = '<p style="color:#888;">💬 Nenhuma mensagem ainda. Comece a conversar!</p>';
        }
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        chatMessages.innerHTML = '<p style="color:red;">❌ Não foi possível carregar o histórico.</p>';
    }
}

function renderizarMensagem(msg) {
    const isUser = msg.role === 'user';
    const sender = isUser ? 'Você' : 'IA';
    const cor    = isUser ? '#007bff' : '#28a745';
    adicionarMensagemNaView(sender, msg.conteudo, cor);
}

// -----------------------------------------------
// POST {API_BASE_URL}/messages/menssagens
// -----------------------------------------------
async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    adicionarMensagemNaView('Você', text, '#007bff');
    chatInput.value = '';

    try {
        const response = await fetch(`${API_BASE_URL}/messages/menssagens`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ conteudo: text }),
            credentials: 'include',
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || `Erro ${response.status}`);
        }

        const data = await response.json();
        adicionarMensagemNaView('IA', data.resposta, '#28a745');

    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        adicionarMensagemNaView('Erro', error.message, 'red');
    }
}

sendChatBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// =============================================
// INICIALIZAÇÃO
// =============================================
window.addEventListener('load', () => {
    const token = localStorage.getItem('access_token');
    const email = localStorage.getItem('user_email');

    if (token && email) {
        atualizarUI(email);
    }
});