const STORAGE_KEY = "teste-whats-state-v1";
const CONFIG_KEY = "teste-whats-config-v1";

const initialState = {
  status: "offline",
  sessionId: null,
  phone: null,
  qrToken: null,
  qrImageDataUrl: null,
  lastUpdate: null,
  logs: [],
};

const initialConfig = {
  mode: "mock",
  apiBase: "http://localhost:8000",
};

const elements = {
  connectionBadge: document.querySelector("#connectionBadge"),
  statusCaption: document.querySelector("#statusCaption"),
  qrStage: document.querySelector("#qrStage"),
  sessionStatus: document.querySelector("#sessionStatus"),
  sessionId: document.querySelector("#sessionId"),
  lastUpdate: document.querySelector("#lastUpdate"),
  phoneValue: document.querySelector("#phoneValue"),
  eventLog: document.querySelector("#eventLog"),
  modeSelect: document.querySelector("#modeSelect"),
  apiBaseInput: document.querySelector("#apiBaseInput"),
  configFeedback: document.querySelector("#configFeedback"),
  messagePhoneInput: document.querySelector("#messagePhoneInput"),
  messageTextInput: document.querySelector("#messageTextInput"),
  sendMessageButton: document.querySelector("#sendMessageButton"),
  sendMessageFeedback: document.querySelector("#sendMessageFeedback"),
  startButton: document.querySelector("#startButton"),
  simulateConnectButton: document.querySelector("#simulateConnectButton"),
  disconnectButton: document.querySelector("#disconnectButton"),
  refreshButton: document.querySelector("#refreshButton"),
  saveConfigButton: document.querySelector("#saveConfigButton"),
  clearLogButton: document.querySelector("#clearLogButton"),
  logItemTemplate: document.querySelector("#logItemTemplate"),
};

let state = loadJson(STORAGE_KEY, initialState);
let config = loadJson(CONFIG_KEY, initialConfig);
let configFeedbackTimer = null;
let sendMessageFeedbackTimer = null;

function loadJson(key, fallback) {
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return structuredClone(fallback);
    return { ...fallback, ...JSON.parse(raw) };
  } catch (error) {
    return structuredClone(fallback);
  }
}

function saveState() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function saveConfig() {
  window.localStorage.setItem(CONFIG_KEY, JSON.stringify(config));
}

function showConfigFeedback(message) {
  elements.configFeedback.textContent = message;

  if (configFeedbackTimer) {
    window.clearTimeout(configFeedbackTimer);
  }

  configFeedbackTimer = window.setTimeout(() => {
    elements.configFeedback.textContent = "";
  }, 2500);
}

function showSendMessageFeedback(message, isError = false) {
  elements.sendMessageFeedback.textContent = message;
  elements.sendMessageFeedback.style.color = isError ? "var(--danger)" : "var(--accent)";

  if (sendMessageFeedbackTimer) {
    window.clearTimeout(sendMessageFeedbackTimer);
  }

  sendMessageFeedbackTimer = window.setTimeout(() => {
    elements.sendMessageFeedback.textContent = "";
  }, 3500);
}

function addLog(title, message) {
  state.logs = [
    {
      id: crypto.randomUUID(),
      time: new Date().toISOString(),
      title,
      message,
    },
    ...state.logs,
  ].slice(0, 20);

  saveState();
  renderLogs();
}

function formatDate(value) {
  if (!value) return "-";
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "medium",
  }).format(new Date(value));
}

function setStatusVisual(status) {
  elements.connectionBadge.classList.remove("is-waiting", "is-connected");

  if (status === "awaiting_qr") {
    elements.connectionBadge.textContent = "Aguardando leitura";
    elements.connectionBadge.classList.add("is-waiting");
    elements.statusCaption.textContent = "QR gerado. Leia com o WhatsApp para concluir o pareamento.";
    return;
  }

  if (status === "connected") {
    elements.connectionBadge.textContent = "Conectado";
    elements.connectionBadge.classList.add("is-connected");
    elements.statusCaption.textContent = "Sessao ativa e pronta para integracao com a bridge real.";
    return;
  }

  elements.connectionBadge.textContent = "Desconectado";
  elements.statusCaption.textContent = "Aguardando inicio de sessao local.";
}

