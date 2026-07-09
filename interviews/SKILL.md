---
name: interviews
description: Antes de implementar qualquer feature, sistema ou refactor não-trivial, entreviste o usuário primeiro para expor as decisões que mudariam a arquitetura. Acione quando o usuário pedir para construir, projetar ou arquitetar algo cujo formato ainda não está definido ("crie um app que...", "como estruturar Y", "adiciona a feature Z"). Priorize perguntas que mudam o design, não as cosméticas; pare assim que as decisões de arquitetura estiverem resolvidas. NÃO acione para edições pequenas, correção de bugs, perguntas simples, ou quando o usuário já definiu a arquitetura ou disse para só construir.
---

# Interviews

Antes de construir algo não-trivial, faça uma entrevista curta. O objetivo não é
coletar requisitos — é encontrar as poucas decisões que mudariam a arquitetura se
respondidas de outro jeito, e resolvê-las antes de escrever qualquer código.

Uma pergunta que muda a arquitetura vale por dez cosméticas.

## Quando entrar

Entre quando o usuário pedir para construir, projetar, refatorar ou arquitetar algo
cujo formato ainda não está decidido.

Pule quando:

- A mudança é pequena, mecânica ou uma correção de bug.
- O usuário já descreveu a arquitetura, ou disse para só construir.
- A resposta está no código — leia o repo em vez de perguntar.

Na dúvida se vale entrevistar, faça uma única pergunta: *"Quer que eu te entreviste
rápido antes de construir, ou já está claro?"*

## Como conduzir

### 1. Lote inicial

Faça 4-6 perguntas de uma vez para mapear o terreno. Puxe-as para as decisões que
bifurcam o design. Bom território:

- **Dados e estado** — qual é a fonte da verdade, quem é dono do estado, qual o formato do modelo central.
- **Fronteiras** — o que está dentro vs fora do escopo, o que conversa com o quê, síncrono vs assíncrono.
- **Restrições que amarram o design** — escala, latência, offline, custo, sistemas existentes nos quais encaixar.
- **Falha e ciclo de vida** — o que acontece quando quebra, como é deployado, quem mantém.
- **Construir vs comprar** — já existe ferramenta/skill/lib que elimina a necessidade de construir.

Pule o que dá pra inferir do repo ou do pedido. Não pergunte sobre cores, nomes ou
detalhes baratos de mudar depois.

### 2. Follow-ups

Leia as respostas. Onde uma resposta abre uma bifurcação de arquitetura, aprofunde
uma pergunta — uma de cada vez, adaptando ao que foi dito. Persiga só os fios que
mudam o design.

### 3. Pare quando a arquitetura estiver travada

Pare assim que as decisões que mudariam o design estiverem resolvidas. Não encha a
entrevista com perguntas de baixo valor. Ao parar, diga que parou e vá para a saída.

## Saída

Siga a convenção do projeto:

- Repo usa **specs** (`specs/`, `spec/`) → escreva as decisões como spec nesse formato.
- Repo usa **ADRs** (`docs/adr/`, `decisions/`, `*/adr/`) → escreva um ADR.
- Nenhum dos dois → dê um recap curto das decisões de arquitetura no chat.

Detecte a convenção olhando o repo antes de escolher. Na dúvida, pergunte qual o
usuário prefere.
