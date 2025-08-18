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
      <v-chip>轮到 {{ isBlackTurn ? "黑棋" : "白棋" }}</v-chip>
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
      <v-btn @click="undoMove" :disabled="moveHistory.length === 0 || gameOver"
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

    <!-- 禁手提示弹窗 -->
    <v-dialog v-model="forbiddenDialogVisible" max-width="300">
      <v-card>
        <v-card-title class="headline">禁手提示</v-card-title>
        <v-card-text>{{ forbiddenText }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="forbiddenDialogVisible = false"
            >确定</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import chessDownSound from "../assets/audio/chess_down.mp3";

const props = defineProps({
  doubleThree: { type: Boolean, default: true },
  doubleFour: { type: Boolean, default: true },
  longConnect: { type: Boolean, default: true },
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
const forbiddenDialogVisible = ref(false);
const forbiddenText = ref("");
const movesCount = ref(0);

// 预览落子
const confirmMode = ref(false);
const previewX = ref(-1);
const previewY = ref(-1);

// 胜利线
const winLineState = ref<Point[] | null>(null);

// --------- 生命周期 ---------
onMounted(() => {
  initData();
  initBoard();
  window.addEventListener("resize", initBoard);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", initBoard);
  clearTimer();
});

// --------- 初始化数据 ---------
function initData() {
  chessData = Array.from({ length: size }, () => Array(size).fill(0));
  isBlackTurn.value = true;
  gameOver.value = false;
  canMove.value = true;
  moveHistory.value = [];
  timeElapsed.value = 0;
  movesCount.value = 0;
  winLineState.value = null;
}

// --------- 定时器 ---------
function startTimer() {
  timer.value = window.setInterval(() => {
    if (!gameOver.value) timeElapsed.value++;
  }, 1000);
}

function clearTimer() {
  if (timer.value !== null) clearInterval(timer.value);
}

// --------- 格式化时间 ---------
function formatTime(seconds: number) {
  const m = String(Math.floor(seconds / 60)).padStart(2, "0");
  const s = String(seconds % 60).padStart(2, "0");
  return `${m}:${s}`;
}

// --------- 初始化棋盘 ---------
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

// --------- 绘制棋盘 ---------
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

// --------- 星位 ---------
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

// --------- 点击落子 ---------
function handleClick(e: MouseEvent) {
  if (!canMove.value || gameOver.value || !board.value) return;

  const rect = board.value.getBoundingClientRect();
  const x = Math.round((e.clientX - rect.left - cellSize / 2) / cellSize);
  const y = Math.round((e.clientY - rect.top - cellSize / 2) / cellSize);
  if (x < 0 || x >= size || y < 0 || y >= size) return;

  if (confirmMode.value) {
    confirmMove(x, y);
  } else {
    previewMove(x, y);
  }
}

// --------- 确认落子 ---------
function confirmMove(x: number, y: number) {
  if (previewX.value !== x || previewY.value !== y) {
    confirmMode.value = false;
    previewX.value = -1;
    previewY.value = -1;
    drawAllPieces();
    return;
  }

  if (chessData[y][x] !== 0) {
    confirmMode.value = false;
    previewX.value = -1;
    previewY.value = -1;
    drawAllPieces();
    return;
  }

  // 禁手判断
  if (isBlackTurn.value && isForbiddenMove(x, y)) {
    forbiddenText.value = "黑棋禁手！不能落子。";
    forbiddenDialogVisible.value = true;
    confirmMode.value = false;
    previewX.value = -1;
    previewY.value = -1;
    drawAllPieces();
    return;
  }

  const piece: Piece = isBlackTurn.value ? 1 : 2;
  if (moveHistory.value.length === 0) startTimer();
  movesCount.value++;

  drawPieceAnimated(x, y, piece);
  confirmMode.value = false;
  previewX.value = -1;
  previewY.value = -1;
}

// --------- 预览落子 ---------
function previewMove(x: number, y: number) {
  if (chessData[y][x] === 0) {
    confirmMode.value = true;
    previewX.value = x;
    previewY.value = y;
    drawAllPieces();
    drawPiecePreview(x, y, isBlackTurn.value ? 1 : 2);
  }
}

// --------- 绘制动画棋子 ---------
function drawPieceAnimated(x: number, y: number, piece: 1 | 2) {
  const duration = 100;
  const startTime = performance.now();
  const startRadius = 2; // 避免 r0 = 0
  const endRadius = Math.max(cellSize * 0.4, 2);

  const drawExistingPieces = () => {
    drawBoard();
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        if (chessData[i][j] !== 0)
          drawPieceStatic(j, i, chessData[i][j] as 1 | 2);
      }
    }

    if (gameOver.value && winLineState.value) {
      drawWinLine(winLineState.value);
    }
  };

  const animate = (currentTime: number) => {
    const elapsedTime = currentTime - startTime;
    const progress = Math.min(elapsedTime / duration, 1);

    let currentRadius = startRadius + (endRadius - startRadius) * progress;
    currentRadius = Math.max(currentRadius, 2); // 确保 r0 > 0

    drawExistingPieces();

    const centerX = cellSize / 2 + x * cellSize;
    const centerY = cellSize / 2 + y * cellSize;

    ctx!.beginPath();
    ctx!.arc(centerX, centerY, currentRadius, 0, 2 * Math.PI);
    ctx!.closePath();

    const gradient = ctx!.createRadialGradient(
      centerX - 2,
      centerY - 2,
      Math.max(currentRadius * 0.1, 1), // 避免 r0 < 0
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
      // 动画完成后写入棋盘数据
      chessData[y][x] = piece;
      moveHistory.value.push({ x, y, piece });
      new Audio(chessDownSound).play();

      const winLine = checkWin(x, y);
      if (winLine) {
        gameOver.value = true;
        clearInterval(timer.value!);
        winLineState.value = winLine;
        winnerText.value = `${piece === 1 ? "黑棋" : "白棋"}胜利！`;
        dialogVisible.value = true;
      }

      isBlackTurn.value = !isBlackTurn.value;
      confirmMode.value = false;
      previewX.value = -1;
      previewY.value = -1;

      drawAllPieces();
    }
  };

  requestAnimationFrame(animate);
}

// --------- 绘制所有棋子 ---------
function drawAllPieces() {
  drawBoard();
  drawAllPiecesStatic();

  if (confirmMode.value && previewX.value !== -1 && previewY.value !== -1)
    drawPiecePreview(previewX.value, previewY.value, isBlackTurn.value ? 1 : 2);

  if (winLineState.value) drawWinLine(winLineState.value);
}

function drawAllPiecesStatic() {
  const lastMove = moveHistory.value.length > 0 ? moveHistory.value[moveHistory.value.length - 1] : null;
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (chessData[y][x] !== 0) {
        const isLastMove = !!lastMove && lastMove.x === x && lastMove.y === y;
        drawPieceStatic(x, y, chessData[y][x], isLastMove);
      }
    }
  }
}

