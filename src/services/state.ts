// state.ts
import { ref } from "vue";
import type { Room, ChatMessage } from "@/services/types";

export const rooms = ref<Room[]>([]);
export const currentRoom = ref<Room | null>(null);

export const messages = ref<ChatMessage[]>([]);
