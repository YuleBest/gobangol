<template>
  <div
    style="
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 10px;
    "
  >
    <v-chip-group>
      <v-chip>轮到 {{ isBlackTurn ? "黑棋" : "白棋" }}</v-chip>
      <v-chip>{{ formatTime(timeElapsed) }}</v-chip>
    </v-chip-group>

    <div style="width: 100%; display: flex; justify-content: center">
      <canvas
        ref="board"
        style="
          width: 90%;
          max-width: 400px;
          height: auto;
          border: 1px solid #333;
        "
      ></canvas>
    </div>
    <div
      style="margin: 10px 0; display: flex; justify-content: center; gap: 10px"
    >
      <v-btn @click="undoMove" :disabled="moveHistory.length === 0 || gameOver">
        悔棋
      </v-btn>
      <v-btn @click="resetGame">重置棋盘</v-btn>
      <v-btn v-if="gameOver" @click="resetGame">再来一次</v-btn>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const board = ref(null);
const size = 15;
let ctx = null;
let cellSize = 0;
let chessData = [];
const isBlackTurn = ref(true);
const gameOver = ref(false);
const canMove = ref(true);
const moveHistory = ref([]);
const timeElapsed = ref(0);
const timer = ref(null);

onMounted(() => {
  initData();
  initBoard();
  window.addEventListener("resize", initBoard);
  // 暂时移除startTimer，等待第一次落子时启动
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", initBoard);
  clearInterval(timer.value);
});

function initData() {
  chessData = Array.from({ length: size }, () => Array(size).fill(0));
  isBlackTurn.value = true;
  gameOver.value = false;
  canMove.value = true;
  moveHistory.value = [];
  timeElapsed.value = 0;
}

function startTimer() {
  timer.value = setInterval(() => {
    if (!gameOver.value) timeElapsed.value++;
  }, 1000);
}

function formatTime(seconds) {
  const m = String(Math.floor(seconds / 60)).padStart(2, "0");
  const s = String(seconds % 60).padStart(2, "0");
  return `${m}:${s}`;
}

// --------- 初始化棋盘 ---------
function initBoard() {
  const canvas = board.value;
  ctx = canvas.getContext("2d");

  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;

  // 使用父容器宽度，但限制最大尺寸
  const canvasSize = Math.min(rect.width, 600);

  canvas.width = canvasSize * dpr;
  canvas.height = canvasSize * dpr;
  ctx.scale(dpr, dpr);

  cellSize = canvasSize / size;

  drawBoard();
  drawAllPieces();
  canvas.onclick = handleClick;
}

function drawBoard() {
  const canvasWidth = board.value.getBoundingClientRect().width;

  const gradient = ctx.createLinearGradient(0, 0, canvasWidth, canvasWidth);
  gradient.addColorStop(0, "#f9e4b7");
  gradient.addColorStop(1, "#e5c78a");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvasWidth, canvasWidth);

  ctx.strokeStyle = "#333";
  ctx.lineWidth = 1;
  for (let i = 0; i < size; i++) {
    ctx.beginPath();
    ctx.moveTo(cellSize / 2, cellSize / 2 + i * cellSize);
    ctx.lineTo(canvasWidth - cellSize / 2, cellSize / 2 + i * cellSize);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(cellSize / 2 + i * cellSize, cellSize / 2);
    ctx.lineTo(cellSize / 2 + i * cellSize, canvasWidth - cellSize / 2);
    ctx.stroke();
  }

  // 绘制星位
  const starPoints = [];
  if (size === 15) {
    starPoints.push(
      { x: 3, y: 3 },
      { x: 11, y: 3 },
      { x: 3, y: 11 },
      { x: 11, y: 11 },
      { x: 7, y: 7 }
    );
  } else if (size === 19) {
    starPoints.push(
      { x: 3, y: 3 },
      { x: 9, y: 3 },
      { x: 15, y: 3 },
      { x: 3, y: 9 },
      { x: 9, y: 9 },
      { x: 15, y: 9 },
      { x: 3, y: 15 },
      { x: 9, y: 15 },
      { x: 15, y: 15 }
    );
  }

  starPoints.forEach((point) => {
    const centerX = cellSize / 2 + point.x * cellSize;
    const centerY = cellSize / 2 + point.y * cellSize;
    const starRadius = cellSize * 0.1; // 星位圆点大小

    ctx.beginPath();
    ctx.arc(centerX, centerY, starRadius, 0, 2 * Math.PI);
    ctx.fillStyle = "#333"; // 星位颜色
    ctx.fill();
  });
}

// --------- 点击落子 ---------
function handleClick(e) {
  if (!canMove.value || gameOver.value) return;

  if (moveHistory.value.length === 0) {
    startTimer();
  }

  const rect = board.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  const i = Math.round((x - cellSize / 2) / cellSize);
  const j = Math.round((y - cellSize / 2) / cellSize);

  if (i < 0 || i >= size || j < 0 || j >= size) return;
  if (chessData[j][i] !== 0) return;

  canMove.value = false; // 冷却
  setTimeout(() => (canMove.value = true), 500);

  drawPieceAnimated(i, j, isBlackTurn.value);
}

