<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>本格競馬レースシミュレーター (18頭・高低差・コース位置対応)</title>
<style>
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #1e252b;
    color: #f0f3f5;
    margin: 0;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  h1 { margin-bottom: 10px; font-size: 24px; }
  .controls {
    background: #2c353d;
    padding: 15px 20px;
    border-radius: 8px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  }
  label { font-size: 14px; font-weight: bold; }
  select, button {
    padding: 8px 12px;
    border-radius: 4px;
    border: none;
    font-size: 14px;
  }
  button {
    background: #27ae60;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
  }
  button:hover { background: #2ecc71; }
  button:disabled { background: #7f8c8d; cursor: not-allowed; }
  
  #canvas-container {
    position: relative;
    box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    border-radius: 12px;
    overflow: hidden;
    background: #0f1418;
  }
  canvas { display: block; }

  .results-panel {
    margin-top: 15px;
    width: 800px;
    background: #2c353d;
    padding: 15px;
    border-radius: 8px;
  }
  .results-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }
  .results-table th, .results-table td {
    padding: 6px 10px;
    text-align: center;
    border-bottom: 1px solid #3a4651;
  }
  .results-table th { background: #1e252b; }
  .waku-1 { background: #ffffff; color: #000; font-weight: bold; }
  .waku-2 { background: #222222; color: #fff; font-weight: bold; }
  .waku-3 { background: #e74c3c; color: #fff; font-weight: bold; }
  .waku-4 { background: #3498db; color: #fff; font-weight: bold; }
  .waku-5 { background: #f1c40f; color: #000; font-weight: bold; }
  .waku-6 { background: #2ecc71; color: #fff; font-weight: bold; }
  .waku-7 { background: #e67e22; color: #fff; font-weight: bold; }
  .waku-8 { background: #9b59b6; color: #fff; font-weight: bold; }
</style>
</head>
<body>

<h1>🏇 リアル競馬レース・シミュレーター</h1>

<div class="controls">
  <div>
    <label>競馬場: </label>
    <select id="trackSelect">
      <option value="tokyo">東京競馬場 (左回り / 直線長 / 坂あり)</option>
      <option value="nakayama">中山競馬場 (右回り / 急坂あり)</option>
      <option value="kyoto">京都競馬場 (右回り / 淀の坂)</option>
      <option value="hanshin">阪神競馬場 (右回り / 仁川の坂)</option>
    </select>
  </div>

  <div>
    <label>距離: </label>
    <select id="distanceSelect">
      <option value="1600">1600m (マイル)</option>
      <option value="2000" selected>2000m (中距離)</option>
      <option value="2400">2400m (クラシック)</option>
    </select>
  </div>

  <div>
    <label>馬場状態: </label>
    <select id="conditionSelect">
      <option value="good">良 (標準)</option>
      <option value="yielding">稍重 (荒れやすい)</option>
      <option value="soft">重 (スタミナ勝負)</option>
      <option value="bad">不良 (大波乱)</option>
    </select>
  </div>

  <div>
    <label>頭数: </label>
    <select id="horseCountSelect">
      <option value="8">8頭</option>
      <option value="12">12頭</option>
      <option value="16">16頭</option>
      <option value="18" selected>18頭 (フルゲート)</option>
    </select>
  </div>

  <button id="startBtn">レース出走！</button>
</div>

<div id="canvas-container">
  <canvas id="raceCanvas" width="800" height="500"></canvas>
</div>

<div class="results-panel">
  <h3>🏆 到着順位 / 入線結果</h3>
  <table class="results-table">
    <thead>
      <tr>
        <th>着順</th>
        <th>馬番</th>
        <th>馬名</th>
        <th>脚質</th>
        <th>タイム</th>
      </tr>
    </thead>
    <tbody id="resultBody">
      <tr><td colspan="5">レース開始ボタンを押してください</td></tr>
    </tbody>
  </table>
</div>

<script>
// --- 馬名ランダム生成用 ---
const nameParts1 = ["サイレンス", "ディープ", "オルフェ", "ゴールド", "キタサン", "アーモンド", "コントレイル", "イクイノ", "ウオッカ", "ダイワ", "メジロ", "シンボリ", "トウカイ", "スペシャル", "グラス"];
const nameParts2 = ["スズカ", "インパクト", "ーヴル", "シップ", "ブラック", "アイ", "ファン", "ノックス", "スカーレット", "マックイーン", "ルドルフ", "テイオー", "ウィーク", "ワンダー", "キング"];
const styles = ["逃げ", "先行", "差し", "追込"];

function generateHorseName(idx) {
  const p1 = nameParts1[idx % nameParts1.length];
  const p2 = nameParts2[(idx * 3) % nameParts2.length];
  return p1 + p2;
}

// --- 枠色クラス取得 ---
function getWakuClass(gate, total) {
  let waku = 1;
  if (total <= 8) waku = gate;
  else {
    waku = Math.ceil((gate / total) * 8);
  }
  return `waku-${Math.min(Math.max(waku, 1), 8)}`;
}

// --- コース定義＆パラメータ ---
const TRACK_SPECS = {
  tokyo: { name: "東京", dir: -1, slopeStart: 0.15, slopeEnd: 0.3, slopeType: "up", finishAngle: Math.PI / 2 }, // 左回り
  nakayama: { name: "中山", dir: 1, slopeStart: 0.85, slopeEnd: 0.98, slopeType: "up", finishAngle: -Math.PI / 2 }, // 右回り
  kyoto: { name: "京都", dir: 1, slopeStart: 0.35, slopeEnd: 0.5, slopeType: "down", finishAngle: -Math.PI / 2 },
  hanshin: { name: "阪神", dir: 1, slopeStart: 0.8, slopeEnd: 0.95, slopeType: "up", finishAngle: -Math.PI / 2 }
};

const canvas = document.getElementById('raceCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('startBtn');

let horses = [];
let isRacing = false;
let raceTime = 0;
let finishedHorses = [];
let trackConfig = {};

// --- 楕円コース上の座標計算 ---
function getCoursePosition(progress, lane, dir) {
  const cx = 400, cy = 250;
  const rx = 320 - lane * 10; 
  const ry = 180 - lane * 6;

  // 角度調整 (ゴール位置を基準点にする)
  const angle = trackConfig.finishAngle + (progress * Math.PI * 2 * dir);
  
  const x = cx + rx * Math.cos(angle);
  const y = cy + ry * Math.sin(angle);
  return { x, y, angle };
}

// --- 馬クラス ---
class Horse {
  constructor(id, name, number, total) {
    this.id = id;
    this.name = name;
    this.number = number;
    this.total = total;
    this.wakuClass = getWakuClass(number, total);
    
    // 基本能力 (能力に幅を持たせる)
    this.baseSpeed = 0.00085 + Math.random() * 0.0001;
    this.stamina = 0.85 + Math.random() * 0.3;
    this.style = styles[Math.floor(Math.random() * styles.length)];
    
    // スパート開始地点の分散 (展開のゆらぎ)
    this.spurtPoint = 0.65 + Math.random() * 0.15; 
    if (this.style === "追込") this.spurtPoint += 0.08;
    if (this.style === "逃げ") this.spurtPoint -= 0.1;

    this.reset();
  }

  reset() {
    this.progress = 0; // 0.0 ～ 1.0
    this.lane = this.number;
    this.currentStamina = this.stamina;
    this.speed = 0;
    this.finished = false;
    this.finishTime = 0;
    
    // 当日の体調・展開の気まぐれブレ (着順固定化の防止)
    this.conditionMod = 0.92 + Math.random() * 0.16; 
  }

  update(condition) {
    if (this.finished) return;

    // 馬場影響ブレ
    let condFactor = 1.0;
    if (condition === 'yielding') condFactor = 0.97 + (Math.random() * 0.06);
    if (condition === 'soft') condFactor = 0.93 + (Math.random() * 0.1);
    if (condition === 'bad') condFactor = 0.88 + (Math.random() * 0.15); // 不良馬場は大波乱

    // 脚質に応じたペース配分
    let targetPace = 1.0;
    if (this.progress < this.spurtPoint) {
      if (this.style === "逃げ") targetPace = 1.12;
      else if (this.style === "先行") targetPace = 1.05;
      else if (this.style === "差し") targetPace = 0.96;
      else if (this.style === "追込") targetPace = 0.90;
    } else {
      // スパート区間
      if (this.currentStamina > 0.1) {
        if (this.style === "追込") targetPace = 1.35;
        else if (this.style === "差し") targetPace = 1.25;
        else targetPace = 1.15;
      } else {
        // スタミナ切れ
        targetPace = 0.75;
      }
    }

    // 坂道の影響
    let slopeMod = 1.0;
    if (this.progress >= trackConfig.slopeStart && this.progress <= trackConfig.slopeEnd) {
      if (trackConfig.slopeType === "up") {
        slopeMod = 0.85; // 上り坂で減速＆スタミナ消費
        this.currentStamina -= 0.002;
      } else if (trackConfig.slopeType === "down") {
        slopeMod = 1.1; // 下り坂で加速
      }
    }

    // スピード計算
    this.speed = this.baseSpeed * this.conditionMod * condFactor * targetPace * slopeMod;
    
    // スタミナ消費
    this.currentStamina -= (this.speed * 0.4);
    
    // 位置更新
    this.progress += this.speed;

    if (this.progress >= 1.0) {
      this.progress = 1.0;
      this.finished = true;
      this.finishTime = raceTime;
      finishedHorses.push(this);
    }
  }
}

// --- 初期化 ---
function initRace() {
  const count = parseInt(document.getElementById('horseCountSelect').value);
  const trackKey = document.getElementById('trackSelect').value;
  const dist = parseInt(document.getElementById('distanceSelect').value);
  
  trackConfig = TRACK_SPECS[trackKey];
  
  // スタート地点計算（距離に応じてスタート地点をズラす）
  // 2000mを1周(1.0)とした時の相対オフセット計算
  const lapRatio = dist / 2000;
  const startOffset = (1.0 - (lapRatio % 1.0)) % 1.0;

  horses = [];
  finishedHorses = [];
  raceTime = 0;

  for (let i = 1; i <= count; i++) {
    const h = new Horse(i, generateHorseName(i), i, count);
    h.progress = startOffset; // スタート位置のセット
    horses.push(h);
  }

  drawCourse();
}

// --- 描画処理 ---
function drawCourse() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. ターフ（芝生）
  ctx.fillStyle = "#1e824c";
  ctx.beginPath();
  ctx.ellipse(400, 250, 340, 200, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#0f1418";
  ctx.beginPath();
  ctx.ellipse(400, 250, 180, 90, 0, 0, Math.PI * 2);
  ctx.fill();

  // 2. 坂道エリアの描画（ビジュアル表示）
  const sStart = getCoursePosition(trackConfig.slopeStart, 9, trackConfig.dir);
  const sEnd = getCoursePosition(trackConfig.slopeEnd, 9, trackConfig.dir);
  
  ctx.lineWidth = 14;
  ctx.strokeStyle = trackConfig.slopeType === "up" ? "rgba(230, 126, 34, 0.6)" : "rgba(52, 152, 219, 0.6)";
  ctx.beginPath();
  ctx.arc(400, 250, 250, trackConfig.finishAngle + trackConfig.slopeStart * Math.PI*2 * trackConfig.dir, trackConfig.finishAngle + trackConfig.slopeEnd * Math.PI*2 * trackConfig.dir, trackConfig.dir < 0);
  ctx.stroke();

  // 坂道ラベル
  ctx.fillStyle = "#fff";
  ctx.font = "12px sans-serif";
  ctx.fillText(trackConfig.slopeType === "up" ? "▲ 坂道 (消費強)" : "▼ 下り坂 (加速)", sStart.x, sStart.y);

  // 3. ゴール線（赤）
  const goalPosInner = getCoursePosition(0, 1, trackConfig.dir);
  const goalPosOuter = getCoursePosition(0, 18, trackConfig.dir);
  ctx.strokeStyle = "#e74c3c";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(goalPosInner.x, goalPosInner.y);
  ctx.lineTo(goalPosOuter.x, goalPosOuter.y);
  ctx.stroke();
  ctx.fillStyle = "#e74c3c";
  ctx.fillText("GOAL", goalPosOuter.x - 15, goalPosOuter.y - 8);

  // 4. スタート線（緑）
  const startOffset = horses[0] ? horses[0].progress : 0;
  const startPosInner = getCoursePosition(startOffset, 1, trackConfig.dir);
  const startPosOuter = getCoursePosition(startOffset, 18, trackConfig.dir);
  ctx.strokeStyle = "#2ecc71";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(startPosInner.x, startPosInner.y);
  ctx.lineTo(startPosOuter.x, startPosOuter.y);
  ctx.stroke();
  ctx.fillStyle = "#2ecc71";
  ctx.fillText("START", startPosOuter.x - 20, startPosOuter.y - 8);

  // 5. 馬の描画
  horses.forEach(h => {
    const pos = getCoursePosition(h.progress, h.lane, trackConfig.dir);

    // 馬の円
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 7, 0, Math.PI * 2);
    ctx.fillStyle = getWakuColor(h.wakuClass);
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 1;
    ctx.stroke();

    // 馬番テキスト
    ctx.fillStyle = (h.wakuClass === 'waku-1') ? '#000' : '#fff';
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(h.number, pos.x, pos.y);
  });
}

function getWakuColor(wakuClass) {
  const colors = {
    'waku-1': '#ffffff', 'waku-2': '#222222', 'waku-3': '#e74c3c',
    'waku-4': '#3498db', 'waku-5': '#f1c40f', 'waku-6': '#2ecc71',
    'waku-7': '#e67e22', 'waku-8': '#9b59b6'
  };
  return colors[wakuClass] || '#fff';
}

// --- メインループ ---
function gameLoop() {
  if (!isRacing) return;

  const condition = document.getElementById('conditionSelect').value;
  raceTime += 0.016;

  let allFinished = true;
  horses.forEach(h => {
    h.update(condition);
    if (!h.finished) allFinished = false;
  });

  drawCourse();

  if (allFinished) {
    isRacing = false;
    startBtn.disabled = false;
    showResults();
  } else {
    requestAnimationFrame(gameLoop);
  }
}

// --- 結果表示 ---
function showResults() {
  const tbody = document.getElementById('resultBody');
  tbody.innerHTML = '';

  finishedHorses.forEach((h, index) => {
    const tr = document.createElement('tr');
    
    // タイム変換 (仮想タイム)
    const timeFormatted = (60 + h.finishTime * 8).toFixed(1) + "秒";

    tr.innerHTML = `
      <td><strong>${index + 1}着</strong></td>
      <td><span class="${h.wakuClass}" style="padding:2px 6px; border-radius:3px;">${h.number}</span></td>
      <td>${h.name}</td>
      <td>${h.style}</td>
      <td>${timeFormatted}</td>
    `;
    tbody.appendChild(tr);
  });
}

// --- イベント登録 ---
startBtn.addEventListener('click', () => {
  initRace();
  isRacing = true;
  startBtn.disabled = true;
  gameLoop();
});

// 初期表示
initRace();
</script>

</body>
</html>
