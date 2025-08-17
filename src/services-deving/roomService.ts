export async function createRoom(): Promise<string> {
  const res = await fetch("http://localhost:3000/create-room", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const data = (await res.json()) as { roomId: string };
  return data.roomId;
}

export async function getRoomList(): Promise<string[]> {
  const res = await fetch("http://localhost:3000/rooms");
  const data = (await res.json()) as { rooms: string[] };
  return data.rooms;
}

export async function deleteRoom(roomId: string) {
  await fetch(`http://localhost:3000/rooms/${roomId}`, { method: "DELETE" });
}

export async function addRoom(roomId: string) {
  await fetch(`http://localhost:3000/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ roomId }),
  });
}

// WebSocket 订阅
export function subscribeRoomList(callback: (rooms: string[]) => void) {
  const ws = new WebSocket("ws://localhost:3001");
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "update") callback(msg.rooms);
  };
  return ws;
}
