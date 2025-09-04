# YouTube Downloader

Baixe vídeos do YouTube em massa a partir de arquivos CSV, com ambiente Python isolado e interface interativa.

## Como usar

1. **Clone o repositório:**
   ```sh
   git clone git@github.com:realmcastro/youtube_downloader.git
   cd youtube_downloader
   ```

2. **Coloque seus arquivos CSV na pasta do projeto.**
   - O CSV deve ter as colunas `link` (URL do vídeo) e `file` (nome final do arquivo).

3. **Execute o script de download:**
   ```sh
   bash baixar_videos.sh
   ```
   - O script cria o ambiente virtual, instala as dependências e inicia a interface interativa.

4. **Siga as instruções na tela para selecionar os arquivos CSV e baixar os vídeos.**

---

- Os vídeos baixados vão para a pasta `videos/`.
- O nome do arquivo final será exatamente o da coluna `file` do CSV. 