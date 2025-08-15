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
    "
  >
    <!-- 顶部信息显示 -->
    <v-chip-group>
      <v-chip>轮到 {{ isBlackTurn ? "你 (黑棋)" : "AI (白棋)" }}</v-chip>
      <v-chip>{{ formatTime(timeElapsed) }}</v-chip>
      <v-chip>第 {{ movesCount }} 手</v-chip>
    </v-chip-group>

    <!-- 棋盘 -->
    <div style="width: 100%; display: flex; justify-content: center">
      <canvas
        ref="board"
        style="
          width: 90%;
          min-width: 220px;
          max-width: 280px;
          height: auto;
          border: 1px solid #333;
          box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
        "
      ></canvas>
    </div>

    <!-- 操作按钮 -->
    <div
      style="margin: 10px 0; display: flex; justify-content: center; gap: 10px"
    >
      <v-btn
        @click="undoMove"
        :disabled="moveHistory.length < 2 || gameOver || aiThinking"
        >悔棋</v-btn
      >
      <v-btn @click="resetGame">重置棋盘</v-btn>
      <v-btn v-if="gameOver" @click="resetGame">再来一次</v-btn>
    </div>

    <!-- 游戏结束弹窗 -->
    <v-dialog v-model="dialogVisible" max-width="300">
      <v-card>
        <v-card-title class="headline">游戏结束</v-card-title>
        <v-card-text>{{ winnerText }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialogVisible = false">关闭</v-btn>
          <v-btn color="primary" @click="resetGame">再来一局</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, defineProps } from "vue";
import chessDownSound from "../assets/audio/chess_down.mp3";

// --------- Props ---------
const props = defineProps({
  difficulty: {
    type: String,
    default: "medium",
  },
});

// --------- 类型定义 ---------
type Piece = 0 | 1 | 2;
interface Move {
  x: number;
  y: number;
  piece: Piece;
}
interface Point {
  x: number;
  y: number;
}

// --------- 响应式数据 ---------
const board = ref<HTMLCanvasElement | null>(null);
const size = 15;
let ctx: CanvasRenderingContext2D | null = null;
let cellSize = 0;

let chessData: Piece[][] = [];
const isBlackTurn = ref(true);
const gameOver = ref(false);
const canMove = ref(true);
const moveHistory = ref<Move[]>([]);
const timeElapsed = ref(0);
const timer = ref<number | null>(null);
const dialogVisible = ref(false);
const winnerText = ref("");
const movesCount = ref(0);

// 预览落子
const confirmMode = ref(false);
const previewX = ref(-1);
const previewY = ref(-1);

// 胜利线
const winLineState = ref<Point[] | null>(null);

// AI 控制
const aiThinking = ref(false);

// -------- 生命周期 --------
onMounted(() => {
  initData();
  initBoard();
  window.addEventListener("resize", initBoard);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", initBoard);
  clearTimer();
});

// -------- 初始化数据 --------
function initData() {
  chessData = Array.from({ length: size }, () => Array(size).fill(0));
  isBlackTurn.value = true;
  gameOver.value = false;
  canMove.value = true;
  moveHistory.value = [];
  timeElapsed.value = 0;
  movesCount.value = 0;
  winLineState.value = null;
  aiThinking.value = false;
}

// -------- 定时器 --------
function startTimer() {
  if (!timer.value) {
    timer.value = window.setInterval(() => {
      if (!gameOver.value) timeElapsed.value++;
    }, 1000);
  }
}

function clearTimer() {
  if (timer.value !== null) {
    clearInterval(timer.value);
    timer.value = null;
  }
}

// -------- 格式化时间 --------
function formatTime(seconds: number) {
  const m = String(Math.floor(seconds / 60)).padStart(2, "0");
  const s = String(seconds % 60).padStart(2, "0");
  return `${m}:${s}`;
}

// -------- 初始化棋盘 --------
function initBoard() {
  if (!board.value) return;
  ctx = board.value.getContext("2d");
  if (!ctx) return;

  const rect = board.value.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const canvasSize = Math.min(rect.width, 600);

  board.value.width = canvasSize * dpr;
  board.value.height = canvasSize * dpr;
  ctx.scale(dpr, dpr);

  cellSize = Math.max(canvasSize / size, 10);

  drawBoard();
  drawAllPieces();

  board.value.onclick = handleClick;
}

// -------- 点击落子 --------
function handleClick(e: MouseEvent) {
  if (!canMove.value || gameOver.value || aiThinking.value || !board.value)
    return;

  const rect = board.value.getBoundingClientRect();
  const x = Math.round((e.clientX - rect.left - cellSize / 2) / cellSize);
  const y = Math.round((e.clientY - rect.top - cellSize / 2) / cellSize);
  if (x < 0 || x >= size || y < 0 || y >= size) return;

  if (!confirmMode.value) previewMove(x, y);
  else confirmMove(x, y);
}

