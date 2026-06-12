from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencias import pegar_sessao, verificar_token
from models import Usuario, Consent                              # após adicionar ao models.py
from schemas import ConsentCreateSchema, ConsentResponseSchema  # após adicionar ao schemas.py

consent_router = APIRouter(prefix="/consents", tags=["consents"])


# ─── GET /consents ────────────────────────────────────────────────────────────
@consent_router.get("/", response_model=List[ConsentResponseSchema])
async def listar_consents(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Lista todas as permissões do agente para o usuário autenticado."""
    consents = session.query(Consent).filter_by(id_usuario=usuario.id).all()
    return consents


# ─── POST /consents ───────────────────────────────────────────────────────────
@consent_router.post("/", response_model=ConsentResponseSchema, status_code=201)
async def criar_consent(
    dados: ConsentCreateSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Concede uma nova permissão ao agente de IA."""
    # Evita duplicata de permissão ativa
    existente = (
        session.query(Consent)
        .filter_by(id_usuario=usuario.id, permissao=dados.permissao, ativo=True)
        .first()
    )
    if existente:
        raise HTTPException(status_code=400, detail=f"Permissão '{dados.permissao}' já está ativa.")

    novo_consent = Consent(id_usuario=usuario.id, permissao=dados.permissao)
    session.add(novo_consent)
    session.commit()
    session.refresh(novo_consent)
    return novo_consent


# ─── DELETE /consents/{permissao} ────────────────────────────────────────────
@consent_router.delete("/{permissao}", status_code=200)
async def revogar_consent(
    permissao: str,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Revoga (desativa) uma permissão do agente. Não apaga o registro."""
    consent = (
        session.query(Consent)
        .filter_by(id_usuario=usuario.id, permissao=permissao, ativo=True)
        .first()
    )
    if not consent:
        raise HTTPException(status_code=404, detail=f"Permissão '{permissao}' não encontrada ou já revogada.")

    consent.ativo = False
    session.commit()
    return {"message": f"Permissão '{permissao}' revogada com sucesso."}
