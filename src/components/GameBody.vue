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
      <v-chip>步数: {{ movesCount }}</v-chip>
    </v-chip-group>

    <div style="width: 100%; display: flex; justify-content: center">
      <canvas
        ref="board"
        style="
          width: 90%;
          max-width: 400px;
          height: auto;
          border: 1px solid #333;
          box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
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

    <v-dialog v-model="dialogVisible" max-width="300">
      <v-card>
        <v-card-title class="headline">游戏结束</v-card-title>
        <v-card-text>{{ winnerText }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="resetGame">再来一局</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
const dialogVisible = ref(false);
const winnerText = ref("");
const movesCount = ref(0);
const confirmMode = ref(false);
const previewX = ref(-1);
const previewY = ref(-1);

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
  movesCount.value = 0;
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

  const rect = board.value.getBoundingClientRect();
  const x = Math.round((e.clientX - rect.left - cellSize / 2) / cellSize);
  const y = Math.round((e.clientY - rect.top - cellSize / 2) / cellSize);

  if (x < 0 || x >= size || y < 0 || y >= size) return;

  if (confirmMode.value) {
    // 确认落子
    if (x === previewX.value && y === previewY.value) {
      if (chessData[y][x] !== 0) {
        // 如果点击了已经有棋子的位置，取消预览
        confirmMode.value = false;
        previewX.value = -1;
        previewY.value = -1;
        drawAllPieces();
        return;
      }

      if (moveHistory.value.length === 0) {
        startTimer();
      }
      movesCount.value++;

      const piece = isBlackTurn.value ? 1 : 2;
      chessData[y][x] = piece;
      moveHistory.value.push({ x, y, piece });
      drawPieceAnimated(x, y, piece);

      confirmMode.value = false;
      previewX.value = -1;
      previewY.value = -1;
      isBlackTurn.value = !isBlackTurn.value;
    } else {
      // 点击了其他位置，取消预览
      confirmMode.value = false;
      previewX.value = -1;
      previewY.value = -1;
      drawAllPieces();
    }
  } else {
    // 第一次点击，显示半透明预览
    if (chessData[y][x] === 0) {
      confirmMode.value = true;
      previewX.value = x;
      previewY.value = y;
      drawAllPieces();
      drawPiecePreview(x, y, isBlackTurn.value ? 1 : 2);
    }
  }
}

function drawPieceAnimated(x, y, piece) {
  const duration = 100; // 动画持续时间，毫秒
  const startTime = performance.now();
  const startRadius = 0;
  const endRadius = cellSize * 0.4;

  function animate(currentTime) {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);
    const currentRadius = startRadius + (endRadius - startRadius) * progress;

    drawBoard();
    drawAllPieces(); // 清除所有棋子，包括预览棋子

    const centerX = cellSize / 2 + x * cellSize;
    const centerY = cellSize / 2 + y * cellSize;

    ctx.beginPath();
    ctx.arc(centerX, centerY, currentRadius, 0, 2 * Math.PI);
    ctx.closePath();

    const gradient = ctx.createRadialGradient(
      centerX - 2,
      centerY - 2,
      currentRadius * 0.1,
      centerX,
      centerY,
      currentRadius
    );
    if (piece === 1) {
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
      // 动画结束后，检查胜利
      const winLine = checkWin(x, y);
      if (winLine) {
        gameOver.value = true;
        clearInterval(timer.value);
        drawWinLine(winLine);
        winnerText.value = `${piece === 1 ? '黑棋' : '白棋'}胜利！`;
        dialogVisible.value = true;
      }
      if (gameOver.value) {
        movesCount.value = 0;
      }
    }
  }
  requestAnimationFrame(animate);
}

// --------- 绘制棋子 ---------
function drawAllPieces() {
  drawBoard();
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (chessData[y][x] !== 0) {
        drawPieceStatic(x, y, chessData[y][x]);
      }
    }
  }
  if (confirmMode.value && previewX.value !== -1 && previewY.value !== -1) {
    drawPiecePreview(previewX.value, previewY.value, isBlackTurn.value ? 1 : 2);
  }
}

function drawPiecePreview(x, y, piece) {
  const centerX = cellSize / 2 + x * cellSize;
  const centerY = cellSize / 2 + y * cellSize;
  const radius = cellSize * 0.4;
  
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
  ctx.fillStyle = piece === 1 ? 'rgba(0, 0, 0, 0.5)' : 'rgba(255, 255, 255, 0.5)';
  ctx.fill();
}



function drawPieceStatic(x, y, piece) {
  const centerX = cellSize / 2 + x * cellSize;
  const centerY = cellSize / 2 + y * cellSize;
  const radius = cellSize * 0.4;

  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
  ctx.closePath();

  const gradient = ctx.createRadialGradient(
    centerX - 2,
    centerY - 2,
    radius * 0.1,
    centerX,
    centerY,
    radius
  );
  if (piece === 1) {
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

  const lastMove = moveHistory.value.pop();
  chessData[lastMove.y][lastMove.x] = 0;
  isBlackTurn.value = !isBlackTurn.value;
  movesCount.value--;
  confirmMode.value = false;
  previewX.value = -1;
  previewY.value = -1;
  drawAllPieces();
}

// --------- 重置棋盘 ---------
function resetGame() {
  clearInterval(timer.value);
  initData();
  initBoard();
  dialogVisible.value = false;
  confirmMode.value = false;

}
</script>
