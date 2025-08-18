// chatService.ts
import { ws } from "@/services/wsClient";
import { messages, currentRoom } from "@/services/state";

export function handleChatMessage(payload: any) {
  messages.value.push(payload);
}

export function sendMessage(playerName: string, message: string) {
  if (!currentRoom.value) return;
  if (!message.trim()) return;

  ws.value?.send(
    JSON.stringify({
      action: "sendMessage",
      payload: {
        roomId: currentRoom.value.id,
        playerName,
        message,
      },
    })
  );
}
