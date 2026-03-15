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

## Estado Meta / WhatsApp consolidado

- Portifolio principal para operacao real: `BWS`.
- Conta principal de WhatsApp em uso dentro de `BWS`: `UZA Multinivel`.
- Numero real confirmado em uso: `+55 19 99727-5276`.
- Status atual da conta principal do WhatsApp em `BWS`: `Verificado` e `Aprovado`.
- App tecnico principal ligado a essa operacao: `Scalle_wpp`.
- Conta de teste mantida em `BWS`: `Test WhatsApp Business Account`.
- Portifolio `BWS UZA multinivel`: tratado como ambiente de teste/legado e nao como base principal de operacao.
- Portifolio `UZA Multinivel`: tratado como legado/revisao; nao usar como base operacional principal ate limpeza futura.
- Regra operacional definida:
  - operar manualmente a partir de `BWS`
  - tratar `BWS UZA multinivel` apenas como teste enquanto existir
  - nao tomar decisoes estruturais usando `UZA Multinivel` sem revisao item a item
- Nome de exibicao do numero principal `+55 19 99727-5276`:
  - `UZA Multinivel` foi rejeitado
  - novo nome enviado para revisao: `Uza`
  - envio do novo nome nao derrubou o funcionamento do numero; status observado apos mudanca: `Em analise`
- Integracao Meta / Cloud API:
  - dados minimos necessarios da Meta: `Phone Number ID`, `WABA ID`, `Access Token`, `App ID`, `App Secret`
  - dados definidos no sistema integrador: `Webhook URL`, `Verify Token`
  - para operacao real, considerar rotacao de `Access Token` e revisao de acessos do app se houver ex-responsavel com permissao

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
- Todo novo projeto local com backend/container deve ficar isolado dos demais:
  - pasta propria
  - `docker-compose.yml` proprio
  - containeres com prefixo do projeto
  - banco/volume proprio por projeto
  - nunca compartilhar banco ou volume entre projetos diferentes, salvo decisao explicita do usuario

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
  - stack Docker local criada com `docker-compose.yml` para `api + mongo`
  - isolamento local definido por projeto: `teste-whats` usa containeres e volumes proprios, sem compartilhar banco com outras frentes
- Proximo passo previsto:
  - conectar a API a uma bridge backend real para WhatsApp
  - trocar QR simulado por QR real
  - persistir sessao operacional fora do navegador
  - integrar envio e recebimento de mensagens

## Ponto de retomada atual

- Repositorio `geral-ia` inicializado e publicado no GitHub:
  - remoto: `https://github.com/gitcesarrabellopedroso-debug/geral-ia.git`
  - branch atual: `master`
- Ultimos commits publicados:
  - `8281490` - `feat: add whatsapp runtime backend integration layer`
  - `3ed1e4e` - `feat: add local docker stack for teste-whats api`
- Estado atual de `teste-whats`:
  - frontend local pronto em `./teste-whats/`
  - API Python pronta em `./teste-whats/api/`
  - runtime de sessao WhatsApp exposto em `/api/v1/whatsapp/*`
  - compatibilidade adicional em `/api/whatsapp/*`
  - MongoDB local previsto no `docker-compose.yml`
  - bridge local self-hosted adicionada em `./teste-whats/bridge/` usando `Node.js + Baileys`
  - stack local validada com tres servicos: `teste-whats-api`, `teste-whats-bridge`, `teste-whats-mongo`
  - frontend atualizado para renderizar `qr_image_data_url` real e usar `http://localhost:8000` por padrao no modo API
  - endpoint de envio real de mensagem implementado localmente em `POST /api/whatsapp/messages/send`
- Como subir localmente na retomada:
  1. entrar em `./teste-whats/`
  2. rodar `docker compose up --build`
  3. acessar `http://localhost:8000/docs`
  4. abrir `./teste-whats/index.html`
  5. selecionar `API externa`
  6. usar `http://localhost:8000`
  7. iniciar sessao para gerar QR real via bridge local
- Proximo passo tecnico ao retomar:
  - decidir entre manter a bridge local apenas para testes ou migrar a integracao para `WhatsApp Cloud API`
  - se seguir com a stack local, validar envio real apos pareamento com numero de teste adequado
  - se migrar para Cloud API, levantar `Phone Number ID`, `WABA ID`, `Access Token`, `App ID` e `App Secret` em `Scalle_wpp`

## Playbook Meta / WhatsApp

- Documento operacional dedicado: `./meta-whatsapp-playbook.md`
- Estrutura principal validada na Meta:
  - portfolio principal: `BWS`
  - conta do WhatsApp principal: `UZA Multinivel`
  - numero real atual: `+55 19 99727-5276`
  - app principal: `Scalle_wpp`
  - system user tecnico atual: `scalee_api_2`
- Dados tecnicos ja levantados:
  - `Phone Number ID`: `926220003913113`
  - `WABA ID`: `1241971824445557`
  - `App ID`: `1536921637532151`
  - `Verify Token` definido para a futura aplicacao: `scalee_whatsapp_20260314`
  - `Access Token` atual valido deve ser o gerado no `scalee_api_2`
- Regra operacional atual:
  - operar no portfolio `BWS`
  - usar `UZA Multinivel` para numeros reais
  - manter `Test WhatsApp Business Account` apenas como teste
  - deixar `BWS UZA multinivel` parado por enquanto
  - deixar `UZA Multinivel` legado/congelado para revisao futura
  - considerar `uza_app` como legado; tokens antigos revogados
- Fluxo padrao daqui para frente:
  - novo numero: adicionar no `BWS`, verificar, revisar display name, pegar `Phone Number ID`, testar envio
  - novo cliente: decidir se entra no `BWS` temporariamente ou em portfolio proprio
  - novo portfolio: criar separado, nomear corretamente e so depois preparar WhatsApp
- Importante:
  - o `Webhook URL` final deve ser da propria aplicacao
  - o `Webhook URL` antigo `https://webhook.scalee.com.br/webhook/b58c422d-6251-43f4-a40b-85bdf1d456ab/webhook` nao deve ser tratado como definitivo sem controle do backend
  - o webhook antigo em `webhook.scalee.com.br` nao deve ser tratado como base definitiva se nao houver controle do backend
  - na Meta, o campo `messages` ja ficou assinado no webhook atual
  - para receber mensagens automaticamente ainda falta criar a rota de webhook na aplicacao e sincronizar com a Meta

## Checklist rapido para iniciar qualquer frente

1. Confirmar se a tarefa e de documentacao/organizacao (`geral-ia`) ou de produto/sistema (`../OzonoTech2/`).
2. Verificar se existe skill aplicavel antes de seguir no modo manual.
3. Preservar o fluxo de deploy e a arquitetura atual do OzonoTech.
4. Nao prometer automacao, deploy ou integracao sem validar primeiro no projeto real.