function renderQr() {
  if (state.status !== "awaiting_qr") {
    elements.qrStage.innerHTML = `
      <div class="qr-placeholder">
        <span>QR indisponivel</span>
        <small>Inicie a sessao para gerar um QR de teste.</small>
      </div>
    `;
    return;
  }

  if (state.qrImageDataUrl) {
    elements.qrStage.innerHTML = `
      <div class="qr-box qr-box-image">
        <img class="qr-image" src="${state.qrImageDataUrl}" alt="QR Code do WhatsApp para pareamento">
      </div>
    `;
    return;
  }

  if (!state.qrToken) {
    elements.qrStage.innerHTML = `
      <div class="qr-placeholder">
        <span>Gerando QR</span>
        <small>Aguardando a bridge devolver a imagem do QR real.</small>
      </div>
    `;
    return;
  }

  elements.qrStage.innerHTML = `
    <div class="qr-box">
      <div class="qr-pattern" aria-hidden="true"></div>
      <span class="qr-label">${state.qrToken}</span>
    </div>
  `;
}

function renderSummary() {
  setStatusVisual(state.status);
  renderQr();

  elements.sessionStatus.textContent = state.status;
  elements.sessionId.textContent = state.sessionId || "-";
  elements.lastUpdate.textContent = formatDate(state.lastUpdate);
  elements.phoneValue.textContent = state.phone || "-";
}

function renderLogs() {
  elements.eventLog.innerHTML = "";

  if (!state.logs.length) {
    elements.eventLog.innerHTML = `
      <li class="event-item">
        <span class="event-time">-</span>
        <div class="event-body">
          <strong class="event-title">Sem eventos</strong>
          <p class="event-message">Os eventos de conexao e sessao vao aparecer aqui.</p>
        </div>
      </li>
    `;
    return;
  }

  for (const item of state.logs) {
    const node = elements.logItemTemplate.content.cloneNode(true);
    node.querySelector(".event-time").textContent = formatDate(item.time);
    node.querySelector(".event-title").textContent = item.title;
    node.querySelector(".event-message").textContent = item.message;
    elements.eventLog.appendChild(node);
  }
}

function renderConfig() {
  elements.modeSelect.value = config.mode;
  elements.apiBaseInput.value = config.apiBase;
}

function render() {
  renderSummary();
  renderLogs();
  renderConfig();
}

function syncConfigFromInputs() {
  config = {
    mode: elements.modeSelect.value,
    apiBase: elements.apiBaseInput.value.trim() || initialConfig.apiBase,
  };
}

function touchState(partial) {
  state = {
    ...state,
    ...partial,
    lastUpdate: new Date().toISOString(),
  };
  saveState();
  renderSummary();
}

function randomToken(size = 8) {
  return Array.from(crypto.getRandomValues(new Uint8Array(size)))
    .map((value) => value.toString(16).padStart(2, "0"))
    .join("")
    .slice(0, size)
    .toUpperCase();
}

async function startSession() {
  syncConfigFromInputs();
  saveConfig();

  if (config.mode === "api") {
    return startSessionFromApi();
  }

  touchState({
    status: "awaiting_qr",
    sessionId: `session-${randomToken(10)}`,
    qrToken: `QR-${randomToken(6)}`,
    qrImageDataUrl: null,
    phone: null,
  });

  addLog("Sessao iniciada", "QR local gerado para validar a interface de pareamento.");
}

async function simulateConnect() {
  syncConfigFromInputs();
  saveConfig();

  if (config.mode === "api") {
    return refreshStatusFromApi();
  }

  if (state.status !== "awaiting_qr") {
    addLog("Acao ignorada", "Nao ha QR pendente para leitura no modo local.");
    return;
  }

  touchState({
    status: "connected",
    phone: "+55 11 99999-0000",
    qrToken: null,
    qrImageDataUrl: null,
  });

  addLog("Pareamento concluido", "Leitura do QR simulada com sucesso.");
}

