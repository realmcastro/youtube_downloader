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

# Função para juntar pares de .mp4 e .m4a com o mesmo nome base usando ffmpeg
juntar_audio_video() {
  cd videos 2>/dev/null || return 0
  for video in *.mp4; do
    [ -e "$video" ] || continue
    base="${video%.mp4}"
    # Procura qualquer arquivo de áudio com padrão NOME.audio.*
    audio_file=$(ls "${base}.audio."* 2>/dev/null | head -n1)
    if [[ -n "$audio_file" && -f "$audio_file" ]]; then
      echo "Juntando $video + $audio_file -> $video (sobrescrevendo)"
      ffmpeg -y -i "$video" -i "$audio_file" -c:v copy -c:a aac -strict experimental "${base}_muxed.mp4" < /dev/null
      mv -f "${base}_muxed.mp4" "$video"
      # Opcional: remover o áudio separado
      # rm "$audio_file"
    fi
  done
  cd ..
}

# 3. Executa o cli_downloader.py usando o Python do venv
"$VENV_DIR/bin/python" cli_downloader.py

# Para juntar manualmente depois, execute no terminal:
# source baixar_videos.sh && juntar_audio_video 