function drawPieceAnimated(i, j, isBlack) {
  const x = cellSize / 2 + i * cellSize;
  const y = cellSize / 2 + j * cellSize;
  const maxRadius = (cellSize / 2) * 0.8;
  let startTime = null;
  const duration = 200;

  function animate(time) {
    if (!startTime) startTime = time;
    const elapsed = time - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const radius = maxRadius * progress;

    drawBoard();
    drawAllPiecesExcept(i, j);

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.closePath();

    const gradient = ctx.createRadialGradient(
      x - 2,
      y - 2,
      radius * 0.1,
      x,
      y,
      radius
    );
    if (isBlack) {
      gradient.addColorStop(0, "#555");
      gradient.addColorStop(1, "#000");
    } else {
      gradient.addColorStop(0, "#fff");
      gradient.addColorStop(1, "#ddd");
    }
    ctx.fillStyle = gradient;
    ctx.fill();

    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      chessData[j][i] = isBlack ? 1 : 2;
      moveHistory.value.push({ i, j, isBlack });
      const winLine = checkWin(i, j);
      if (winLine) {
        gameOver.value = true;
        clearInterval(timer.value); // 游戏结束时停止计时器
        drawWinLine(winLine);
        setTimeout(() => alert(`${isBlack ? "黑棋" : "白棋"}胜利！`), 10);
      }
      isBlackTurn.value = !isBlackTurn.value;
      drawPieceStatic(i, j, isBlack, true); // 绘制红色描边
    }
  }

  requestAnimationFrame(animate);
}

// --------- 绘制棋子 ---------
function drawAllPieces() {
  for (let j = 0; j < size; j++) {
    for (let i = 0; i < size; i++) {
      if (chessData[j][i] === 1) drawPieceStatic(i, j, true, false);
      if (chessData[j][i] === 2) drawPieceStatic(i, j, false, false);
    }
  }
}

function drawAllPiecesExcept(skipI, skipJ) {
  for (let j = 0; j < size; j++) {
    for (let i = 0; i < size; i++) {
      if (i === skipI && j === skipJ) continue;
      if (chessData[j][i] === 1) drawPieceStatic(i, j, true, false);
      if (chessData[j][i] === 2) drawPieceStatic(i, j, false, false);
    }
  }
}

function drawPieceStatic(i, j, isBlack, isLastMove = false) {
  const x = cellSize / 2 + i * cellSize;
  const y = cellSize / 2 + j * cellSize;
  const radius = (cellSize / 2) * 0.8;

  ctx.beginPath();
  ctx.arc(x, y, radius, 0, 2 * Math.PI);
  ctx.closePath();

  if (isLastMove) {
    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.stroke();
  }

  const gradient = ctx.createRadialGradient(
    x - 2,
    y - 2,
    radius * 0.1,
    x,
    y,
    radius
  );
  if (isBlack) {
    gradient.addColorStop(0, "#555");
    gradient.addColorStop(1, "#000");
  } else {
    gradient.addColorStop(0, "#fff");
    gradient.addColorStop(1, "#ddd");
  }
  ctx.fillStyle = gradient;
  ctx.fill();
}

// --------- 胜利检测 ---------
function checkWin(x, y) {
  const color = chessData[y][x];
  if (color === 0) return null;
  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];
  for (const dir of dirs) {
    let count = 1;
    const winLine = [{ x, y }];
    let i = 1;
    while (true) {
      const nx = x + dir.dx * i,
        ny = y + dir.dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        count++;
        winLine.push({ x: nx, y: ny });
      } else break;
      i++;
    }
    i = 1;
    while (true) {
      const nx = x - dir.dx * i,
        ny = y - dir.dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        count++;
        winLine.unshift({ x: nx, y: ny });
      } else break;
      i++;
    }
    if (count >= 5) return winLine;
  }
  return null;
}

// --------- 绘制胜利线 ---------
function drawWinLine(winLine) {
  ctx.strokeStyle = "green";
  ctx.lineWidth = 5;
  ctx.beginPath();
  const startX = cellSize / 2 + winLine[0].x * cellSize;
  const startY = cellSize / 2 + winLine[0].y * cellSize;
  ctx.moveTo(startX, startY);
  const endX = cellSize / 2 + winLine[winLine.length - 1].x * cellSize;
  const endY = cellSize / 2 + winLine[winLine.length - 1].y * cellSize;
  ctx.lineTo(endX, endY);
  ctx.stroke();
}

// --------- 悔棋 ---------
function undoMove() {
  if (moveHistory.value.length === 0 || gameOver.value) return;
  // 如果悔棋导致棋盘为空，则停止计时器并重置时间
  if (moveHistory.value.length === 1) {
    clearInterval(timer.value);
    timeElapsed.value = 0;
  }
  const last = moveHistory.value.pop();
  chessData[last.j][last.i] = 0;
  isBlackTurn.value = last.isBlack;
  drawBoard();
  drawAllPieces();
}

// --------- 重置棋盘 ---------
function resetGame() {
  clearInterval(timer.value);
  initData();
  drawBoard();
  drawAllPieces();
}
</script>