// -------- 确认落子 --------
function confirmMove(x: number, y: number) {
  if (chessData[y][x] !== 0) {
    confirmMode.value = false;
    previewX.value = -1;
    previewY.value = -1;
    drawAllPieces();
    return;
  }

  const piece: Piece = 1; // 玩家永远黑棋
  if (moveHistory.value.length === 0) startTimer();
  movesCount.value++;

  drawPieceAnimated(x, y, piece, () => {
    checkGameOver(x, y);
    if (!gameOver.value) {
      // AI 回合
      aiMove();
    }
  });

  confirmMode.value = false;
  previewX.value = -1;
  previewY.value = -1;
}

// -------- 预览落子 --------
function previewMove(x: number, y: number) {
  if (chessData[y][x] === 0) {
    confirmMode.value = true;
    previewX.value = x;
    previewY.value = y;
    drawAllPieces();
    drawPiecePreview(x, y, 1);
  }
}

// -------- AI 落子 --------
function aiMove() {
  aiThinking.value = true;
  setTimeout(() => {
    const { x, y } = findBestMove();
    movesCount.value++;
    drawPieceAnimated(x, y, 2, () => {
      checkGameOver(x, y);
      aiThinking.value = false;
    });
  });
}

// -------- 简单评分算法 --------
function findBestMove(): { x: number; y: number } {
  let bestScore = -Infinity;
  let bestMove = { x: 0, y: 0 };

  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (chessData[y][x] !== 0) continue;
      const score = evaluateMove(x, y, 2) + evaluateMove(x, y, 1) * 0.8;
      if (score > bestScore) {
        bestScore = score;
        bestMove = { x, y };
      }
    }
  }

  return bestMove;
}

// -------- 评分函数 --------
function evaluateMove(x: number, y: number, color: 1 | 2): number {
  let score = 0;
  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];

  // 根据难度调整AI行为
  let depth = 5; // 默认搜索深度
  let defenseFactor = 0.8; // 防守权重

  switch (props.difficulty) {
    case "simple":
      depth = 3;
      defenseFactor = 0.5;
      break;
    case "medium":
      depth = 5;
      defenseFactor = 0.8;
      break;
    case "hard":
      depth = 7;
      defenseFactor = 1.0;
      break;
    case "expert":
      depth = 9;
      defenseFactor = 1.2;
      break;
    case "nightmare":
      depth = 20;
      defenseFactor = 1.7;
      break;
  }

  for (const { dx, dy } of dirs) {
    let count = 0;
    for (let step = 1; step < depth; step++) {
      const nx = x + dx * step;
      const ny = y + dy * step;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) count++;
      else break;
    }
    for (let step = 1; step < depth; step++) {
      const nx = x - dx * step;
      const ny = y - dy * step;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) count++;
      else break;
    }

    // 根据难度调整得分计算
    if (color === 2) {
      // AI棋子
      score += Math.pow(10, count);
    } else {
      // 玩家棋子
      score += Math.pow(10, count) * defenseFactor;
    }
  }

  return score;
}

// -------- 检查游戏结束 --------
function checkGameOver(x: number, y: number) {
  const winLine = checkWin(x, y);
  if (winLine) {
    gameOver.value = true;
    clearTimer();
    winLineState.value = winLine;
    winnerText.value = `${
      chessData[y][x] === 1 ? "恭喜你战胜了AI" : "你被AI击败，去多加练习吧~"
    }`;
    dialogVisible.value = true;
  } else {
    isBlackTurn.value = !isBlackTurn.value;
  }
}

// -------- 绘制棋盘 --------
function drawBoard() {
  if (!ctx || !board.value) return;

  const canvasWidth = board.value.getBoundingClientRect().width;

  // 背景渐变
  const gradient = ctx.createLinearGradient(0, 0, canvasWidth, canvasWidth);
  gradient.addColorStop(0, "#f9e4b7");
  gradient.addColorStop(1, "#e5c78a");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvasWidth, canvasWidth);

  ctx.strokeStyle = "#333";
  ctx.lineWidth = 1;

  // 网格线
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

  drawStarPoints();
}

// -------- 星位 --------
function drawStarPoints() {
  if (!ctx) return;

  const points: Point[] = [];
  if (size === 15) {
    points.push(
      { x: 3, y: 3 },
      { x: 11, y: 3 },
      { x: 3, y: 11 },
      { x: 11, y: 11 },
      { x: 7, y: 7 }
    );
  } else if (size === 19) {
    const positions = [3, 9, 15];
    for (let x of positions) for (let y of positions) points.push({ x, y });
  }

  points.forEach((p) => {
    const cx = cellSize / 2 + p.x * cellSize;
    const cy = cellSize / 2 + p.y * cellSize;
    const r = cellSize * 0.1;
    ctx!.beginPath();
    ctx!.arc(cx, cy, r, 0, Math.PI * 2);
    ctx!.fillStyle = "#333";
    ctx!.fill();
  });
}

