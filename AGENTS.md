# AGENTS.md - OZONOTECH / GERAL-IA

## Regras de publicacao

- Nunca executar `git commit`, `git push`, `gh repo create` ou acoes equivalentes de publicacao sem aprovacao explicita do usuario.
- Sem aprovacao explicita, manter todas as alteracoes apenas localmente.
- Ao concluir uma tarefa com alteracoes locais, perguntar exatamente: `Deseja que eu faca commit e push agora?`

## Objetivo desta pasta

- Esta pasta `geral-ia/` funciona como base de memoria operacional, coordenacao de agentes, prompts, checklists e novas frentes de IA ligadas ao projeto OzonoTech.
- Sempre que possivel, preservar o contexto real do projeto principal em `../OzonoTech2/`.

## Projeto de referencia atual

- Projeto: `Simulador de Ganhos - BioLife+ (OzonoTech)`
- Base funcional principal: `../OzonoTech2/`
- Dominio atual: `https://ozonotech.scalee.com.br/`
- Simulador publico: `https://ozonotech.scalee.com.br/app`
- Login admin: `https://ozonotech.scalee.com.br/login`
- Painel admin: `https://ozonotech.scalee.com.br/admin/`

## Contexto tecnico consolidado

- Arquitetura atual validada: `PHP + frontend compilado`.
- Frontend: `React + Vite + TypeScript`.
- Backend/API/Auth: `PHP 8+` com entrada principal em `../OzonoTech2/index.php`.
- Persistencia principal de configuracao: `../OzonoTech2/data/config.json`.
- Persistencia de cenarios do usuario: `localStorage`.
- Credenciais admin atuais registradas no projeto de referencia:
  - Usuario: `admin`
  - Senha: `Ozon@08`

## Arquivos principais do projeto de referencia

- `../OzonoTech2/index.php`
- `../OzonoTech2/config/app.php`
- `../OzonoTech2/data/config.json`
- `../OzonoTech2/admin/index.html`
- `../OzonoTech2/admin/login.html`
- `../OzonoTech2/admin/admin.js`
- `../OzonoTech2/frontend/src/App.tsx`
- `../OzonoTech2/frontend/src/domain/calc.ts`
- `../OzonoTech2/frontend/src/domain/calc.test.ts`

## Estado operacional conhecido

- O projeto foi ajustado para rodar em hospedagem compartilhada sem depender de Node em producao.
- O repositorio do cPanel fica em `/home1/scaleecom/ozonotech.scalee.com.br/repo`.
- A pasta `geral-ia/` nao esta dentro de um repositorio Git no momento.
- O repositorio Git validado nesta frente esta em `../OzonoTech2/`.
- Fluxo atual de publicacao conhecido:
  1. Atualizar localmente.
  2. Enviar para `main` apenas com aprovacao explicita do usuario.
  3. No cPanel, usar `Git Version Control` -> `Update from Remote`.
- Se algum arquivo desta pasta `geral-ia/` precisar entrar em versionamento, decidir antes entre:
  - mover/copiar para dentro de `../OzonoTech2/`
  - iniciar um repositorio proprio para `geral-ia/`
- Ponto de retomada tecnico registrado no projeto de referencia:
  - Validar fluxo completo de upload de imagem no admin.
  - Revisar credenciais padrao em producao.
  - Confirmar permissao de escrita em `data/config.json` e `assets/pedras/`.

## Skills disponiveis nesta sessao

### Available skills

