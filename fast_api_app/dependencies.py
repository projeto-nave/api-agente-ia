from fastapi import Depends, HTTPException,Cookie, Response, Request
from main import SECRET_KEY, ALGORITHM
from main import oauth2_scheme,oauth2_scheme_opcional
from sqlalchemy.orm import sessionmaker,Session
from models import Usuario,DB
from jose import jwt, JWTError
import uuid

def pegar_sessao():
    try:
        Session = sessionmaker(bind=DB)
        session = Session()
        yield session 
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    #verificar token valido
    #extrair id do usuario do token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
        if id_usuario is None:
            return None
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter_by(id=id_usuario).first()
    return usuario

def verificar_token_opcional(
    token: str = Depends(oauth2_scheme_opcional),
    session: Session = Depends(pegar_sessao)
):
    # Se não veio token, retorna None (visitante)
    if token is None:
        return "visitante"

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
        if id_usuario is None:
            raise "visitante"
    except JWTError:
        # Token inválido – aqui você decide: trata como não autenticado ou levanta erro?
        # Para uma rota flexível, retorne None (não autenticado)
        raise HTTPException(status_code=200,detail={"menssagem":"acesso sem login"})

    usuario = session.query(Usuario).filter_by(id=id_usuario).first()
    if usuario:
        return usuario
    else:
        return "visitante"
    


def get_session_id(
    request: Request,
    response: Response,
    session_id: str = Cookie(None, alias="gues_session")
) -> str:
    if session_id:
        return session_id
    # Cria novo ID
    novo_id = str(uuid.uuid4())
    response.set_cookie(
        key="gues_session",
        value=novo_id,
        max_age=60*60*24*30,  # 30 dias
        httponly=True,        # impede acesso via JS (mais seguro)
        secure=False,         # mude para True em produção com HTTPS
        samesite="lax"
    )
    return novo_id