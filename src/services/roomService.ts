// roomService.ts
import { ws } from "@/services/wsClient";
import type { Room } from "@/services/types";
import { rooms, currentRoom } from "@/services/state";

export function handleRoomMessage(action: string, payload: any) {
  switch (action) {
    case "roomList":
      if (!currentRoom.value) rooms.value = payload;
      else
        rooms.value = payload.filter(
          (r: Room) => r.id !== currentRoom.value?.id
        );
      break;
    case "roomCreated":
      currentRoom.value = payload;
      rooms.value.push(payload);
      break;
    case "joinedRoom":
      currentRoom.value = payload;
      break;
    case "roomUpdate":
      if (!currentRoom.value) return;
      currentRoom.value.players = payload.players;
      currentRoom.value.spectators = payload.spectators;
      currentRoom.value.roomStatus = payload.roomStatus;
      break;
    case "roomClosed":
      if (currentRoom.value && currentRoom.value.id === payload.id) {
        currentRoom.value = null;
      }
      rooms.value = rooms.value.filter((r) => r.id !== payload.id);
      break;
  }
}

export function createRoom(creator: string, password?: string) {
  ws.value?.send(
    JSON.stringify({
      action: "createRoom",
      payload: { creator, password: password || "" },
    })
  );
}

export function joinRoom(roomId: string, user: string, password?: string) {
  ws.value?.send(
    JSON.stringify({
      action: "joinRoom",
      payload: { roomId, user, password: password || "" },
    })
  );
}

export function leaveRoom(user: string) {
  if (!currentRoom.value) return;
  ws.value?.send(
    JSON.stringify({
      action: "leaveRoom",
      payload: { roomId: currentRoom.value.id, user },
    })
  );
  currentRoom.value = null;
}

export function destroyRoom(roomId: string) {
  ws.value?.send(
    JSON.stringify({ action: "destroyRoom", payload: { roomId } })
  );
  if (currentRoom.value && currentRoom.value.id === roomId) {
    currentRoom.value = null;
  }
}
