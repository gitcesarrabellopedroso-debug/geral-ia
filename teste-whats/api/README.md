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

## Endpoints iniciais

- `GET /api/v1/health`
- `POST /api/v1/whatsapp-sessions`
- `GET /api/v1/whatsapp-sessions`
- `GET /api/v1/whatsapp-sessions/{session_id}`
- `PATCH /api/v1/whatsapp-sessions/{session_id}`
- `DELETE /api/v1/whatsapp-sessions/{session_id}`

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
