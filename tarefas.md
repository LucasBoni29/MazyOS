# Tarefas

> O que tá em jogo agora. Atualizado em 2026-10-09.

## Próxima sessão — criar a conta do TikTok

O conteúdo do Mimesis (shorts 1 e 3) está 100% pronto pra publicar: cortado, legendado,
com thumbnail e legenda de post escritas. **Falta só a conta do TikTok existir.** Lucas vai
pedir apoio numa sessão futura pra criar a conta — tratar como tarefa própria quando ele voltar
com isso.

- [ ] Criar a conta do TikTok do BoniFLY (sessão futura, a pedido do Lucas)
- [ ] Publicar short 1 (mímicos) e short 3 (marretada) assim que a conta existir — arquivos e
  legendas já prontos em `marketing/conteudo/video-mimesis-2026-10-08/`
- [ ] Layout com câmera em cima e gameplay embaixo (print de referência enviado em 2026-10-08) —
  confirmar se o Lucas grava a câmera no OBS e se quer esse formato (não é bloqueante)

## Pronto pra publicar — `marketing/conteudo/video-mimesis-2026-10-08/`

- `short-01-mimicos-legendado.mp4` + capa em `thumb-mimesis-mimicos-2026-10-09/` + legenda em
  `legenda-short-01-mimicos.md`
- `short-03-marretada-legendado.mp4` + capa em `thumb-mimesis-marretada-2026-10-09/` + legenda em
  `legenda-short-03-marretada.md`
- Short 2 (banho) descartado — Lucas não gostou do resultado, não vai ao ar

## Notas técnicas

- Legenda: `scripts/legendar_video.py` (faster-whisper `large-v3-turbo`, CPU). Etapas `transcrever`
  → revisão do `.txt` → `gravar`. Durante os ajustes do short 1 surgiram 3 bugs de timing e os três
  foram corrigidos no script (fica valendo pra sempre, não só pra esse vídeo):
  1. Linha juntada sem palavras reais suficientes do Whisper — tempo virava segundos demais
  2. Busca de palavras "ouvidas" ia longe demais e pegava fala de outra pessoa no meio
  3. Timestamps quase-zero do Whisper (voz sobreposta/ruído) sendo usados como se fossem reais —
     agora tem um filtro de duração mínima por palavra que descarta esse lixo
- Thumbnail sem foto de reação: `scripts/gerar_thumbnail.py` agora aceita rodar só com print +
  texto (foto é opcional via `--foto`) — Lucas ainda não grava webcam
- Moderação TikTok: slur e termo sexual explícito na legenda do short 1 foram suavizados no texto
  (áudio ficou intacto) — "porra/caralho/matar" não é risco, "viado" e conteúdo sexual explícito são
- O player do VS Code não toca áudio AAC — sempre assistir os vídeos fora dele
- No short 3, "Portugal" é como o Whisper ouviu algo (provavelmente o nome de um jogador/apelido)
  — o Lucas revisou e manteve assim, considerar correto

## Feito

- [x] 3 shorts do Mimesis cortados — enquadramento com fundo desfocado (vídeo inteiro, sem corte) aprovado
- [x] Legenda estilo TikTok (palavra fica amarela na fala) integrada no `/editar-video`
- [x] Short 1 (mímicos) legendado, revisado e suavizado pra moderação — aprovado pelo Lucas
- [x] Short 3 (marretada) legendado e revisado — aprovado pelo Lucas
- [x] Short 2 (banho) descartado — Lucas não gostou do resultado
- [x] Thumbnails dos shorts 1 e 3 geradas (sem foto de reação — ainda não grava webcam)
- [x] Legendas de post (texto + hashtags) escritas pros shorts 1 e 3

## Agenda da semana

- [ ] Sábado (10/10) — gravar Stay Close com o amigo (âncora: quem assustar primeiro paga a rodada)
- [ ] Domingo (11/10) — gravar Grain Rot (deixa rolar, descarta se não render)