async function disconnectSession() {
  syncConfigFromInputs();
  saveConfig();

  if (config.mode === "api") {
    return disconnectFromApi();
  }

  touchState({
    status: "offline",
    sessionId: null,
    phone: null,
    qrToken: null,
    qrImageDataUrl: null,
  });

  addLog("Sessao encerrada", "A conexao local foi limpa.");
}

async function refreshStatus() {
  syncConfigFromInputs();
  saveConfig();

  if (config.mode === "api") {
    return refreshStatusFromApi();
  }

  state.lastUpdate = new Date().toISOString();
  saveState();
  renderSummary();
  addLog("Status atualizado", "Leitura local concluida.");
}

function saveConfiguration() {
  syncConfigFromInputs();
  saveConfig();
  addLog("Configuracao salva", `Modo atual: ${config.mode}.`);
  showConfigFeedback("Configuracao salva.");
}

async function startSessionFromApi() {
  try {
    const response = await fetch(`${config.apiBase}/api/whatsapp/session/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const payload = await response.json();
    syncStateFromApi(payload, "Sessao iniciada via API.");
  } catch (error) {
    addLog("Erro na API", "Falha ao iniciar sessao no endpoint remoto.");
  }
}

async function refreshStatusFromApi() {
  try {
    const response = await fetch(`${config.apiBase}/api/whatsapp/status`);
    const payload = await response.json();
    syncStateFromApi(payload, "Status sincronizado via API.");
  } catch (error) {
    addLog("Erro na API", "Falha ao consultar status no endpoint remoto.");
  }
}

async function disconnectFromApi() {
  try {
    const response = await fetch(`${config.apiBase}/api/whatsapp/session/disconnect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const payload = await response.json();
    syncStateFromApi(payload, "Sessao desconectada via API.");
  } catch (error) {
    addLog("Erro na API", "Falha ao desconectar a sessao remota.");
  }
}

async function sendMessageFromApi() {
  syncConfigFromInputs();
  saveConfig();

  if (config.mode !== "api") {
    showSendMessageFeedback("Troque para API externa antes de enviar.", true);
    return;
  }

  const phone = elements.messagePhoneInput.value.trim();
  const text = elements.messageTextInput.value.trim();

  if (!phone || !text) {
    showSendMessageFeedback("Preencha numero e mensagem.", true);
    return;
  }

  try {
    const response = await fetch(`${config.apiBase}/api/whatsapp/messages/send`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        phone,
        text,
      }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Falha ao enviar mensagem.");
    }

    addLog("Mensagem enviada", `Envio confirmado para ${payload.to}.`);
    showSendMessageFeedback("Mensagem enviada.");
    elements.messageTextInput.value = "";
  } catch (error) {
    const message = error instanceof Error ? error.message : "Falha ao enviar mensagem.";
    addLog("Erro no envio", message);
    showSendMessageFeedback(message, true);
  }
}

function syncStateFromApi(payload, message) {
  touchState({
    status: payload.status || "offline",
    sessionId: payload.session_id || payload.sessionId || null,
    phone: payload.phone || null,
    qrToken: payload.qr_token || payload.qrToken || null,
    qrImageDataUrl: payload.qr_image_data_url || payload.qrImageDataUrl || null,
  });

  addLog("API sincronizada", message);
}

elements.startButton.addEventListener("click", startSession);
elements.simulateConnectButton.addEventListener("click", simulateConnect);
elements.disconnectButton.addEventListener("click", disconnectSession);
elements.refreshButton.addEventListener("click", refreshStatus);
elements.saveConfigButton.addEventListener("click", saveConfiguration);
elements.sendMessageButton.addEventListener("click", sendMessageFromApi);
elements.clearLogButton.addEventListener("click", () => {
  state.logs = [];
  saveState();
  renderLogs();
});

render();