// --------- 绘制预览棋子 ---------
function drawPiecePreview(x: number, y: number, piece: Piece) {
  const cx = cellSize / 2 + x * cellSize;
  const cy = cellSize / 2 + y * cellSize;
  ctx!.beginPath();
  ctx!.arc(cx, cy, cellSize * 0.4, 0, Math.PI * 2);
  ctx!.fillStyle = piece === 1 ? "rgba(0,0,0,0.5)" : "rgba(255,255,255,0.5)";
  ctx!.fill();
}

// --------- 绘制静态棋子 ---------
function drawPieceStatic(x: number, y: number, piece: Piece, isLastMove: boolean = false) {
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

  if (isLastMove) {
    ctx!.beginPath();
    ctx!.arc(cx, cy, radius + 2, 0, Math.PI * 2);
    ctx!.strokeStyle = "red";
    ctx!.lineWidth = 2;
    ctx!.stroke();
  }
}

// --------- 胜利检测 ---------
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

// --------- 禁手判断 ---------
function isForbiddenMove(x: number, y: number): boolean {
  // 只有黑棋有禁手
  if (!isBlackTurn.value) return false;

  // 模拟落子
  chessData[y][x] = 1; // 假设是黑棋

  let forbidden = false;

  // 三三禁手
  if (props.doubleThree && checkDoubleThree(x, y)) {
    forbidden = true;
  }

  // 四四禁手
  if (!forbidden && props.doubleFour && checkDoubleFour(x, y)) {
    forbidden = true;
  }

  // 长连禁手
  if (!forbidden && props.longConnect && checkLongConnect(x, y)) {
    forbidden = true;
  }

  // 撤销模拟落子
  chessData[y][x] = 0;

  return forbidden;
}

// 检查三三禁手
function checkDoubleThree(x: number, y: number): boolean {
  let count = 0;
  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];

  for (const { dx, dy } of dirs) {
    const liveThreeCount = countLiveThrees(x, y, dx, dy);
    if (liveThreeCount >= 2) {
      count++;
    }
  }
  return count >= 2;
}

// 检查活三
function countLiveThrees(x: number, y: number, dx: number, dy: number): number {
  let liveThreeCount = 0;

  // 方向一
  const line1 = getLine(x, y, dx, dy);
  if (isLiveThree(line1)) liveThreeCount++;

  // 方向二
  const line2 = getLine(x, y, -dx, -dy);
  if (isLiveThree(line2)) liveThreeCount++;

  return liveThreeCount;
}

