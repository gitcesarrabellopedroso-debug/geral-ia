# Teste Whats

Projeto inicial de interface para validar o fluxo de conexao do WhatsApp antes da fase de infraestrutura.

## Objetivo desta fase

- validar a tela de pareamento por QR code
- validar estados de conexao
- validar UX de sessao persistente
- deixar o frontend pronto para plugar na bridge real depois

## Estrutura

- `index.html`: interface principal
- `styles.css`: visual
- `app.js`: logica local e integracao futura com API
- `bridge/`: bridge local self-hosted para WhatsApp Web via Baileys
- `api/`: API Python que consulta a bridge e persiste o estado

## Como testar agora

Abra `index.html` no navegador.

Fluxo local:

1. Clique em `Iniciar sessao`
2. O sistema gera um QR local de teste
3. Clique em `Simular leitura`
4. O status muda para `Conectado`
5. Clique em `Desconectar` para limpar a sessao

Os dados ficam no `localStorage` do navegador para simular persistencia.

## Como testar com WhatsApp real local

### Opcao recomendada com Docker

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats
docker compose up --build
```

Servicos:

- frontend estatico: abrir `index.html` no navegador
- API local: `http://localhost:8000`
- docs da API: `http://localhost:8000/docs`
- bridge local do WhatsApp: `http://localhost:8081/health`

Depois:

1. abrir `index.html`
2. mudar `Modo` para `API externa`
3. manter `Base URL da API` como `http://localhost:8000`
4. clicar em `Salvar configuracao`
5. clicar em `Iniciar sessao`
6. ler o QR real com o WhatsApp
7. apos conectar, preencher numero e mensagem no card `Envio real`
8. clicar em `Enviar mensagem`

### Opcao sem Docker para a bridge

```bash
cd /Users/cesarrabello/Documents/1_projetos_python/sistemas/ozonotech/geral-ia/teste-whats/bridge
cp .env.example .env
npm install
npm start
```

Nesse caso, a bridge sobe em `http://localhost:8081`.

## Contrato previsto para a API real

Quando a bridge do WhatsApp entrar, o frontend ja espera estes endpoints:

### `GET /api/whatsapp/status`

Resposta esperada:

```json
{
  "status": "offline",
  "sessionId": null,
  "phone": null,
  "qrToken": null
}
```

Status validos:

- `offline`
- `awaiting_qr`
- `connected`

### `POST /api/whatsapp/session/start`

Inicia ou reabre uma sessao de pareamento.

Resposta esperada:

```json
{
  "status": "awaiting_qr",
  "sessionId": "session-abc123",
  "phone": null,
  "qrToken": "QR-123456"
}
```

### `POST /api/whatsapp/session/disconnect`

Encerra a sessao atual.

Resposta esperada:

```json
{
  "status": "offline",
  "sessionId": null,
  "phone": null,
  "qrToken": null
}
```

## Proximo passo recomendado

Depois desta fase de projeto:

1. validar o pareamento real com a bridge local
2. validar envio real de mensagens
3. persistir sessao operacional no ambiente definitivo
4. integrar recebimento de mensagens e webhooks
