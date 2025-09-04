"""
Script para baixar vídeos do YouTube a partir de um CSV.

Regras:
- Coluna 'link' é a URL do vídeo.
- Coluna 'file' é o nome final do arquivo de saída.
- Tenta baixar vídeo em 1080p com áudio embutido.
- Se não houver, baixa o melhor vídeo disponível e o melhor áudio separado, mescla e salva com o nome especificado.

Requisitos: pip install yt-dlp pandas
"""
import os
import subprocess
import pandas as pd

CSV_PATH = "yt-download-page-4.csv"
OUTPUT_DIR = "videos"

# Garante que a pasta de saída existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def baixar_video(url, output_filename):
    """
    Baixa o vídeo do YouTube conforme as regras:
    1. Tenta baixar 1080p com áudio embutido.
    2. Se não houver, baixa o melhor vídeo e áudio separados e mescla.
    """
    saida_path = os.path.join(OUTPUT_DIR, output_filename)
    # 1. Tenta baixar 1080p com áudio embutido
    cmd_1080p = [
        "yt-dlp",
        "-f", "bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080][ext=mp4]/bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", saida_path,
        url
    ]
    try:
        print(f"Baixando: {url} -> {saida_path}")
        subprocess.run(cmd_1080p, check=True)
    except subprocess.CalledProcessError:
        print(f"Falha ao baixar 1080p, tentando melhor qualidade disponível para: {url}")
        # 2. Baixa o melhor vídeo e áudio disponíveis
        cmd_best = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", saida_path,
            url
        ]
        subprocess.run(cmd_best, check=True)

def main():
    df = pd.read_csv(CSV_PATH, sep='|', engine='python')
    # Remove aspas extras dos nomes das colunas
    df.columns = [col.strip().replace('"', '') for col in df.columns]
    for idx, row in df.iterrows():
        url = row['link'].strip().replace('"', '')
        output_filename = row['file'].strip().replace('"', '')
        if not url or not output_filename:
            continue
        try:
            baixar_video(url, output_filename)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

if __name__ == "__main__":
    main() 