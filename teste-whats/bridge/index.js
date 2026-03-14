require("dotenv").config();

const fs = require("fs");
const path = require("path");

const express = require("express");
const pino = require("pino");
const QRCode = require("qrcode");
const { Boom } = require("@hapi/boom");
const {
  default: makeWASocket,
  Browsers,
  DisconnectReason,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} = require("@whiskeysockets/baileys");

const PORT = Number(process.env.BRIDGE_PORT || 8081);
const AUTH_DIR = path.resolve(process.env.BRIDGE_AUTH_DIR || "./data/auth");
const START_TIMEOUT_MS = Number(process.env.BRIDGE_START_TIMEOUT_MS || 20000);
const LOG_LEVEL = process.env.BRIDGE_LOG_LEVEL || "info";

fs.mkdirSync(AUTH_DIR, { recursive: true });

const logger = pino({
  level: LOG_LEVEL,
});

const app = express();
app.use(express.json());

const sessions = new Map();

function nowIso() {
  return new Date().toISOString();
}

function authPathFor(sessionKey) {
  return path.join(AUTH_DIR, sessionKey);
}

function normalizePhone(rawValue) {
  if (!rawValue) return null;
  const candidate = String(rawValue).split(":")[0];
  const digits = candidate.replace(/\D/g, "");
  return digits || null;
}

function createEmptySession(sessionKey) {
  return {
    sessionKey,
    sessionId: `baileys-${sessionKey}`,
    status: "offline",
    phone: null,
    qrToken: null,
    qrImageDataUrl: null,
    lastError: null,
    metadata: {
      provider: "baileys",
      bridge: "self-hosted-local",
    },
    updatedAt: nowIso(),
    socket: null,
    saveCreds: null,
    authDir: authPathFor(sessionKey),
    waiters: new Set(),
    isStarting: false,
    intentionalDisconnect: false,
  };
}

function getSession(sessionKey) {
  const normalizedKey = String(sessionKey).trim().toLowerCase();
  if (!sessions.has(normalizedKey)) {
    sessions.set(normalizedKey, createEmptySession(normalizedKey));
  }
  return sessions.get(normalizedKey);
}

function serializeSession(session) {
  return {
    status: session.status,
    session_id: session.sessionId,
    phone: session.phone,
    qr_token: session.qrToken,
    qr_image_data_url: session.qrImageDataUrl,
    last_error: session.lastError,
    metadata: session.metadata,
    updated_at: session.updatedAt,
  };
}

function normalizeRecipient(rawValue) {
  const digits = String(rawValue || "").replace(/\D/g, "");
  if (!digits) {
    return null;
  }
  return `${digits}@s.whatsapp.net`;
}

function resolveWaiters(session) {
  for (const waiter of session.waiters) {
    clearTimeout(waiter.timeoutId);
    waiter.resolve();
  }
  session.waiters.clear();
}

function updateSession(session, partial) {
  const nextMetadata = partial.metadata
    ? { ...session.metadata, ...partial.metadata }
    : session.metadata;

  Object.assign(session, partial, {
    metadata: nextMetadata,
    updatedAt: nowIso(),
  });

  resolveWaiters(session);
}

function waitForState(session, matcher, timeoutMs) {
  if (matcher(session)) {
    return Promise.resolve();
  }

  return new Promise((resolve) => {
    const timeoutId = setTimeout(() => {
      session.waiters.delete(waiter);
      resolve();
    }, timeoutMs);

    const waiter = {
      timeoutId,
      resolve,
    };

    session.waiters.add(waiter);
  });
}

function clearAuthState(session) {
  fs.rmSync(session.authDir, { recursive: true, force: true });
}

async function teardownSocket(session, shouldClearAuth = false) {
  if (session.saveCreds && session.socket) {
    session.socket.ev.off("creds.update", session.saveCreds);
  }

  if (session.socket) {
    session.socket.ev.removeAllListeners("connection.update");
    session.socket.ev.removeAllListeners("creds.update");
    session.socket.end(new Error("Session closed"));
  }

  session.socket = null;
  session.saveCreds = null;
  session.isStarting = false;

  if (shouldClearAuth) {
    clearAuthState(session);
  }
}

