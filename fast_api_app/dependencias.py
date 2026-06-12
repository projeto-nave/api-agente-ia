from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM
from main import oauth2_scheme
from sqlalchemy.orm import sessionmaker,Session
from models import Usuario,DB
from jose import jwt, JWTError


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
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter_by(id=id_usuario).first()
    return usuario