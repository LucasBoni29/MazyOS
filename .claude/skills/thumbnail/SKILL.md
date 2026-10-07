---
name: thumbnail
description: >
  Monta a thumbnail do vídeo combinando print da gameplay + foto de reação (fundo removido
  automaticamente via rembg) + texto curto de impacto. Gera as duas versões de uma vez:
  16:9 pra YouTube e 9:16 pra TikTok/Shorts. Use quando o usuário disser "cria a thumbnail",
  "faz a capa do vídeo", "monta a thumb", ou /thumbnail.
---

# /thumbnail — Capa do vídeo (YouTube + TikTok)

Pega print + foto normal + texto → entrega as duas thumbnails já prontas, sem o usuário
precisar recortar nada na mão.

## Dependências

- **Pillow** (`pip install Pillow`)
- **rembg com backend CPU** (`pip install "rembg[cpu]"`) — remove o fundo da foto automaticamente.
  **Atenção:** só `pip install rembg` (sem `[cpu]`) instala sem o `onnxruntime` e falha em runtime
  com "No onnxruntime backend found" — sempre usar a variante `[cpu]`
- **Script:** `scripts/gerar_thumbnail.py`
- **Outputs vão em:** `marketing/conteudo/thumb-<tema>-<YYYY-MM-DD>/`

Checar se as libs estão instaladas antes de rodar (`python -c "import PIL, rembg"`). Se faltar
alguma, mostrar a instalação (seção abaixo) e parar — não seguir sem elas.

---

## Workflow

### Passo 1 — Coletar input

Perguntar (ou já receber):

1. Print marcante da gameplay (momento engraçado/chocante)
2. Foto normal do usuário com a expressão de reação — **não precisa já vir recortada**,
   o script remove o fundo sozinho
3. Texto de impacto, até 3 palavras (ex: "ISSO É REAL?", "SAÍ CORRENDO")
4. Tema/jogo, pra nomear a pasta

Se o texto vier mais longo que 3-4 palavras, sugerir um corte mais curto antes de gerar
(thumbnail precisa ser lida em menos de 1 segundo).

### Passo 2 — Gerar

```bash
python scripts/gerar_thumbnail.py "<print>" "<foto>" "TEXTO" "marketing/conteudo/thumb-<tema>-<data>/"
```

Isso gera `thumbnail-youtube.png` (1280x720) e `thumbnail-tiktok.png` (1080x1920) na pasta.

### Passo 3 — Mostrar e ajustar

Mostrar as duas imagens geradas. Se o usuário quiser ajustar (posição da foto, tamanho do
texto, cor), editar os parâmetros do script pra esse caso específico — não precisa reescrever
o script inteiro, só os valores daquela chamada.

---

## Instalar dependências (Windows)

```powershell
pip install Pillow "rembg[cpu]"
```

A primeira execução do `rembg` baixa um modelo de IA (~175MB) pra remoção de fundo — precisa
de internet na primeira vez, depois funciona offline. Se o `pip install rembg` falhar por
incompatibilidade de versão do Python, avisar o usuário e sugerir um ambiente virtual com
Python 3.11 ou 3.12 (`py -3.11 -m venv venv`) como alternativa.

---

## Regras

- Nunca usar foto de outra pessoa sem o usuário confirmar que é ele mesmo na imagem
- Texto sempre em caixa alta, curto, com contorno grosso (legibilidade em miniatura é prioridade)
- Sempre gerar as duas versões (YouTube + TikTok) juntas, mesmo que o usuário só peça uma —
  é praticamente o mesmo processo e evita ele pedir a outra depois
- Quando `identidade/design-guide.md` tiver cores/fontes definidas, usar elas no texto da
  thumbnail em vez do branco/preto padrão
- Salvar sempre em `marketing/conteudo/thumb-<tema>-<data>/`
