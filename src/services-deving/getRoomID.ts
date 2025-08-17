// 封装后端请求
export async function getRoomID(): Promise<string> {
  try {
    const res = await fetch("http://localhost:3000/create-room", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const data = (await res.json()) as { roomId: string };
    return data.roomId;
  } catch (err) {
    console.error(err);
    throw new Error("获取房间号失败");
  }
}
