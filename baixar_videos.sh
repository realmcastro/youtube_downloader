#!/bin/bash
# Script para baixar vídeos do YouTube a partir de CSVs usando ambiente virtual Python
# Uso: bash baixar_videos.sh

set -e

VENV_DIR="venv"
PYTHON_BIN="python3"

# 1. Cria o venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual Python..."
    $PYTHON_BIN -m venv "$VENV_DIR"
else
    echo "Ambiente virtual já existe."
fi

# 2. Instala dependências no venv
source "$VENV_DIR/bin/activate"
echo "Instalando dependências (yt-dlp, pandas)..."
pip install --upgrade pip > /dev/null
touch requirements.txt
echo -e "yt-dlp\npandas" > requirements.txt
pip install -r requirements.txt
rm requirements.txt

deactivate

# 3. Executa o cli_downloader.py usando o Python do venv
"$VENV_DIR/bin/python" cli_downloader.py 