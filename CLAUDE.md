# MazyOS — Sistema operacional do negócio

Sua empresa roda em cima desse arquivo. Aqui ficam as regras de operação
do MazyOS — como o Claude lê o contexto, aprende com correções, mantém
tudo atualizado e cria skills novas conforme a operação evolui.

Esse arquivo é editável. Quando o `/instalar` rodar, ele complementa o
final dessa página com as regras específicas do seu negócio.

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (quando existirem
e estiverem preenchidos):

1. `_memoria/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_memoria/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_memoria/estrategia.md` — foco atual, prioridades, prazos

Usar essas informações como base pra qualquer resposta ou decisão. Ao
sugerir prioridades, formatos ou abordagens, considerar o foco atual
descrito em `estrategia.md`.

Pra qualquer tarefa visual (carrossel, post, landing page), consultar
`identidade/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas
usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe skill relevante
em `.claude/skills/`. Se encontrar, seguir as instruções da skill. Se
não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o
usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o
padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma
instrução que parece permanente (frases como "na verdade é assim", "não
faça mais isso", "prefiro assim", "sempre que...", "evita...", "da
próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (clientes, serviços, mercado) → `_memoria/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato, o que evitar) → `_memoria/preferencias.md`
- **Sobre prioridades e foco** (projetos, metas, prazos) → `_memoria/estrategia.md`
- **Regra de comportamento nessa pasta** → próprio `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro.
Confirmar mostrando a linha adicionada.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na
verdade o arquivo se chama X"). Só perguntar quando a informação tiver
valor duradouro.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante (cliente novo, skill
nova, mudança de foco, processo novo, ferramenta instalada, estrutura
alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize a memória?"

Se sim, identificar o que atualizar:

- **Cliente, serviço, ferramenta, equipe** → `_memoria/empresa.md`
- **Mudança de prioridade ou foco** → `_memoria/estrategia.md`
- **Tom ou estilo** → `_memoria/preferencias.md`
- **Pasta, regra de organização, skill criada** → `CLAUDE.md`
- **Visual (cores, fontes, logo)** → `identidade/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo
inteiro, só adicionar ou editar a linha relevante.

**Quando NÃO perguntar:**
- Tarefas pontuais sem impacto no contexto (escrever um email avulso, criar um post)
- Perguntas simples ou conversas sem ação
- Mudanças já salvas pelo bloco "Aprender com correções"

**Dica:** rode `/atualizar` pra uma varredura completa quando houver dúvida.

---

## Criação de skills

Quando o usuário pedir skill nova:

1. Verificar se existe template relevante em `templates/skills/`. Se
   existir, usar como base e adaptar pro contexto
2. Perguntar se é específica desse projeto ou útil em qualquer:
   - Específica → `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Universal → `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_memoria/empresa.md` e `_memoria/preferencias.md` pra calibrar
   o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, exemplos),
   criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code

---

## BoniFLY — perfil do negócio

> Preenchido pelo `/instalar`.

### O que é esse workspace

Operação de conteúdo do BoniFLY — marca pessoal de criador de conteúdo gamer no TikTok. Aqui Lucas produz, edita e publica shorts de jogos (terror, FPS, RPG) com reações exageradas, em paralelo ao trabalho full-time como desenvolvedor Full Stack.

**Estrutura de pastas:**
- `_memoria/` — quem é o Lucas/BoniFLY, como fala, o que tá em foco agora
- `identidade/` — cores, fontes, logo, padrão visual (ainda em branco)
- `marketing/` — conteúdo, legendas, roteiros (saída das skills)
- `saidas/` — análises, documentos pontuais
- `dados/` — arquivos a analisar (CSV, PDF, planilha)
- `scripts/` — utilitários (gerar imagem, postar, render)
- `tarefas.md` — o que tá em jogo agora

### Quem é

Lucas, também conhecido como **BoniFLY**. Desenvolvedor Full Stack de dia (08h-17h), criador de conteúdo gamer fora do expediente — sozinho, com apoio de IA pra edição. Grava com OBS Studio.

### O que produz

- Shorts de TikTok jogando terror, FPS e RPG, com reações exageradas ("noia jogando")

### Audiência

Ainda no zero — construindo do início. Público-alvo: pessoas que curtem rir vendo bagunça, surto de raiva e reação exagerada em jogo de terror; parte quer jogar junto com ele por ser divertido.

### Tom de voz

Informal, direto, humor ácido e autodepreciativo, palavrão leve pra dar ênfase. Ver exemplos completos em `_memoria/preferencias.md`.

Evitar: clichê motivacional, abertura padrão de criador genérico, qualquer coisa que soe roteirizada.

### Posicionamento

Autenticidade acima de produção polida — o diferencial do BoniFLY é parecer real, não um canal "profissional" de games. Novo no ramo, ainda competindo mentalmente com veteranos (Alanzoka, Coringa, Bistecone, LuanGameplay), mas a aposta é a reação genuína, não a comparação direta.

### Regras do sistema

- Conteúdo novo salvar em `marketing/conteudo/<tipo>-<tema>-<data>/`
- Skills ativas pro fluxo de produção: `/editar-video` (corta raw do OBS via ffmpeg a partir
  de timestamps), `/thumbnail` (monta capa YouTube+TikTok via Pillow/rembg), `/briefing-semanal`
  (plano de gravação da semana)

### Ferramentas conectadas

- [x] OBS Studio (gravação)
- [x] Edição automatizada local — ffmpeg (`/editar-video`) + Pillow/rembg (`/thumbnail`)
- [ ] TikTok (conta em criação)