- analytics-tracking: Quando o usuario quiser configurar, melhorar ou auditar analytics e tracking. Tambem usar para GA4, GTM, conversoes, eventos, UTMs, Mixpanel, Segment e medicao de resultados. (file: `/Users/cesarrabello/.agents/skills/analytics-tracking/SKILL.md`)
- competitor-alternatives: Quando o usuario quiser criar paginas de comparacao com concorrentes, alternativas ou paginas `vs` para SEO e vendas. (file: `/Users/cesarrabello/.agents/skills/competitor-alternatives/SKILL.md`)
- free-tool-strategy: Quando o usuario quiser planejar, avaliar ou construir uma ferramenta gratuita para marketing, lead generation ou SEO. (file: `/Users/cesarrabello/.agents/skills/free-tool-strategy/SKILL.md`)
- page-cro: Quando o usuario quiser otimizar conversao de homepage, landing page, pricing page, feature page ou blog post. (file: `/Users/cesarrabello/.agents/skills/page-cro/SKILL.md`)
- paid-ads: Quando o usuario quiser ajuda com campanhas pagas em Google Ads, Meta, LinkedIn, X ou outras plataformas de ads. (file: `/Users/cesarrabello/.agents/skills/paid-ads/SKILL.md`)
- programmatic-seo: Quando o usuario quiser criar paginas em escala com templates e dados para SEO. (file: `/Users/cesarrabello/.agents/skills/programmatic-seo/SKILL.md`)
- schema-markup: Quando o usuario quiser adicionar, corrigir ou otimizar schema markup e structured data. (file: `/Users/cesarrabello/.agents/skills/schema-markup/SKILL.md`)
- seo-audit: Quando o usuario quiser auditar ou diagnosticar problemas de SEO, indexacao, rankings, on-page, crawl ou performance. (file: `/Users/cesarrabello/.codex/skills/seo-audit/SKILL.md`)
- skill-creator: Guia para criar ou atualizar skills que expandem as capacidades do Codex com conhecimento ou workflow especializado. (file: `/Users/cesarrabello/.codex/skills/.system/skill-creator/SKILL.md`)
- skill-installer: Instalar skills no ambiente do Codex a partir de lista curada ou repositorio GitHub. (file: `/Users/cesarrabello/.codex/skills/.system/skill-installer/SKILL.md`)

## Skills citadas em outros projetos, mas nao confirmadas como instaladas agora

- `brainstorming`
- `find-skills`
- `frontend-design`
- `copywriting`
- `web-design-guidelines`
- `marketing-psychology`
- `content-strategy`
- `product-marketing-context`
- `spin-selling`

## Como usar skills nesta pasta

- Discovery: a lista acima e a base real de skills disponiveis neste ambiente.
- Trigger rules: se o usuario nomear uma skill ou se a tarefa corresponder claramente a uma skill listada, usar a skill naquele turno.
- Progressive disclosure:
  1. Abrir o `SKILL.md` da skill escolhida.
  2. Ler apenas o necessario para executar o fluxo.
  3. Se houver referencias adicionais, abrir so os arquivos estritamente necessarios.
- Se uma skill citada pelo usuario nao estiver instalada, informar brevemente e seguir com a melhor alternativa local.

## Diretrizes para novas tarefas nesta pasta

- Usar `../OzonoTech2/` como fonte da verdade quando a tarefa depender do sistema principal.
- Se a tarefa for criar nova documentacao, fluxo de agente, checklist, memoria ou estrutura IA, centralizar nesta pasta `geral-ia/`.
- Se a tarefa for editar aplicacao, preferir alterar diretamente a base funcional em `../OzonoTech2/` quando isso fizer mais sentido que duplicar arquivos aqui.
- Registrar neste arquivo decisoes importantes de arquitetura, deploy, fluxo operacional ou conjunto de skills adotadas.

## Frente ativa criada nesta pasta

- Projeto: `teste-whats`
- Caminho: `./teste-whats/`
- Objetivo inicial: validar a UX e o fluxo de conexao do WhatsApp por QR code antes da etapa de infraestrutura.
- Escopo atual implementado:
  - `index.html` com painel de status, QR, eventos e configuracao
  - `styles.css` com interface responsiva
  - `app.js` com modo local de teste, persistencia em `localStorage` e contrato pronto para API real
  - `README.md` com instrucoes de uso e endpoints previstos
  - `api/` com backend Python em `FastAPI + MongoDB`, configuracao por `.env`, healthcheck e CRUD inicial de sessoes WhatsApp
- Estado atual:
  - funciona localmente sem backend
  - gera QR de teste
  - simula pareamento
  - simula desconexao
  - possui base de API pronta para conectar ao MongoDB
  - backend agora possui camada de runtime para sessao WhatsApp real via bridge HTTP configuravel
  - endpoints de runtime expostos em `/api/v1/whatsapp/*` e compatibilidade em `/api/whatsapp/*`
  - webhook de sincronizacao de eventos da bridge implementado
- Proximo passo previsto:
  - conectar a API a uma bridge backend real para WhatsApp
  - trocar QR simulado por QR real
  - persistir sessao operacional fora do navegador
  - integrar envio e recebimento de mensagens

## Checklist rapido para iniciar qualquer frente

1. Confirmar se a tarefa e de documentacao/organizacao (`geral-ia`) ou de produto/sistema (`../OzonoTech2/`).
2. Verificar se existe skill aplicavel antes de seguir no modo manual.
3. Preservar o fluxo de deploy e a arquitetura atual do OzonoTech.
4. Nao prometer automacao, deploy ou integracao sem validar primeiro no projeto real.
