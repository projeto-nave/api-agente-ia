from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
from fast_api_app.models import Base, DB
import os

load_dotenv()

SECRET_KEY         = os.getenv("SECRET_KEY")
ALGORITHM          = os.getenv("ALGORITHM")
EXPIRED_TIME_TOKEN = int(os.getenv("EXPIRED_TIME_TOKEN"))
API_KEY            = os.getenv("API_KEY")

app = FastAPI(
    title="Nave - Agente de IA",
    description="""
## API do Agente Anfitrião das Naves do Conhecimento

Gerencie usuários, consentimentos e conversas com o agente de IA.

### Autenticação
1. Crie um usuário em **POST /auth/criar_usuario**
2. Faça login em **POST /auth/login** e copie o `access_token`
3. Clique em **Authorize** (🔒) e cole o token no campo `Bearer`
""",
    version="1.0.0",
    servers=[
        {"url": "https://api-agente-ia-gqkw.onrender.com", "description": "Produção"},
        {"url": "http://localhost:8000",         "description": "Local"},
    ]
)

# ── CORS: permite o GitHub Pages chamar a API ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://RedFalc0n12.github.io",  # substitua pelo seu usuário
        "http://localhost:8000",
        "http://127.0.0.1:5500",          # Live Server do VS Code
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cria todas as tabelas no banco se não existirem ───────────────────────────
Base.metadata.create_all(bind=DB)

CryptContext  = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ── Routers ───────────────────────────────────────────────────────────────────
from fast_api_app.auth_routes    import auth_router
from fast_api_app.consent_routes import consent_router
from fast_api_app.message_routes import message_router

app.include_router(auth_router)
app.include_router(consent_router)
app.include_router(message_router)

# para executar: uvicorn main:app --reload