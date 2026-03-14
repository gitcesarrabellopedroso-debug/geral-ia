# Teste Whats Bridge

Bridge local self-hosted para conectar o `teste-whats` ao WhatsApp Web sem SaaS de terceiros.

## Stack

- Node.js
- Express
- Baileys
- QRCode

## Endpoints

- `GET /health`
- `POST /sessions/:sessionKey/start`
- `GET /sessions/:sessionKey`
- `POST /sessions/:sessionKey/disconnect`

## Rodando localmente sem Docker

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats/bridge
cp .env.example .env
npm install
npm start
```

Bridge:

- `http://localhost:8081`

## Rodando com Docker Compose

Use o `docker compose` da raiz de `teste-whats`. Ele sobe:

- MongoDB
- API Python
- Bridge local do WhatsApp

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats
docker compose up --build
```

## Fluxo esperado

1. A bridge inicia ou reabre a sessao do WhatsApp.
2. O QR real e devolvido como `qr_image_data_url`.
3. A API Python consulta esta bridge.
4. O frontend exibe o QR real em modo `API externa`.

## Observacoes

- A autenticacao da sessao fica em `./data/auth` no modo local.
- No Docker, o estado da sessao fica no volume `teste_whats_bridge_auth`.
- `disconnect` limpa a autenticacao local para forcar novo pareamento no proximo `start`.
