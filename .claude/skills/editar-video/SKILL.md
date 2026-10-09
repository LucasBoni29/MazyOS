---
name: editar-video
description: >
  Corta e monta o vídeo final a partir do raw do OBS + uma lista de timestamps dos melhores
  momentos (anotados no papel). Usa ffmpeg pra cortar cada trecho e concatenar num vídeo só,
  pronto pra publicar — sem passos intermediários pro usuário. Use quando o usuário disser
  "edita esse vídeo", "corta esses momentos", "monta o vídeo do OBS", "já tenho os timestamps",
  ou /editar-video.
---

# /editar-video — Corte e montagem automática

Tira o trabalho braçal da edição: o usuário já sabe os melhores momentos (anotou no papel),
essa skill só precisa cortar e juntar.

## Dependências

- **ffmpeg** instalado e no PATH. Checar com `ffmpeg -version` antes de rodar qualquer coisa.
  Se não encontrar, parar e mostrar o passo a passo de instalação (ver seção abaixo) —
  não tentar contornar de outra forma.
- **Python 3** (já vem com o projeto)
- **faster-whisper** (`pip install faster-whisper`) — só pra etapa de legenda. Primeira execução
  baixa o modelo (~1.6GB)
- **Script:** `scripts/cortar_video.py`
- **Outputs vão em:** `marketing/conteudo/video-<tema>-<YYYY-MM-DD>/`

---

## Workflow

### Passo 1 — Coletar input

Perguntar (ou já receber, se o usuário colou tudo de uma vez):

1. Caminho do arquivo raw (o .mkv/.mp4 que saiu do OBS)
2. Os timestamps dos melhores momentos — aceitar no formato livre que o usuário mandar
   (ex: "12:30 até 13:10, depois 25:00 até 26:45") e eu mesmo normalizo pro formato do script
3. É pra YouTube (formato original, 16:9) ou short vertical pro TikTok (9:16)? Se o usuário
   não especificar, perguntar — isso decide a flag `--vertical`
4. Qual o tema/jogo do vídeo, pra nomear a pasta de saída

### Passo 2 — Checar ffmpeg

Rodar `ffmpeg -version`. Se falhar, mostrar a instalação (seção "Instalar ffmpeg" abaixo) e parar
aqui — não seguir sem a ferramenta.

### Passo 3 — Normalizar timestamps

Escrever um arquivo temporário `timestamps.txt` com uma linha por trecho, formato `inicio - fim`
(`HH:MM:SS` ou `MM:SS`), na pasta de saída do vídeo.

### Passo 4 — Cortar e montar

```bash
python scripts/cortar_video.py "<raw>" "marketing/conteudo/video-<tema>-<data>/timestamps.txt" "marketing/conteudo/video-<tema>-<data>/final.mp4" [--vertical]
```

Mostrar o progresso e o resultado (duração final, caminho do arquivo).

### Passo 5 — Legenda (opcional, recomendado pra TikTok)

Legenda estilo TikTok: palavra em branco que fica amarela no momento da fala, abaixo da gameplay.
Usa `scripts/legendar_video.py` (faster-whisper, modelo `large-v3-turbo`, roda local na CPU).

1. Transcrever o vídeo já cortado:
   ```bash
   python scripts/legendar_video.py transcrever "<pasta>/<short>.mp4"
   ```
   Gera `<short>.legenda.txt` (uma linha por bloco: `[mm:ss.cc - mm:ss.cc] texto`)
2. **CHECKPOINT:** mostrar o `.txt` pro usuário e pedir que ele corrija. Os gameplays têm
   várias pessoas falando ao mesmo tempo + som do jogo + gíria, então sempre vai ter erro.
   Ele pode corrigir palavras, apagar linhas ou ajustar tempos — nunca gravar sem essa revisão
3. Gravar a legenda:
   ```bash
   python scripts/legendar_video.py gravar "<pasta>/<short>.mp4"
   ```
   Gera `<short>-legendado.mp4` — o vídeo sem legenda continua intacto

### Passo 6 — Confirmar

Avisar que o vídeo final está pronto e perguntar se o usuário quer revisar antes de considerar
publicável, ou se já pode seguir pra thumbnail / publicação.

---

## Instalar ffmpeg (Windows)

```powershell
winget install Gyan.FFmpeg
```

Depois, **fechar e abrir o terminal de novo** (o PATH só atualiza em sessão nova) e confirmar:

```powershell
ffmpeg -version
```

Se o `winget` não estiver disponível, baixar o build em https://www.gyan.dev/ffmpeg/builds/
(pasta `ffmpeg-release-essentials`), extrair, e adicionar a subpasta `bin` ao PATH do Windows.

---

## Regras

- Nunca inventar timestamps — só usar os que o usuário passou
- Nunca descartar o raw original — o script só lê, nunca sobrescreve o arquivo de entrada
- Sempre perguntar o formato (YouTube vs TikTok vertical) se não estiver claro
- Se o corte resultar em um vídeo muito curto (<5s) ou muito longo pro formato (ex: >3min pra
  um "short"), avisar o usuário antes de finalizar
- Salvar sempre em `marketing/conteudo/video-<tema>-<data>/`, seguindo o padrão do resto do MazyOS
