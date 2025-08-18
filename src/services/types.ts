// types.ts
export interface Room {
  id: string;
  creator: string;
  players: string[];
  spectators: string[];
  roomStatus: string;
  password?: string;
}

export interface ChatMessage {
  playerName: string;
  message: string;
}
