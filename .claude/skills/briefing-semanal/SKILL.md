---
name: briefing-semanal
description: >
  Organiza o plano de gravação da semana — quais jogos gravar, o gancho/desafio de cada
  gameplay, e se o foco é vídeo longo pro YouTube ou cortes dinâmicos pro TikTok. Pega ideias
  bagunçadas e devolve um plano único pra semana toda, pra sentar e gravar sem pensar em mais
  nada. Use quando o usuário disser "briefing da semana", "plano de gravação", "o que eu gravo
  essa semana", "organiza minha pauta", ou /briefing-semanal.
---

# /briefing-semanal — Plano de gravação da semana

Não é roteiro engessado. É a definição prévia de jogo + "história"/desafio da gameplay +
plataforma de destino, pra cada sessão de gravação da semana.

## Dependências

- `_memoria/empresa.md` — gêneros favoritos, posicionamento
- `_memoria/preferencias.md` — tom de voz (usar no gancho de cada vídeo)
- `_memoria/estrategia.md` — foco atual (ex: consistência de postagem > qualidade de produção)
- **Output vai em:** `marketing/briefing-semana-<YYYY-MM-DD>.md` (data = segunda-feira da semana)

---

## Workflow

### Passo 1 — Coletar ideias

Perguntar: "Quais jogos/ideias você tá pensando pra essa semana?" — aceitar lista bagunçada,
incompleta, ou só "quero jogar terror de novo, não sei qual". Não exigir que o usuário já
chegue organizado.

### Passo 2 — Organizar em plano

Pra cada gravação da semana, definir:

- **Jogo:** qual título
- **Gancho/desafio:** a "história" daquela gameplay — o que torna esse vídeo específico
  interessante (ex: "tentar passar de um boss usando a pior arma do jogo", "terminar o jogo
  sem usar guia nenhum", "primeira vez jogando às cegas"). Se o usuário não tiver um gancho
  claro, sugerir 1-2 opções com base no jogo escolhido
- **Formato/plataforma:** YouTube longo (gameplay completa) ou corte dinâmico pro TikTok
  (shorts com os melhores momentos)
- **Dia sugerido:** distribuir ao longo da semana, sem overload — considerar que o usuário
  grava fora do expediente (8h-17h é trabalho fixo)

Se o usuário já tiver dias fixos de gravação, respeitar isso. Se não, sugerir uma distribuição
razoável (2-3 sessões de gravação pra semana, por exemplo) e perguntar se funciona.

### Passo 3 — Gerar o documento

Formato do arquivo `marketing/briefing-semana-<data>.md`:

```markdown
# Briefing da semana — <data de início> a <data de fim>

## <Dia da semana> — <Jogo>
**Gancho:** <desafio/história da gameplay>
**Formato:** <YouTube longo | Corte TikTok>
**Notas:** <qualquer observação extra>

## <Dia da semana> — <Jogo>
...
```

### Passo 4 — Entregar

Mostrar o plano completo. Perguntar se tá bom ou se quer ajustar algum dia/gancho antes de
salvar definitivo.

---

## Regras

- Não criar um documento por gravação — sempre um único arquivo cobrindo a semana toda
  (criar atrito por sessão é exatamente o que essa skill existe pra evitar)
- Gancho tem que ser concreto e específico, nunca genérico ("vou jogar e ver o que acontece"
  não é gancho)
- Respeitar o tom de `_memoria/preferencias.md` ao sugerir ganchos — nada de frase roteirizada
  ou clichê de criador genérico
- Se a semana não tiver tema/fio condutor nenhum, tá tudo bem — nem toda semana precisa de
  conceito, só precisa de plano
- Depois de salvar, não é necessário perguntar sobre skill nova ou atualização de memória —
  isso já é o fluxo normal dessa skill
