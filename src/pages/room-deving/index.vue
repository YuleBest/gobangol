<template>
  <div>
    <button @click="handleCreateRoom">创建房间</button>
    <p v-if="latestRoom">最新房间号：{{ latestRoom }}</p>
    <h3>房间列表</h3>
    <ul>
      <li v-for="r in roomList" :key="r">{{ r }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { createRoom, subscribeRoomList } from "@/services-deving/roomService";

export default defineComponent({
  setup() {
    const latestRoom = ref("");
    const roomList = ref<string[]>([]);

    const handleCreateRoom = async () => {
      latestRoom.value = await createRoom();
    };

    onMounted(() => {
      subscribeRoomList((rooms) => (roomList.value = rooms));
    });

    return { latestRoom, roomList, handleCreateRoom };
  },
});
</script>
