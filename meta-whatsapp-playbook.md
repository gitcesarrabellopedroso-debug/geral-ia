# Playbook Meta / WhatsApp

## Estrutura atual validada

- Portfolio principal: `BWS`
- Conta do WhatsApp principal: `UZA Multinivel`
- Numero real atual: `+55 19 99727-5276`
- App principal: `Scalle_wpp`
- System user tecnico atual: `scalee_api_2`
- Conta de teste: `Test WhatsApp Business Account`

## Dados tecnicos ja levantados

- `Phone Number ID`: `926220003913113`
- `WABA ID`: `1241971824445557`
- `App ID`: `1536921637532151`
- `Verify Token` definido para a futura aplicacao: `scalee_whatsapp_20260314`
- `Access Token`: nao registrar em documento publico; usar o token atual do `scalee_api_2`

## Regras operacionais

- Operar no portfolio `BWS`
- Usar `UZA Multinivel` para numeros reais
- Manter `Test WhatsApp Business Account` apenas como teste
- Nao usar `BWS UZA multinivel` para operacao nova
- Tratar `UZA Multinivel` como legado/congelado ate revisao futura
- Nao apagar ativos da Meta no impulso; validar primeiro se o item e real, teste ou legado

## O que repetir para cada numero novo

1. Entrar no portfolio `BWS`
2. Abrir `Contas do WhatsApp`
3. Adicionar o novo numero ou nova conta
4. Verificar por SMS ou ligacao
5. Revisar o nome de exibicao
6. Pegar o `Phone Number ID`
7. Confirmar se o webhook atual pode ser reutilizado
8. Testar envio de mensagem

## O que normalmente nao precisa repetir

- Criar novo app
- Criar novo portfolio
- Criar novo system user
- Refazer webhook do zero
- Rotacionar token sem necessidade

## Prompt pronto: novo numero

```text
Vamos cadastrar um novo numero na Meta.

Estrutura atual:
- Portfolio principal: BWS
- Conta do WhatsApp principal: UZA Multinivel
- App principal: Scalle_wpp
- System user atual: scalee_api_2

Quero que voce me conduza, um passo por vez, para:
1. validar se o numero entra no BWS
2. adicionar o numero
3. verificar por SMS ou ligacao
4. revisar o nome de exibicao
5. pegar o Phone Number ID
6. confirmar se o webhook atual pode ser reutilizado
7. testar envio de mensagem
```

## Prompt pronto: novo cliente

```text
Vamos configurar um novo cliente na Meta.

Quero que voce me conduza, um passo por vez, para decidir:
1. se esse cliente entra no meu portfolio atual ou em estrutura separada
2. qual conta do WhatsApp criar
3. qual numero usar
4. como organizar sem misturar com os ativos atuais
5. como preparar a integracao com a aplicacao
```

## Prompt pronto: novo portfolio

```text
Vamos criar um novo portfolio empresarial na Meta.

Quero que voce me conduza, um passo por vez, para:
1. criar o novo portfolio
2. nomear corretamente
3. deixar separado do BWS
4. decidir quais pessoas e apps entram nele
5. preparar esse portfolio para receber numeros de WhatsApp sem misturar com os atuais
```

## Checklist curto

```text
Checklist Meta
- Numero novo: BWS > Contas do WhatsApp > adicionar > verificar > display name > Phone Number ID > teste
- Cliente novo: decidir se entra no BWS ou em ambiente separado
- Portfolio novo: criar, nomear, separar acessos, depois configurar WhatsApp
```

## Integracao com a aplicacao

Hoje ja estao definidos:

- `Phone Number ID`: `926220003913113`
- `WABA ID`: `1241971824445557`
- `App ID`: `1536921637532151`
- `Verify Token`: `scalee_whatsapp_20260314`

A aplicacao ainda precisa prover:

- `Webhook URL` proprio
- endpoint que responda a verificacao da Meta
- recebimento de eventos `messages`
- logica para chamar a IA
- envio de resposta via Graph API usando `Phone Number ID` + `Access Token`

## Observacoes importantes

- O `Webhook URL` final deve ser da propria aplicacao
- O webhook antigo em `webhook.scalee.com.br` nao deve ser tratado como base definitiva se nao houver controle do backend
- O token antigo do `uza_app` foi revogado
- O token atual em uso deve ser o gerado no `scalee_api_2`
