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

## Como testar agora

Abra `index.html` no navegador.

Fluxo local:

1. Clique em `Iniciar sessao`
2. O sistema gera um QR local de teste
3. Clique em `Simular leitura`
4. O status muda para `Conectado`
5. Clique em `Desconectar` para limpar a sessao

Os dados ficam no `localStorage` do navegador para simular persistencia.

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

1. criar uma bridge backend para WhatsApp
2. substituir `qrToken` por QR real
3. persistir sessao fora do navegador
4. integrar envio e recebimento de mensagens