// 获取指定方向的棋子序列
function getLine(x: number, y: number, dx: number, dy: number): Piece[] {
  const line: Piece[] = [];
  for (let i = -4; i <= 4; i++) {
    const nx = x + dx * i;
    const ny = y + dy * i;
    if (nx >= 0 && nx < size && ny >= 0 && ny < size) {
      line.push(chessData[ny][nx]);
    } else {
      line.push(-1 as Piece); // 边界外视为-1
    }
  }
  return line;
}

// 判断是否为活三
function isLiveThree(line: Piece[]): boolean {
  // 活三的模式，例如：01110 (0代表空，1代表黑棋)
  // 简化判断，实际需要更复杂的模式匹配
  const patterns = [
    [0, 1, 1, 1, 0], // 眠三
    [0, 1, 0, 1, 1, 0], // 跳三
    [0, 1, 1, 0, 1, 0], // 跳三
  ];

  for (const pattern of patterns) {
    for (let i = 0; i <= line.length - pattern.length; i++) {
      let match = true;
      for (let j = 0; j < pattern.length; j++) {
        if (pattern[j] === 0 && line[i + j] !== 0) {
          match = false;
          break;
        }
        if (pattern[j] === 1 && line[i + j] !== 1) {
          match = false;
          break;
        }
      }
      if (match) return true;
    }
  }
  return false;
}

// 检查四四禁手
function checkDoubleFour(x: number, y: number): boolean {
  let count = 0;
  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];

  for (const { dx, dy } of dirs) {
    const liveFourCount = countLiveFours(x, y, dx, dy);
    if (liveFourCount >= 2) {
      count++;
    }
  }
  return count >= 2;
}

// 检查活四
function countLiveFours(x: number, y: number, dx: number, dy: number): number {
  let liveFourCount = 0;

  // 方向一
  const line1 = getLine(x, y, dx, dy);
  if (isLiveFour(line1)) liveFourCount++;

  // 方向二
  const line2 = getLine(x, y, -dx, -dy);
  if (isLiveFour(line2)) liveFourCount++;

  return liveFourCount;
}

// 判断是否为活四
function isLiveFour(line: Piece[]): boolean {
  // 活四的模式，例如：011110
  const patterns = [
    [0, 1, 1, 1, 1, 0], // 活四
    [1, 0, 1, 1, 1, 0], // 跳活四
    [0, 1, 0, 1, 1, 1, 0], // 跳活四
    [0, 1, 1, 0, 1, 1, 0], // 跳活四
    [0, 1, 1, 1, 0, 1, 0], // 跳活四
  ];

  for (const pattern of patterns) {
    for (let i = 0; i <= line.length - pattern.length; i++) {
      let match = true;
      for (let j = 0; j < pattern.length; j++) {
        if (pattern[j] === 0 && line[i + j] !== 0) {
          match = false;
          break;
        }
        if (pattern[j] === 1 && line[i + j] !== 1) {
          match = false;
          break;
        }
      }
      if (match) return true;
    }
  }
  return false;
}

// 检查长连禁手
function checkLongConnect(x: number, y: number): boolean {
  const color = 1; // 黑棋
  const dirs = [
    { dx: 1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 1, dy: 1 },
    { dx: 1, dy: -1 },
  ];

  for (const { dx, dy } of dirs) {
    let count = 1;
    // 正方向
    for (let i = 1; ; i++) {
      const nx = x + dx * i;
      const ny = y + dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        count++;
      } else break;
    }

    // 反方向
    for (let i = 1; ; i++) {
      const nx = x - dx * i;
      const ny = y - dy * i;
      if (nx < 0 || nx >= size || ny < 0 || ny >= size) break;
      if (chessData[ny][nx] === color) {
        count++;
      } else break;
    }

    if (count > 5) return true;
  }
  return false;
}

// --------- 绘制胜利线 ---------
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

// --------- 悔棋 ---------
function undoMove() {
  if (moveHistory.value.length === 0 || gameOver.value) return;
  const last = moveHistory.value.pop()!;
  chessData[last.y][last.x] = 0;
  isBlackTurn.value = !isBlackTurn.value;
  movesCount.value--;
  confirmMode.value = false;
  previewX.value = -1;
  previewY.value = -1;
  winLineState.value = null;
  drawAllPieces();
}

// --------- 重置棋盘 ---------
function resetGame() {
  clearTimer();
  winLineState.value = null;
  initData();
  initBoard();
  dialogVisible.value = false;
  forbiddenDialogVisible.value = false;
  confirmMode.value = false;
}
</script>
