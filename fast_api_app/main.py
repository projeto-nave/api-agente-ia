from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import logging

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",      # Live Server
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def log_cookies(request: Request, call_next):
    print(f"🍪 Cookies recebidos: {request.cookies}")
    response = await call_next(request)
    print(f"🍪 Cookies enviados: {response.headers.get('set-cookie')}")
    return response



# ── Routers existentes ────────────────────────────────────────────────────────
from auth_routes        import auth_router
from message_routes import message_router


app.include_router(auth_router)
app.include_router(message_router)






# para executar: uvicorn main:app --reload