async function bootstrapSession(session) {
  if (session.isStarting || session.socket) {
    return;
  }

  session.isStarting = true;
  session.intentionalDisconnect = false;
  fs.mkdirSync(session.authDir, { recursive: true });

  try {
    const { state, saveCreds } = await useMultiFileAuthState(session.authDir);
    const { version } = await fetchLatestBaileysVersion();

    const socket = makeWASocket({
      version,
      auth: state,
      browser: Browsers.macOS("Teste Whats"),
      printQRInTerminal: false,
      logger: logger.child({ component: "baileys", sessionKey: session.sessionKey }),
    });

    session.socket = socket;
    session.saveCreds = saveCreds;

    socket.ev.on("creds.update", saveCreds);

    socket.ev.on("connection.update", async (update) => {
      const { connection, lastDisconnect, qr } = update;

      if (qr) {
        const qrImageDataUrl = await QRCode.toDataURL(qr, {
          errorCorrectionLevel: "M",
          margin: 2,
          width: 360,
        });

        updateSession(session, {
          status: "awaiting_qr",
          qrToken: qr,
          qrImageDataUrl,
          phone: null,
          lastError: null,
          metadata: {
            event: "qr",
          },
        });
      }

      if (connection === "open") {
        updateSession(session, {
          status: "connected",
          sessionId: socket.user?.id || session.sessionId,
          phone: normalizePhone(socket.user?.id),
          qrToken: null,
          qrImageDataUrl: null,
          lastError: null,
          metadata: {
            event: "open",
            user_id: socket.user?.id || null,
            user_name: socket.user?.name || null,
          },
        });
        session.isStarting = false;
        return;
      }

      if (connection === "close") {
        const statusCode = new Boom(lastDisconnect?.error)?.output?.statusCode;
        const loggedOut = statusCode === DisconnectReason.loggedOut;
        const shouldReconnect = !session.intentionalDisconnect && !loggedOut;

        await teardownSocket(session, loggedOut || session.intentionalDisconnect);

        if (shouldReconnect) {
          updateSession(session, {
            status: "error",
            lastError: "connection_closed_reconnecting",
            metadata: {
              event: "close",
              reconnecting: true,
            },
          });

          setTimeout(() => {
            bootstrapSession(session).catch((error) => {
              logger.error({ error, sessionKey: session.sessionKey }, "Failed to reconnect session");
            });
          }, 1500);
          return;
        }

        updateSession(session, {
          status: "offline",
          phone: null,
          qrToken: null,
          qrImageDataUrl: null,
          lastError: loggedOut ? "logged_out" : null,
          metadata: {
            event: "close",
            logged_out: loggedOut,
          },
        });
      }
    });
  } catch (error) {
    await teardownSocket(session);
    updateSession(session, {
      status: "error",
      lastError: error instanceof Error ? error.message : "bridge_start_failed",
      metadata: {
        event: "startup_error",
      },
    });
  } finally {
    session.isStarting = false;
  }
}

app.get("/health", (_request, response) => {
  response.json({
    status: "ok",
    service: "teste-whats-bridge",
    sessions: sessions.size,
  });
});

app.post("/sessions/:sessionKey/start", async (request, response) => {
  const session = getSession(request.params.sessionKey);

  if (session.status === "connected" || session.status === "awaiting_qr") {
    response.json(serializeSession(session));
    return;
  }

  await bootstrapSession(session);
  await waitForState(
    session,
    (current) => ["awaiting_qr", "connected", "error"].includes(current.status),
    START_TIMEOUT_MS,
  );

  response.json(serializeSession(session));
});

app.get("/sessions/:sessionKey", (request, response) => {
  const session = getSession(request.params.sessionKey);
  response.json(serializeSession(session));
});

app.post("/sessions/:sessionKey/disconnect", async (request, response) => {
  const session = getSession(request.params.sessionKey);
  session.intentionalDisconnect = true;

  if (session.socket) {
    try {
      await session.socket.logout();
    } catch (error) {
      logger.warn({ error, sessionKey: session.sessionKey }, "Socket logout returned an error");
    }
  }

  await teardownSocket(session, true);
  updateSession(session, {
    status: "offline",
    phone: null,
    qrToken: null,
    qrImageDataUrl: null,
    lastError: null,
    metadata: {
      event: "manual_disconnect",
    },
  });

  response.json(serializeSession(session));
});

app.post("/sessions/:sessionKey/messages", async (request, response) => {
  const session = getSession(request.params.sessionKey);
  const recipientJid = normalizeRecipient(request.body?.phone);
  const text = String(request.body?.text || "").trim();

  if (!recipientJid) {
    response.status(400).json({
      detail: "A valid phone number is required.",
    });
    return;
  }

  if (!text) {
    response.status(400).json({
      detail: "Message text is required.",
    });
    return;
  }

  if (!session.socket || session.status !== "connected") {
    response.status(409).json({
      detail: "Session is not connected.",
    });
    return;
  }

  try {
    const sendResult = await session.socket.sendMessage(recipientJid, { text });

    response.json({
      status: "sent",
      to: recipientJid.replace("@s.whatsapp.net", ""),
      text,
      provider_message_id: sendResult?.key?.id || null,
      metadata: {
        provider: "baileys",
        remote_jid: sendResult?.key?.remoteJid || recipientJid,
        from_me: Boolean(sendResult?.key?.fromMe),
      },
    });
  } catch (error) {
    logger.error({ error, sessionKey: session.sessionKey }, "Failed to send WhatsApp message");
    response.status(500).json({
      detail: error instanceof Error ? error.message : "Failed to send WhatsApp message.",
    });
  }
});

app.listen(PORT, () => {
  logger.info({ port: PORT, authDir: AUTH_DIR }, "Teste Whats bridge is running");
});
