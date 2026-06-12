# 🤖 Agente de IA — Backend FastAPI

Backend de uma aplicação de agente de IA com autenticação JWT, histórico de chat, perfis de usuário e controle de permissões. Construído com **FastAPI**, **SQLAlchemy** e **MySQL**.

---

## 📁 Estrutura do projeto

```
.
├── main.py                 # Ponto de entrada da aplicação
├── models.py               # Modelos do banco de dados (SQLAlchemy)
├── schemas.py              # Schemas de validação (Pydantic)
├── dependencias.py         # Funções reutilizáveis (sessão, verificação de token)
├── auth_routes.py          # Rotas de autenticação (/auth)
├── requeriment_routes.py   # Rotas de requerimentos (/requeriments)
├── profile_routes.py       # Rotas de perfil do usuário (/profile)
├── consent_routes.py       # Rotas de permissões do agente (/consents)
├── message_routes.py       # Rotas de chat com a IA (/message)
├── requirements.txt        # Dependências do projeto
└── .env                    # Variáveis de ambiente (não versionar)
```

---

## ⚙️ Configuração do ambiente

### 1. Clone e crie o ambiente virtual

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>

python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de dados MySQL
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/agente_ia

# JWT
SECRET_KEY=sua_chave_secreta_muito_segura kL._=^Ysqp+vlNY6
ALGORITHM=HS256
EXPIRED_TIME_TOKEN=30

# API Anthropic (agente de IA)
ANTHROPIC_API_KEY=sk-ant-...
```

> ⚠️ Nunca suba o arquivo `.env` para o repositório. Adicione-o ao `.gitignore`.

### iniciar serviço do banco de dados
# sudo /opt/lampp/lampp start


### 4. Crie o banco de dados MySQL

```sql
CREATE DATABASE agente_ia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Execute as migrações

```bash
alembic upgrade head
```

> Se for a primeira vez usando o Alembic no projeto, inicialize com `alembic init alembic` e configure o `alembic.ini` para usar a `DATABASE_URL` do `.env`.

### 6. Inicie o servidor

```bash
uvicorn main:app --reload
```

A aplicação estará disponível em `http://localhost:8000`.
A documentação interativa (Swagger) em `http://localhost:8000/docs`.

---

## 🗺️ Rotas da API

### 🔐 Autenticação — `/auth`

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `GET` | `/auth/` | Verifica se a rota está ativa | ❌ |
| `POST` | `/auth/criar_usuario` | Cadastra um novo usuário | ❌ |
| `POST` | `/auth/login` | Autentica e retorna tokens JWT | ❌ |
| `POST` | `/auth/refresh` | Gera um novo access token | ✅ |

**Exemplo — Login:**
```json
POST /auth/login
{
  "email": "usuario@email.com",
  "senha": "minhasenha123"
}
```
**Resposta:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### 👤 Perfil — `/profile`

Todas as rotas exigem autenticação (`Bearer token`).

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/profile/` | Retorna o perfil do usuário logado |
| `POST` | `/profile/` | Cria o perfil (apenas um por usuário) |
| `PUT` | `/profile/` | Atualiza os dados do perfil |

**Exemplo — Criar perfil:**
```json
POST /profile/
{
  "bio": "Desenvolvedor apaixonado por IA",
  "avatar_url": "https://exemplo.com/avatar.png",
  "preferencias": "{\"tema\": \"escuro\", \"idioma\": \"pt-BR\"}"
}
```

> O campo `preferencias` é uma string JSON livre — use para armazenar qualquer configuração do usuário.

---

### 🛡️ Permissões do agente — `/consents`

Todas as rotas exigem autenticação.

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/consents/` | Lista todas as permissões ativas |
| `POST` | `/consents/` | Concede uma nova permissão ao agente |
| `DELETE` | `/consents/{permissao}` | Revoga uma permissão |

**Exemplo — Conceder permissão:**
```json
POST /consents/
{
  "permissao": "web_search"
}
```

**Exemplos de permissões sugeridas:**

| Permissão | O que representa |
|-----------|-----------------|
| `web_search` | Agente pode buscar na web |
| `send_email` | Agente pode enviar e-mails |
| `read_calendar` | Agente pode ler a agenda |
| `write_files` | Agente pode criar arquivos |

> Permissões revogadas não são apagadas do banco — apenas marcadas como `ativo = false`, preservando o histórico.

---

### 💬 Chat com o agente — `/message`

Todas as rotas exigem autenticação.

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/message/` | Retorna todo o histórico de mensagens |
| `POST` | `/message/` | Envia uma mensagem e recebe a resposta da IA |
| `DELETE` | `/message/` | Apaga todo o histórico de mensagens |

**Exemplo — Enviar mensagem:**
```json
POST /message/
{
  "conteudo": "Olá! O que você pode fazer por mim?"
}
```

**Resposta:**
```json
{
  "id": 2,
  "usuario_id": 1,
  "role": "assistant",
  "conteudo": "Olá! Posso te ajudar com diversas tarefas...",
  "criado_em": "2024-11-01T10:30:00"
}
```

> O histórico completo da conversa é enviado a cada requisição, mantendo o contexto do chat. As permissões ativas do usuário também são informadas ao agente automaticamente.

---

## 🗄️ Modelos do banco de dados

```
usuarios
├── id, nome, email, senha, ativo, admin

profiles  (1:1 com usuarios)
├── id, usuario_id, bio, avatar_url, preferencias, criado_em, atualizado_em

consents  (N:1 com usuarios)
├── id, usuario_id, permissao, ativo, criado_em

messages  (N:1 com usuarios)
├── id, usuario_id, role, conteudo, criado_em

requeriments  (N:1 com usuarios)
├── id, usuario_id, status, conteudo



---

## 🔒 Autenticação

A API usa **JWT (JSON Web Token)** com dois tokens:

- **access_token** — expira em `EXPIRED_TIME_TOKEN` minutos (padrão: 30 min)
- **refresh_token** — expira em 7 dias

Para acessar rotas protegidas, envie o header:
```
Authorization: Bearer <access_token>
```

Quando o access token expirar, use a rota `/auth/refresh` com o refresh token para obter um novo.

---

## 🧪 Testando a API

Com o servidor rodando, acesse a documentação interativa Swagger em:

```
http://localhost:8000/docs
```

Fluxo recomendado para testar:
1. `POST /auth/criar_usuario` — crie um usuário
2. `POST /auth/login` — faça login e copie o `access_token`
3. Clique em **Authorize** no Swagger e cole o token
4. `POST /profile/` — crie seu perfil
5. `POST /consents/` — conceda permissões ao agente
6. `POST /message/` — converse com o agente de IA

---

## 📦 Dependências principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| `fastapi` | 0.115.0 | Framework web |
| `uvicorn` | 0.30.6 | Servidor ASGI |
| `sqlalchemy` | 2.0.35 | ORM do banco de dados |
| `pymysql` | 1.1.1 | Driver MySQL |
| `python-jose` | 3.3.0 | Geração e validação de JWT |
| `passlib[bcrypt]` | 1.7.4 | Hash de senhas |
| `httpx` | 0.27.2 | Chamadas HTTP para a API da IA |
| `alembic` | 1.13.3 | Migrações do banco de dados |
| `python-dotenv` | 1.0.1 | Leitura do arquivo `.env` |
