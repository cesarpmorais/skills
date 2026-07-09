# skills

Fonte da verdade das minhas agent skills. Model-agnostic por design: cada skill é um
`SKILL.md` (markdown + frontmatter YAML), o formato compartilhado por Claude Code, Codex,
Cursor e dezenas de outros coding agents.

## Como os agents usam este repo

Cada agent lê skills de um diretório próprio. Em vez de copiar arquivos, aponto um symlink
pra cá — assim este repo é a única cópia e todo agent enxerga a mesma coisa:

```bash
# Claude Code
ln -s ~/code/skills ~/.claude/skills

# outros agents (ajuste o destino conforme a doc de cada um)
# Codex   → ~/.codex/skills
# Cursor  → ~/.cursor/skills
```

Alternativa (sem symlink): instalar via o package manager do ecossistema —
`npx skills add <owner/repo@skill> -g`.

## Estrutura

```
skills/
  run_evals.py        # runner de evals compartilhado (aponta pra uma skill por nome)
  find-skills/
    SKILL.md
  <skill>/
    SKILL.md          # frontmatter (name, description) + corpo
    references/       # opcional: arquivos que carregam sob demanda
    evals/            # opcional: evals.json (+ results/, gitignorado)
```

Uma skill = uma capacidade. O `SKILL.md` fica enxuto; detalhes longos vão pra `references/`
e só carregam quando o agent precisa.

## Testar uma skill (evals)

O runner é único na raiz; a skill é o argumento. Roda no `claude -p` em Haiku por padrão:

```bash
python3 run_evals.py interviews                    # default: Haiku
python3 run_evals.py interviews --model claude-sonnet-5
python3 run_evals.py interviews --harness-cmd 'codex exec --full-auto {prompt}'
```

Precisa do CLI `claude` logado (`claude` → `/login`) ou outro harness via `--harness-cmd`.
Se o harness quebra (não logado, crash, timeout) o caso é marcado **ERRORED**, nunca
pass/fail — ferramenta quebrada não vira resultado. Cada skill guarda seu `evals/evals.json`
ao lado do `SKILL.md`.

## Skills

- **find-skills** — descobrir e instalar skills do ecossistema aberto (`npx skills`).
- **interviews** — antes de um build não-trivial, entrevista você para travar as decisões que mudam a arquitetura.
- **slidev** — criar e apresentar slide decks técnicos com Slidev (markdown + Vue). Instalada de `slidevjs/slidev` (oficial).

## Princípios

- **Tudo em inglês.** Toda skill deste repo é escrita em inglês (frontmatter e corpo); este README fica em PT.
- **A description é o que dispara a skill.** Escreva o quê / quando / quando NÃO usar.
- **Enxuto.** Objetivos e restrições, não um passo-a-passo que engessa o agent.
- **Escrita por humano.** O draft pode nascer de uma conversa, mas quem decide o conteúdo
  sou eu — skill ruim codifica um processo ruim pra sempre.
