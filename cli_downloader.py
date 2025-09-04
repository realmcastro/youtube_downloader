"""
CLI interativa para baixar vídeos do YouTube a partir de arquivos CSV.

Funcionalidades:
- Cria e ativa ambiente virtual (venv) automaticamente.
- Instala dependências necessárias (yt-dlp, pandas) no venv.
- Lista todos os arquivos CSV do diretório.
- Permite selecionar um ou mais CSVs para baixar vídeos.
- Valida se o CSV possui as colunas obrigatórias ('link' e 'file').
- Executa o download dos vídeos conforme as regras do projeto.

Como usar:
1. Execute: python cli_downloader.py
2. Siga as instruções interativas.
"""
import os
import sys
import subprocess
import glob
import shutil
import pandas as pd

VENV_DIR = "venv"
REQUIRED_PACKAGES = ["yt-dlp", "pandas"]

# Função para criar ambiente virtual
def criar_venv():
    if not os.path.exists(VENV_DIR):
        print("Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    else:
        print("Ambiente virtual já existe.")

# Função para instalar dependências no venv
def instalar_dependencias():
    pip_path = os.path.join(VENV_DIR, "bin", "pip")
    print("Instalando dependências no venv...")
    subprocess.run([pip_path, "install"] + REQUIRED_PACKAGES, check=True)

# Função para ativar o venv (apenas para instrução ao usuário)
def instruir_ativacao_venv():
    activate_path = os.path.join(VENV_DIR, "bin", "activate")
    print(f"\nPara ativar o ambiente virtual, execute:\nsource {activate_path}\n")

# Função para listar todos os CSVs do diretório atual
def listar_csvs():
    csvs = glob.glob("*.csv")
    if not csvs:
        print("Nenhum arquivo CSV encontrado no diretório.")
        sys.exit(1)
    return csvs

# Função para menu interativo de seleção de CSVs
def selecionar_csvs(csvs):
    print("\nArquivos CSV encontrados:")
    for idx, csv in enumerate(csvs):
        print(f"[{idx+1}] {csv}")
    print("[0] Cancelar")
    selecao = input("\nDigite os números dos CSVs separados por vírgula (ex: 1,3): ")
    if selecao.strip() == "0":
        print("Operação cancelada.")
        sys.exit(0)
    indices = [int(i.strip())-1 for i in selecao.split(",") if i.strip().isdigit() and 0 < int(i.strip()) <= len(csvs)]
    selecionados = [csvs[i] for i in indices]
    if not selecionados:
        print("Nenhum CSV selecionado.")
        sys.exit(1)
    return selecionados

# Função para limpar o CSV removendo o índice inicial (número|) de cada linha
def limpar_csv(caminho_csv):
    linhas_limpa = []
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        for linha in f:
            # Remove tudo até o primeiro pipe (inclusive)
            if '|' in linha:
                linhas_limpa.append(linha.split('|', 1)[1])
            else:
                linhas_limpa.append(linha)
    return linhas_limpa

# Função para validar o CSV
def validar_csv(caminho_csv):
    try:
        linhas = limpar_csv(caminho_csv)
        from io import StringIO
        df = pd.read_csv(StringIO(''.join(linhas)), sep=',')
        df.columns = [col.strip().replace('"', '') for col in df.columns]
        if 'link' not in df.columns or 'file' not in df.columns:
            print(f"CSV '{caminho_csv}' não possui as colunas obrigatórias: 'link' e 'file'.")
            return False
        return True
    except Exception as e:
        print(f"Erro ao ler '{caminho_csv}': {e}")
        return False

# Função para baixar vídeos de um CSV (reutiliza lógica do script anterior)
def baixar_videos_csv(caminho_csv):
    print(f"\nIniciando download para: {caminho_csv}")
    linhas = limpar_csv(caminho_csv)
    from io import StringIO
    df = pd.read_csv(StringIO(''.join(linhas)), sep=',')
    df.columns = [col.strip().replace('"', '') for col in df.columns]
    output_dir = "videos"
    os.makedirs(output_dir, exist_ok=True)
    for idx, row in df.iterrows():
        url = row['link'].strip().replace('"', '')
        output_filename = row['file'].strip().replace('"', '')
        if not url or not output_filename:
            continue
        # Baixar para um nome temporário
        tmp_prefix = f"tmp_{os.path.splitext(output_filename)[0]}"
        tmp_path = os.path.join(output_dir, tmp_prefix)
        cmd_1080p = [
            os.path.join(VENV_DIR, "bin", "yt-dlp"),
            "-f", "bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080][ext=mp4]/bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--force-overwrites",
            "-o", tmp_path,
            url
        ]
        try:
            print(f"Baixando: {url} -> {output_filename}")
            subprocess.run(cmd_1080p, check=True)
        except subprocess.CalledProcessError:
            print(f"Falha ao baixar 1080p, tentando melhor qualidade disponível para: {url}")
            cmd_best = [
                os.path.join(VENV_DIR, "bin", "yt-dlp"),
                "-f", "bestvideo+bestaudio/best",
                "--merge-output-format", "mp4",
                "--force-overwrites",
                "-o", tmp_path,
                url
            ]
            subprocess.run(cmd_best, check=True)
        # Após o download, renomear/mover o arquivo baixado para o nome exato da coluna 'file'
        import glob
        baixados = glob.glob(os.path.join(output_dir, f"{tmp_prefix}*"))
        final_path = os.path.join(output_dir, output_filename)
        if baixados:
            # Remove arquivo final se já existir
            if os.path.exists(final_path):
                os.remove(final_path)
            # Move o primeiro arquivo baixado para o nome exato
            os.rename(baixados[0], final_path)
            # Remove arquivos temporários extras, se houver
            for extra in baixados[1:]:
                try:
                    os.remove(extra)
                except Exception:
                    pass
        else:
            print(f"Arquivo baixado temporário não encontrado para {output_filename}")

# Função principal da CLI
def main():
    print("==== CLI Downloader de Vídeos do YouTube ====")
    criar_venv()
    instalar_dependencias()
    instruir_ativacao_venv()
    csvs = listar_csvs()
    selecionados = selecionar_csvs(csvs)
    for csv in selecionados:
        if validar_csv(csv):
            baixar_videos_csv(csv)
        else:
            print(f"Pulando arquivo inválido: {csv}")
    print("\nProcesso finalizado.")

if __name__ == "__main__":
    main() 