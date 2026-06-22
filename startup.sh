#!/bin/bash

# Instala as dependências
echo "Instalando dependências..."
pip install --no-cache-dir -r requirements.txt

# Inicia a aplicação
echo "Iniciando aplicação..."
uvicorn main:app --host 0.0.0.0 --port 8000