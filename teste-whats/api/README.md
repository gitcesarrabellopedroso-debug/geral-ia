# Teste Whats API

API em Python com FastAPI + MongoDB, estruturada para evoluir junto da frente `teste-whats`.

## Stack

- FastAPI
- PyMongo Async
- Pydantic Settings
- MongoDB

## Estrutura

- `app/main.py`: ponto de entrada da aplicacao
- `app/core/config.py`: configuracoes da aplicacao
- `app/core/database.py`: conexao e bootstrap do MongoDB
- `app/api/v1/endpoints/`: rotas versionadas
- `app/repositories/`: acesso a dados
- `app/schemas/`: contratos HTTP

## Rodando localmente

### Opcao mais simples com Docker

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats
docker compose up --build
```

Servicos:

- API: `http://localhost:8000`
- Docs Swagger: `http://localhost:8000/docs`
- MongoDB: `mongodb://localhost:27017`

### 1. Subir MongoDB

```bash
docker run -d --name teste-whats-mongo -p 27017:27017 mongo:7
```

### 2. Configurar ambiente

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats/api
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### 3. Executar a API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Derrubar containers locais

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats
docker compose down
```

## Endpoints iniciais

- `GET /api/v1/health`
- `POST /api/v1/whatsapp-sessions`
- `GET /api/v1/whatsapp-sessions`
- `GET /api/v1/whatsapp-sessions/{session_id}`
- `PATCH /api/v1/whatsapp-sessions/{session_id}`
- `DELETE /api/v1/whatsapp-sessions/{session_id}`
- `GET /api/v1/whatsapp/status`
- `POST /api/v1/whatsapp/session/start`
- `POST /api/v1/whatsapp/session/disconnect`
- `POST /api/v1/whatsapp/webhooks/session-events`

Compatibilidade com o frontend atual:

- `GET /api/whatsapp/status`
- `POST /api/whatsapp/session/start`
- `POST /api/whatsapp/session/disconnect`
- `POST /api/whatsapp/webhooks/session-events`

## Bridge real do WhatsApp

Esta API agora ja suporta um fluxo de bridge externa para WhatsApp real. O backend Python:

- recebe a chamada do frontend
- consulta ou inicia a sessao via bridge HTTP
- persiste o estado da sessao no MongoDB
- devolve status, QR e metadados para a interface

Variaveis novas:

- `WHATSAPP_BRIDGE_ENABLED`
- `WHATSAPP_BRIDGE_BASE_URL`
- `WHATSAPP_BRIDGE_TIMEOUT_SECONDS`
- `WHATSAPP_BRIDGE_API_KEY`
- `WHATSAPP_DEFAULT_SESSION_KEY`
- `BACKEND_CORS_ORIGINS`

### Contrato esperado da bridge

#### `POST /sessions/{session_key}/start`

```json
{
  "status": "awaiting_qr",
  "session_id": "provider-session-123",
  "phone": null,
  "qr_token": "2@ABCDEF",
  "qr_image_data_url": "data:image/png;base64,...",
  "metadata": {
    "provider": "whatsmeow"
  }
}
```

#### `GET /sessions/{session_key}`

```json
{
  "status": "connected",
  "session_id": "provider-session-123",
  "phone": "5511999990000",
  "qr_token": null,
  "qr_image_data_url": null,
  "metadata": {
    "provider": "whatsmeow"
  }
}
```

#### `POST /sessions/{session_key}/disconnect`

```json
{
  "status": "offline",
  "session_id": "provider-session-123",
  "phone": null,
  "qr_token": null,
  "qr_image_data_url": null,
  "metadata": {
    "provider": "whatsmeow"
  }
}
```

### Webhook opcional da bridge para esta API

Quando a bridge quiser empurrar mudancas de estado sem polling, ela pode chamar:

`POST /api/v1/whatsapp/webhooks/session-events`

Header opcional:

`X-API-Key: <WHATSAPP_BRIDGE_API_KEY>`

Payload:

```json
{
  "session_key": "principal",
  "status": "connected",
  "provider_session_id": "provider-session-123",
  "phone": "5511999990000",
  "qr_token": null,
  "qr_image_data_url": null,
  "last_error": null,
  "metadata": {
    "provider": "whatsmeow",
    "event": "connected"
  }
}
```

## Exemplo de criacao

```bash
curl -X POST http://localhost:8000/api/v1/whatsapp-sessions \
  -H "Content-Type: application/json" \
  -d '{
    "session_key": "principal",
    "status": "awaiting_qr",
    "phone": null,
    "metadata": {
      "source": "frontend"
    }
  }'
```
