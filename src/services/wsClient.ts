// src/services/wsClient.ts
import { ref } from "vue";

export const ws = ref<WebSocket | null>(null);

export function connectWS(
  url: string,
  onOpen?: () => void,
  onError?: () => void
) {
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    console.log("[WS] 已存在连接，复用中");
    onOpen?.();
    return;
  }

  ws.value = new WebSocket(url);

  ws.value.onopen = () => {
    console.log("[WS] 已连接");
    onOpen?.();
  };

  ws.value.onclose = () => {
    console.log("[WS] 已断开");
    ws.value = null;
  };

  ws.value.onerror = (err) => {
    console.error("[WS] 错误", err);
    onError?.();
  };
}

export function closeWS() {
  if (ws.value) {
    ws.value.close();
    ws.value = null;
  }
}

export function fetchRoomList() {
  if (ws.value?.readyState === WebSocket.OPEN) {
    ws.value.send(JSON.stringify({ action: "getRoomList" }));
  }
}
