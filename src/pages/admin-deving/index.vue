<template>
  <div>
    <h2>管理员房间管理</h2>
    <input v-model="newRoomId" placeholder="输入房间号" />
    <button @click="addNewRoom">新增房间</button>

    <ul>
      <li v-for="r in roomList" :key="r">
        {{ r }}
        <button @click="deleteExistingRoom(r)">删除</button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import {
  addRoom,
  deleteRoom,
  subscribeRoomList,
} from "@/services-deving/roomService";

export default defineComponent({
  setup() {
    const roomList = ref<string[]>([]);
    const newRoomId = ref("");

    const addNewRoom = async () => {
      if (!newRoomId.value) return;
      await addRoom(newRoomId.value);
      newRoomId.value = "";
    };

    const deleteExistingRoom = async (roomId: string) => {
      await deleteRoom(roomId);
    };

    onMounted(() => {
      subscribeRoomList((rooms) => (roomList.value = rooms));
    });

    return { roomList, newRoomId, addNewRoom, deleteExistingRoom };
  },
});
</script>
