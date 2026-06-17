from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY         = os.getenv("SECRET_KEY")
ALGORITHM          = os.getenv("ALGORITHM")
EXPIRED_TIME_TOKEN = int(os.getenv("EXPIRED_TIME_TOKEN"))
API_KEY            = os.getenv("API_KEY")

app = FastAPI(
    title="Nave - Agente de IA",
    description="API para gerenciamento de usuários, consentimentos e mensagens do agente de IA Nave.",
    version="1.0.0",
     
)

CryptContext  = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")
oauth2_scheme_opcional = OAuth2PasswordBearer(tokenUrl="auth/login-form",auto_error=False)
tela = "tela de teste"

# ── Routers existentes ────────────────────────────────────────────────────────
from auth_routes        import auth_router
from message_routes import message_router
from chat_routes import chat_router

app.include_router(auth_router)
app.include_router(message_router)
app.include_router(chat_router)

# para executar: uvicorn main:app --reload
