from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencias import pegar_sessao, verificar_token
from main import CryptContext, SECRET_KEY, ALGORITHM, EXPIRED_TIME_TOKEN
from schemas import Usuarioschema, LoguinSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta,timezone
import os
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario,duracao_tolken=timedelta(minutes=EXPIRED_TIME_TOKEN)):
    expired_time = datetime.now(timezone.utc) + duracao_tolken
    dic_info_token = {"sub": str(id_usuario), "exp": expired_time}
    token = jwt.encode(dic_info_token, SECRET_KEY, algorithm=ALGORITHM)
    return token
    
    

def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter_by(email=email).first()
    
    if not usuario:
        return False
    if not CryptContext.verify(senha, usuario.senha):
        return False
    return usuario



@auth_router.get("/")
async def autenticar():
    return {"message": "Rota de autenticação","autenticado": False}

@auth_router.post("/criar_usuario")
async def criar_usuario(usurio_schemas: Usuarioschema, session: Session = Depends(pegar_sessao)):
    # Verificar se o email já existe
    usuario_existente = session.query(Usuario).filter_by(email=usurio_schemas.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        # Criar um novo usuário
        senha_criptografada = CryptContext.hash(usurio_schemas.senha)
        senha = senha_criptografada[:72]  # Armazenar apenas os primeiros 72 caracteres
        novo_usuario = Usuario(nome=usurio_schemas.nome, email=usurio_schemas.email, senha=senha)
        session.add(novo_usuario)
        session.commit()

        raise HTTPException(status_code=200, detail="Usuário criado com sucesso")

@auth_router.post("/login")
async def login(login_schema: LoguinSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")
    
    else:
        access_token = criar_token(usuario.id)
        refrash_token = criar_token(usuario.id, duracao_tolken=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refrash_token,
                "token_type": "bearer"}

@auth_router.post("/login-form")
async def login_form(formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(formulario.username, formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")

    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"}
    

@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    #verificar token
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"}