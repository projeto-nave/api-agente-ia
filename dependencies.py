from fastapi import Depends, HTTPException, Cookie, Response, Request
from main import SECRET_KEY, ALGORITHM
from main import oauth2_scheme, oauth2_scheme_opcional
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario, DB
from jose import jwt, JWTError
import uuid


def pegar_sessao():
    try:
        SessionLocal = sessionmaker(bind=DB)
        session = SessionLocal()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    # verificar token válido / extrair id do usuário do token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError) as error:
        print(error)
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter_by(id=id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario


def verificar_token_opcional(
    token: str = Depends(oauth2_scheme_opcional),
    session: Session = Depends(pegar_sessao)
):
    """
    Rota flexível: tenta autenticar, mas NUNCA derruba a requisição.
    - Sem token        -> retorna None (visitante)
    - Token inválido    -> retorna None (trata como visitante, não levanta erro)
    - Token válido       -> retorna o Usuario
    """
    if token is None:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = payload.get("sub")
        if id_usuario is None:
            return None
        id_usuario = int(id_usuario)
    except (JWTError, TypeError, ValueError):
        # ✅ CORRIGIDO: nunca levanta HTTPException aqui.
        # Levantar exceção (mesmo com status 200) interrompe a request.
        # Token ruim/expirado deve simplesmente cair para "visitante".
        return None

    usuario = session.query(Usuario).filter_by(id=id_usuario).first()
    return usuario if usuario else None


def get_session_id(
    request: Request,
    response: Response,
    session_id: str = Cookie(None, alias="gues_session")
) -> str:
    if session_id:
        return session_id

    # Cria novo ID apenas se realmente não existir cookie ainda
    novo_id = str(uuid.uuid4())
    response.set_cookie(
        key="gues_session",
        value=novo_id,
        max_age=60 * 60 * 24 * 30,  # 30 dias
        httponly=True,              # impede acesso via JS (mais seguro)
        secure=True,               # ⚠️ mude para True em produção com HTTPS
        samesite=None,
        path="/",
        # ✅ CORRIGIDO: domain removido.
        # "domain=localhost" fazia o navegador descartar o cookie quando
        # o site era acessado por 127.0.0.1 (domínio diferente de localhost
        # do ponto de vista do browser). Sem "domain", o navegador usa
        # automaticamente o host que respondeu a requisição.
    )
    return novo_id