// -------- 绘制动画棋子 --------
function drawPieceAnimated(
  x: number,
  y: number,
  piece: 1 | 2,
  callback?: () => void
) {
  const duration = 100;
  const startTime = performance.now();
  const startRadius = 2;
  const endRadius = Math.max(cellSize * 0.4, 2);

  const drawExistingPieces = () => {
    drawBoard();
    drawAllPiecesStatic();
    if (winLineState.value) drawWinLine(winLineState.value);
  };

  const animate = (currentTime: number) => {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);

    let currentRadius = startRadius + (endRadius - startRadius) * progress;
    currentRadius = Math.max(currentRadius, 2);

    drawExistingPieces();

    const centerX = cellSize / 2 + x * cellSize;
    const centerY = cellSize / 2 + y * cellSize;

    ctx!.beginPath();
    ctx!.arc(centerX, centerY, currentRadius, 0, 2 * Math.PI);
    ctx!.closePath();

    const gradient = ctx!.createRadialGradient(
      centerX - 2,
      centerY - 2,
      Math.max(currentRadius * 0.1, 1),
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

    ctx!.fillStyle = gradient;
    ctx!.fill();

    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      chessData[y][x] = piece;
      moveHistory.value.push({ x, y, piece });
      if (callback) callback();
      new Audio(chessDownSound).play();
    }
  };

  requestAnimationFrame(animate);
}

// -------- 绘制所有棋子 --------
function drawAllPieces() {
  drawBoard();
  drawAllPiecesStatic();

  if (confirmMode.value && previewX.value !== -1 && previewY.value !== -1)
    drawPiecePreview(previewX.value, previewY.value, 1);

  if (winLineState.value) drawWinLine(winLineState.value);
}

function drawAllPiecesStatic() {
  for (let y = 0; y < size; y++)
    for (let x = 0; x < size; x++)
      if (chessData[y][x] !== 0) drawPieceStatic(x, y, chessData[y][x]);
}

// -------- 绘制预览棋子 --------
function drawPiecePreview(x: number, y: number, piece: Piece) {
  const cx = cellSize / 2 + x * cellSize;
  const cy = cellSize / 2 + y * cellSize;
  ctx!.beginPath();
  ctx!.arc(cx, cy, cellSize * 0.4, 0, Math.PI * 2);
  ctx!.fillStyle = piece === 1 ? "rgba(0,0,0,0.5)" : "rgba(255,255,255,0.5)";
  ctx!.fill();
}

// -------- 绘制静态棋子 --------
function drawPieceStatic(x: number, y: number, piece: Piece) {
  const cx = cellSize / 2 + x * cellSize;
  const cy = cellSize / 2 + y * cellSize;
  const radius = cellSize * 0.4;

  const grad = ctx!.createRadialGradient(
    cx - 2,
    cy - 2,
    radius * 0.1,
    cx,
    cy,
    radius
  );
  if (piece === 1) {
    grad.addColorStop(0, "#555");
    grad.addColorStop(1, "#000");
  } else {
    grad.addColorStop(0, "#fff");
    grad.addColorStop(1, "#ddd");
  }

  ctx!.beginPath();
  ctx!.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx!.closePath();
  ctx!.fillStyle = grad;
  ctx!.fill();
}

// -------- 胜利检测 --------
function checkWin(x: number, y: number): Point[] | null {
  const color = chessData[y][x];
  if (color === 0) return null;

  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];

  for (const { dx, dy } of dirs) {
    const winLine: Point[] = [{ x, y }];
    let count = 1;

    // 正方向
    for (let i = 1; ; i++) {
      const nx = x + dx * i;
      const ny = y + dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        winLine.push({ x: nx, y: ny });
        count++;
      } else break;
    }

    // 反方向
    for (let i = 1; ; i++) {
      const nx = x - dx * i;
      const ny = y - dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        winLine.unshift({ x: nx, y: ny });
        count++;
      } else break;
    }

    if (count >= 5) return winLine;
  }

  return null;
}

// -------- 绘制胜利线 --------
function drawWinLine(winLine: Point[]) {
  if (!ctx || winLine.length === 0) return;
  ctx.strokeStyle = "green";
  ctx.lineWidth = 5;
  ctx.beginPath();
  const start = winLine[0];
  const end = winLine[winLine.length - 1];
  ctx.moveTo(
    cellSize / 2 + start.x * cellSize,
    cellSize / 2 + start.y * cellSize
  );
  ctx.lineTo(cellSize / 2 + end.x * cellSize, cellSize / 2 + end.y * cellSize);
  ctx.stroke();
}

// -------- 悔棋 --------
function undoMove() {
  if (moveHistory.value.length < 2 || gameOver.value || aiThinking.value)
    return;

  // 悔棋两步：玩家和AI的棋子
  for (let i = 0; i < 2; i++) {
    const last = moveHistory.value.pop()!;
    chessData[last.y][last.x] = 0;
  }
  // 悔棋后，轮到玩家下棋
  isBlackTurn.value = true;
  movesCount.value -= 2;
  confirmMode.value = false;
  previewX.value = -1;
  previewY.value = -1;
  winLineState.value = null;
  drawAllPieces();
}

// -------- 重置棋盘 --------
function resetGame() {
  clearTimer();
  winLineState.value = null;
  initData();
  initBoard();
  dialogVisible.value = false;
  confirmMode.value = false;
}
</script>
