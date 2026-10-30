import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="JRA 週末重賞 究極精密シミュレーター Pro 2026",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .stMultiSelect, .stSelectbox, .stNumberInput, .stButton, input, select {
        touch-action: manipulation !important;
        pointer-events: auto !important;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        background-color: #080c14;
    }
    .hero-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 10px;
        border-left: 4px solid #38bdf8;
        padding-left: 10px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            height: 48px;
            font-size: 15px !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-box">
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">🏇 JRA週末重賞 究極精密シミュレーター <span style="color: #38bdf8; font-size: 18px;">PRO 2026</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">土曜：ファンタジーS ＆ 日曜：天皇賞（秋） | リアルタイムアニメーション ＆ 100回モンテカルロ完全対応</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース：ファンタジーS（土曜・京都芝1400m外・全11頭）
@st.cache_data
def get_fantasy_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "レニュアージュ",
          "jockey": "西村淳也",
          "style": "逃げ",
          "speed": 93,
          "stamina": 90,
          "power": 91,
          "heavy": 91,
          "burst": 92,
          "odds": 12.0,
          "sire": "コントレイル",
      },
      {
          "num": 2,
          "horse": "セイウンマイラヴ",
          "jockey": "田山旺佑",
          "style": "逃げ",
          "speed": 92,
          "stamina": 89,
          "power": 90,
          "heavy": 90,
          "burst": 91,
          "odds": 25.0,
          "sire": "カラヴァッジオ",
      },
      {
          "num": 3,
          "horse": "ビスケットサンド",
          "jockey": "北村友一",
          "style": "差し",
          "speed": 94,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 94,
          "odds": 6.5,
          "sire": "モーリス",
      },
      {
          "num": 4,
          "horse": "ニクスルーナ",
          "jockey": "岩田望来",
          "style": "差し",
          "speed": 91,
          "stamina": 91,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 35.0,
          "sire": "キズナ",
      },
      {
          "num": 5,
          "horse": "バタフライ",
          "jockey": "原田和真",
          "style": "差し",
          "speed": 90,
          "stamina": 92,
          "power": 93,
          "heavy": 94,
          "burst": 90,
          "odds": 45.0,
          "sire": "ロードカナロア",
      },
      {
          "num": 6,
          "horse": "イモージェン",
          "jockey": "C.デムーロ",
          "style": "差し",
          "speed": 95,
          "stamina": 93,
          "power": 93,
          "heavy": 93,
          "burst": 96,
          "odds": 4.0,
          "sire": "サリオス",
      },
      {
          "num": 7,
          "horse": "シャンデヴァーグ",
          "jockey": "鮫島克駿",
          "style": "差し",
          "speed": 92,
          "stamina": 92,
          "power": 91,
          "heavy": 91,
          "burst": 93,
          "odds": 18.0,
          "sire": "ロードカナロア",
      },
      {
          "num": 8,
          "horse": "ブライトスクリプト",
          "jockey": "池添謙一",
          "style": "差し",
          "speed": 96,
          "stamina": 94,
          "power": 93,
          "heavy": 92,
          "burst": 97,
          "odds": 3.0,
          "sire": "サートゥルナーリア",
      },
      {
          "num": 9,
          "horse": "ベニバナ",
          "jockey": "幸英明",
          "style": "差し",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 80.0,
          "sire": "キタサンブラック",
      },
      {
          "num": 10,
          "horse": "フェリチタ",
          "jockey": "松山弘平",
          "style": "先行",
          "speed": 95,
          "stamina": 93,
          "power": 94,
          "heavy": 95,
          "burst": 95,
          "odds": 5.5,
          "sire": "タワーオブロンドン",
      },
      {
          "num": 11,
          "horse": "ツキミ",
          "jockey": "川田将雅",
          "style": "先行",
          "speed": 93,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 94,
          "odds": 8.0,
          "sire": "ビッグアーサー",
      },
  ])


# 3. データベース：天皇賞（秋）（日曜・東京芝2000m・全17頭）
@st.cache_data
def get_tennosho_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "クロワデュノール",
          "jockey": "C.デムーロ",
          "style": "先行",
          "speed": 98,
          "stamina": 97,
          "power": 96,
          "heavy": 95,
          "burst": 98,
          "odds": 2.5,
          "sire": "キタサンブラック",
      },
      {
          "num": 2,
          "horse": "エルトンバローズ",
          "jockey": "松若風馬",
          "style": "先行",
          "speed": 92,
          "stamina": 92,
          "power": 91,
          "heavy": 90,
          "burst": 91,
          "odds": 65.0,
          "sire": "ディープブリランテ",
      },
      {
          "num": 3,
          "horse": "レガレイラ",
          "jockey": "戸崎圭太",
          "style": "差し",
          "speed": 97,
          "stamina": 98,
          "power": 95,
          "heavy": 96,
          "burst": 99,
          "odds": 4.2,
          "sire": "スワーヴリチャード",
      },
      {
          "num": 4,
          "horse": "レディネス",
          "jockey": "横山典弘",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 92,
          "heavy": 91,
          "burst": 92,
          "odds": 80.0,
          "sire": "ドゥラメンテ",
      },
      {
          "num": 5,
          "horse": "シャンパンカラー",
          "jockey": "内田博幸",
          "style": "差し",
          "speed": 93,
          "stamina": 92,
          "power": 93,
          "heavy": 94,
          "burst": 92,
          "odds": 90.0,
          "sire": "Reckless",
      },
      {
          "num": 6,
          "horse": "セイウンハーデス",
          "jockey": "幸英明",
          "style": "逃げ",
          "speed": 93,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 91,
          "odds": 50.0,
          "sire": "マンハッタンカフェ",
      },
      {
          "num": 7,
          "horse": "マスカレードボール",
          "jockey": "C.ルメール",
          "style": "差し",
          "speed": 97,
          "stamina": 96,
          "power": 95,
          "heavy": 94,
          "burst": 97,
          "odds": 5.0,
          "sire": "ドゥラメンテ",
      },
      {
          "num": 8,
          "horse": "ジュブロッサム",
          "jockey": "杉原誠人",
          "style": "先行",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 120.0,
          "sire": "クロフネ",
      },
      {
          "num": 9,
          "horse": "ホウオウビスケッツ",
          "jockey": "岩田康誠",
          "style": "逃げ",
          "speed": 94,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 91,
          "odds": 28.0,
          "sire": "マインドユアビスケッツ",
      },
      {
          "num": 10,
          "horse": "ネブラディスク",
          "jockey": "川田将雅",
          "style": "差し",
          "speed": 95,
          "stamina": 95,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 16.0,
          "sire": "American Post",
      },
      {
          "num": 11,
          "horse": "シェイクユアハート",
          "jockey": "吉村智洋",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 85.0,
          "sire": "Sri Pekan",
      },
      {
          "num": 12,
          "horse": "コスモキュランダ",
          "jockey": "M.デムーロ",
          "style": "差し",
          "speed": 94,
          "stamina": 95,
          "power": 95,
          "heavy": 96,
          "burst": 94,
          "odds": 22.0,
          "sire": "アルアイン",
      },
      {
          "num": 13,
          "horse": "リアライズシリウス",
          "jockey": "丹内祐次",
          "style": "先行",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 70.0,
          "sire": "Southern Image",
      },
      {
          "num": 14,
          "horse": "タガノデュード",
          "jockey": "津村明秀",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 95.0,
          "sire": "ステイゴールド",
      },
      {
          "num": 15,
          "horse": "サクラファレル",
          "jockey": "佐々木大輔",
          "style": "差し",
          "speed": 92,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 60.0,
          "sire": "ハーツクライ",
      },
      {
          "num": 16,
          "horse": "ジョバンニ",
          "jockey": "松山弘平",
          "style": "先行",
          "speed": 95,
          "stamina": 95,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 18.0,
          "sire": "エピファネイア",
      },
      {
          "num": 17,
          "horse": "ダノンデサイル",
          "jockey": "戸崎圭太",
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 96,
          "heavy": 95,
          "burst": 96,
          "odds": 8.0,
          "sire": "エピファネイア",
      },
  ])


# 共通HTMLアニメーションテンプレート（100回シミュレーション＆アニメーション搭載）
def get_sim_html(horses_data, race_config):
  return f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * {{ box-sizing: border-box; touch-action: manipulation; }}
        body {{ margin: 0; padding: 0; font-family: -apple-system, sans-serif; background-color: #080c14; color: white; }}
        .sim-container {{ width: 100%; max-width: 900px; margin: 0 auto; padding: 4px; text-align: center; }}
        .btn-group {{ display: flex; gap: 10px; margin-bottom: 12px; }}
        .start-btn {{
            flex: 1; height: 50px; background: linear-gradient(135deg, #059669, #047857); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(5,150,105,0.3);
        }
        .sim100-btn {{
            flex: 1; height: 50px; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,0.3);
        }
        .status-box {{ font-size: 15px; font-weight: bold; color: #34d399; min-height: 28px; margin-bottom: 8px; }}
        .svg-wrapper {{ 
            width: 100%; background: #06120d; border-radius: 14px; border: 2px solid #1e3a2f; padding: 10px; box-sizing: border-box; overflow: hidden;
        }
        .results-box {{ 
            margin-top: 14px; background: #111827; padding: 16px; border-radius: 12px; border: 1px solid #374151; text-align: left; max-height: 450px; overflow-y: auto;
        }
        .results-table-wrapper {{ width: 100%; overflow-x: auto; }}
        .results-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; min-width: 550px; }}
        .results-table th {{ 
            position: sticky; top: 0; background: #1f2937; padding: 10px; font-size: 13px; text-align: center; color: #9ca3af; border-bottom: 2px solid #374151; z-index: 10;
        }
        .results-table td {{ padding: 9px; font-size: 14px; text-align: center; border-bottom: 1px solid #1f2937; }}
        .waku-tag {{ display: inline-block; width: 24px; height: 24px; line-height: 24px; text-align: center; border-radius: 6px; font-weight: bold; font-size: 12px; margin-right: 6px; }}
        .rank-badge {{ font-weight: bold; font-size: 15px; }}
        .rank-1 {{ color: #f59e0b; }}
        .rank-2 {{ color: #94a3b8; }}
        .rank-3 {{ color: #d97706; }}
        .rate-tag {{ font-weight: bold; color: #f87171; font-size: 16px; }}
        .ticket-box {{ background: #030712; border: 1px solid #374151; padding: 12px 16px; border-radius: 10px; margin-top: 12px; font-size: 13px; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="sim-container">
        <div class="btn-group">
            <button id="startBtn" class="start-btn">▶ レース発走 (GATE OPEN)</button>
            <button id="sim100Btn" class="sim100-btn">⚡ 100回シミュレーション＆買い目</button>
        </div>
        
        <div id="statusBox" class="status-box">発走準備完了：ボタンを押してください</div>
        
        <div class="svg-wrapper">
            <svg id="trackSvg" viewBox="0 0 720 380" width="100%" height="auto" style="display: block;">
                <path d="M 220 70 L 500 70 A 110 110 0 0 1 500 290 L 220 290 A 110 110 0 0 1 220 70 Z" fill="#16382b" stroke="#22c55e" stroke-width="26"/>
                <path d="M 220 84 L 500 84 A 96 96 0 0 1 500 276 L 220 276 A 96 96 0 0 1 220 84 Z" fill="#080c14" stroke="#080c14" stroke-width="2"/>
                <g id="goalGroup"></g>
                <g id="startGroup"></g>
                <g id="horsesGroup"></g>
            </svg>
        </div>

        <div class="results-box">
            <div id="resultsTitle" style="font-weight: bold; color: #f59e0b; font-size: 16px;">🏆 リアルタイム着順結果</div>
            <div id="resultsContent" style="color: #94a3b8;">発走スタンバイOK</div>
        </div>
    </div>

    <script>
        const horsesData = {json.dumps(horses_data)};
        const raceConfig = {json.dumps(race_config)};
        let animId = null;

        function getWakuStyle(num, total) {
            let waku = Math.ceil((num / total) * 8);
            if (total <= 8) waku = num;
            const colors = [
                {{ bg: '#ffffff', text: '#000000' }}, {{ bg: '#333333', text: '#ffffff' }},
                {{ bg: '#ef4444', text: '#ffffff' }}, {{ bg: '#3b82f6', text: '#ffffff' }},
                {{ bg: '#eab308', text: '#000000' }}, {{ bg: '#22c55e', text: '#ffffff' }},
                {{ bg: '#f97316', text: '#ffffff' }}, {{ bg: '#a855f7', text: '#ffffff' }}
            ];
            return colors[Math.min(Math.max(waku - 1, 0), 7)];
        }

        const spec = {{ dir: -1, startP: 0.20, goalP: 1.20 }};

        function getTrackPoint(p, laneOffset = 0) {
            p = (p % 1.0 + 1.0) % 1.0;
            const r = 110 + laneOffset;
            const lenStr = 280;
            const circumference = 2 * Math.PI * r + 2 * lenStr;
            const distOnTrack = p * circumference;
            let x, y, angle;

            if (distOnTrack <= lenStr) {
                x = 500 - distOnTrack; y = 290 + laneOffset; angle = Math.PI;
            } else if (distOnTrack <= lenStr + Math.PI * r) {
                const arcLen = distOnTrack - lenStr;
                const theta = Math.PI / 2 + (arcLen / r);
                x = 220 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
            } else if (distOnTrack <= 2 * lenStr + Math.PI * r) {
                const strLen2 = distOnTrack - (lenStr + Math.PI * r);
                x = 220 + strLen2; y = 70 - laneOffset; angle = 0;
            } else {
                const arcLen2 = distOnTrack - (2 * lenStr + Math.PI * r);
                const theta = -Math.PI / 2 + (arcLen2 / r);
                x = 500 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
            }
            if (spec.dir === -1) {{ x = 720 - x; angle = Math.PI - angle; }}
            return {{ x, y, angle }};
        }

        function drawCourse() {{
            const goalPt = getTrackPoint(spec.goalP);
            document.getElementById('goalGroup').innerHTML = `
                <line x1="${{goalPt.x}}" y1="${{goalPt.y - 22}}" x2="${{goalPt.x}}" y2="${{goalPt.y + 22}}" stroke="#ef4444" stroke-width="5"/>
                <text x="${{goalPt.x}}" y="${{goalPt.y + 38}}" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
            `;
            const startPt = getTrackPoint(spec.startP);
            document.getElementById('startGroup').innerHTML = `
                <line x1="${{startPt.x}}" y1="${{startPt.y - 18}}" x2="${{startPt.x}}" y2="${{startPt.y + 18}}" stroke="#22c55e" stroke-width="4"/>
                <text x="${{startPt.x}}" y="${{startPt.y - 22}}" fill="#22c55e" font-size="12" font-weight="bold" text-anchor="middle">START 🚪</text>
            `;
        }}
        drawCourse();

        document.getElementById('startBtn').addEventListener('click', startSimulation);
        document.getElementById('sim100Btn').addEventListener('click', run100Simulations);

        function startSimulation() {{
            if (animId) cancelAnimationFrame(animId);
            const group = document.getElementById('horsesGroup');
            const status = document.getElementById('statusBox');
            const resultsTitle = document.getElementById('resultsTitle');
            const resultsContent = document.getElementById('resultsContent');
            
            group.innerHTML = '';
            resultsTitle.innerText = "🏆 リアルタイム着順結果";
            resultsContent.innerHTML = '<div style="padding:10px; color:#94a3b8;">⏱ ゲートが開きました！決戦スタート！</div>';

            const runners = horsesData.map((h, i) => {{
                const laneOffset = (i - (horsesData.length - 1) / 2) * 2.1;
                const wakuStyle = getWakuStyle(h.num, horsesData.length);
                const effectiveDrain = Math.max(0.65, raceConfig.drain);
                const conditionMod = 0.92 + Math.random() * 0.16;

                return {{
                    ...h, laneOffset, wakuStyle,
                    progress: spec.startP, targetProgress: spec.goalP,
                    effectiveDrain, conditionMod,
                    staminaRem: h.stamina * 10 / effectiveDrain,
                    spurtPoint: spec.startP + (0.55 + Math.random() * 0.10),
                    finished: false, rank: 0
                }};
            }});

            let finishedCount = 0;
            const totalHorses = runners.length;

            function animate() {{
                group.innerHTML = '';
                runners.forEach((h) => {{
                    if (!h.finished) {{
                        let baseSpeed = h.speed * h.conditionMod * 0.000036;
                        if (h.jockey_bonus > 1.2) baseSpeed *= 1.02;
                        if (h.pace_effect > 0) baseSpeed *= 1.06;

                        if (h.progress >= h.spurtPoint) {{
                            baseSpeed *= (h.style === "差し" || h.style === "追込") ? (1.25 + h.burst * 0.0025) : 1.10;
                        }}

                        h.staminaRem -= 0.04 * h.effectiveDrain;
                        if (h.staminaRem <= 0) baseSpeed *= 0.6;
                        h.progress += baseSpeed;

                        if (h.progress >= h.targetProgress) {{
                            h.progress = h.targetProgress;
                            h.finished = true;
                            finishedCount++;
                            h.rank = finishedCount;
                        }}
                    }}
                    const pt = getTrackPoint(h.progress, h.laneOffset);
                    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    g.setAttribute('transform', `translate(${{pt.x}}, ${{pt.y}})`);
                    g.innerHTML = `
                        <circle cx="0" cy="0" r="8" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                        <text x="0" y="3" font-size="10" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                        <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${{h.name}} (${{h.jockey}})</text>
                    `;
                    group.appendChild(g);
                }});

                if (finishedCount === 0) {{
                    status.innerText = `🏁 熱戦中！`;
                }} else if (finishedCount < totalHorses) {{
                    status.innerText = `🏁 ${{finishedCount}}頭ゴールイン！`;
                }} else {{
                    status.innerText = '🏆 全頭ゴール！';
                }}

                if (finishedCount < totalHorses) {{
                    animId = requestAnimationFrame(animate);
                }} else {{
                    runners.sort((a, b) => a.rank - b.rank);
                    let html = `<div class="results-table-wrapper"><table class="results-table"><thead><tr><th>着順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>脚質</th></tr></thead><tbody>`;
                    runners.forEach((h) => {{
                        const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                        html += `<tr><td class="rank-badge ${{rankClass}}">${{h.rank}}着</td><td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td><td style="text-align:left;"><strong>${{h.name}}</strong></td><td>${{h.jockey}}</td><td>${{h.style}}</td></tr>`;
                    }});
                    html += '</tbody></table></div>';
                    resultsContent.innerHTML = html;
                }}
            }}
            animId = requestAnimationFrame(animate);
        }}

        function run100Simulations() {{
            if (animId) cancelAnimationFrame(animId);
            const status = document.getElementById('statusBox');
            const resultsTitle = document.getElementById('resultsTitle');
            const resultsContent = document.getElementById('resultsContent');

            status.innerText = "⚡ 100回モンテカルロシミュレーション中...";
            resultsTitle.innerText = "📊 100回シミュレーション総合結果 ＆ 推奨買い目";

            const stats = {{}};
            horsesData.forEach(h => {{
                stats[h.name] = {{
                    num: h.num, name: h.name, jockey: h.jockey, style: h.style,
                    wakuStyle: getWakuStyle(h.num, horsesData.length),
                    first: 0, second: 0, third: 0, totalRank: 0
                }};
            }});

            const SIM_COUNT = 100;
            for (let sim = 0; sim < SIM_COUNT; sim++) {{
                let raceRes = horsesData.map(h => {{
                    const effectiveDrain = Math.max(0.65, raceConfig.drain);
                    const burstScore = h.burst / effectiveDrain;
                    const randomMod = (Math.random() - 0.5) * 6.5;
                    const score = (burstScore * 0.35) + (h.speed * 0.30) + (h.stamina * 0.20) + (h.power * 0.15) + h.jockey_bonus + h.gate_bonus + h.pace_effect + randomMod;
                    return {{ name: h.name, score: score }};
                }});
                raceRes.sort((a, b) => b.score - a.score);
                raceRes.forEach((item, index) => {{
                    stats[item.name].totalRank += (index + 1);
                    if (index === 0) stats[item.name].first++;
                    if (index === 1) stats[item.name].second++;
                    if (index === 2) stats[item.name].third++;
                }});
            }}

            const rankedList = Object.values(stats).map(s => {{
                const inTop3 = s.first + s.second + s.third;
                const inTop3Rate = (inTop3 / SIM_COUNT) * 100;
                const avgRank = (s.totalRank / SIM_COUNT).toFixed(2);
                return {{ ...s, inTop3, inTop3Rate, avgRank }};
            }}).sort((a, b) => {{
                if (b.inTop3Rate !== a.inTop3Rate) return b.inTop3Rate - a.inTop3Rate;
                return b.first - a.first;
            }});

            const top5 = rankedList.slice(0, 5);
            let html = `<div class="results-table-wrapper"><table class="results-table">
                <thead><tr><th>予想順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>1着</th><th>2着</th><th>3着</th><th>複勝率</th><th>平均着順</th></tr></thead><tbody>`;

            top5.forEach((h, idx) => {{
                const rankClass = idx === 0 ? 'rank-1' : idx === 1 ? 'rank-2' : idx === 2 ? 'rank-3' : '';
                html += `<tr>
                    <td class="rank-badge ${{rankClass}}">${{idx + 1}}位</td>
                    <td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td>
                    <td style="text-align:left;"><strong>${{h.name}}</strong></td>
                    <td>${{h.jockey}}</td>
                    <td>${{h.first}}回</td><td>${{h.second}}回</td><td>${{h.third}}回</td>
                    <td><span class="rate-tag">${{h.inTop3Rate.toFixed(0)}}%</span></td>
                    <td><strong>${{h.avgRank}}着</strong></td>
                </tr>`;
            }});
            html += '</tbody></table></div>';

            const t1 = top5[0].num;
            const t2 = top5[1].num;
            const t3 = top5[2].num;
            const t4 = top5[3].num;

            html += `<div class="ticket-box">
                <strong>🎯 AI自動構築買い目</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${{t1}} - (${{t2}}, ${{t3}}, ${{t4}})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${{t1}} － 相手 (${{t2}}, ${{t3}}, ${{t4}})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${{t1}}, ${{t2}} → 2着 ${{t1}}, ${{t2}}, ${{t3}} → 3着 ${{t1}}, ${{t2}}, ${{t3}}, ${{t4}}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ 100回シミュレーション＆買い目構築完了";
        }}
    </script>
</body>
</html>"""


# メインのレース選択タブ
main_tab1, main_tab2 = st.tabs(
    ["🌸 土曜：ファンタジーS (GIII)", "🍁 日曜：天皇賞（秋） (GI)"]
  )

# ==========================================
# 🌸 ファンタジーS タブ処理
# ==========================================
with main_tab1:
  df_all = get_fantasy_db()
  if "sel_fan" not in st.session_state:
    st.session_state.sel_fan = df_all["horse"].tolist()

  st.markdown(
      '<div class="section-title">⚡ ファンタジーS 最新全11頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  if st.button(
      "🌸 ファンタジーS (京都・芝1400m外) 全11頭一括セット",
      key="btn_fan",
      use_container_width=True,
  ):
    st.session_state.sel_fan = df_all["horse"].tolist()

  c1, c2 = st.columns(2)
  with c1:
    going_f = st.selectbox(
        "馬場状態 (ファンタジーS)", ["良", "稍重", "重", "不良"], key="g_fan"
    )
  with c2:
    pace_f = st.selectbox(
        "展開ペース (荒れ想定対応)",
        [
            "ハイペース (H - 荒れ想定)",
            "ミドルペース (M)",
            "スローペース (S)",
        ],
        key="p_fan",
    )

  selected_horses = st.multiselect(
      "出走馬選択 (ファンタジーS)",
      options=df_all["horse"].tolist(),
      default=st.session_state.sel_fan,
      key="ms_fan",
  )

  if len(selected_horses) >= 2:
    df_race = (
        df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
    )
    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}
    for idx, r in df_race.iterrows():
      with num_cols[idx % min(3, len(selected_horses))]:
        custom_numbers[r["horse"]] = st.number_input(
            f"{r['horse']} ({r['jockey']}) 馬番",
            1,
            24,
            int(r["num"]),
            key=f"num_f_{r['horse']}",
        )
    df_race["num"] = df_race["horse"].map(custom_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    drain_f = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going_f]
    top_j = ["川田将雅", "C.デムーロ", "池添謙一", "松山弘平", "北村友一"]
    df_race["jockey_bonus"] = df_race["jockey"].apply(
        lambda x: 4.5 if x in top_j else 1.5
    )
    df_race["gate_bonus"] = df_race["num"].apply(
        lambda n: 2.5 if n >= 8 else (2.0 if n <= 3 else 1.0)
    )
    df_race["pace_effect"] = (
        df_race["style"].apply(lambda s: 6.0 if s in ["差し", "追込"] else -6.0)
        if "ハイペース" in pace_f
        else (
            df_race["style"].apply(
                lambda s: 5.0 if s in ["先行", "自在"] else -3.0
            )
            if "スローペース" in pace_f
            else 0.0
        )
    )

    best_f = df_race.sort_values(
        by="speed", ascending=False
    ).iloc[0]  # 表示用
    st.success(
        f"🌸 **ファンタジーS 注目本命**: {best_f['num']}番"
        f" {best_f['horse']} ({best_f['jockey']})"
    )

    horses_js = df_race.to_dict(orient="records")
    race_cfg = {"drain": drain_f, "going": going_f, "pace": pace_f}
    st.components.v1.html(get_sim_html(horses_js, race_cfg), height=880)

# ==========================================
# 🍁 天皇賞（秋） タブ処理
# ==========================================
with main_tab2:
  df_all_t = get_tennosho_db()
  if "sel_ten" not in st.session_state:
    st.session_state.sel_ten = df_all_t["horse"].tolist()

  st.markdown(
      '<div class="section-title">⚡ 天皇賞（秋） 最新全17頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  if st.button(
      "🍁 天皇賞（秋） (東京・芝2000m) 全17頭一括セット",
      key="btn_ten",
      use_container_width=True,
  ):
    st.session_state.sel_ten = df_all_t["horse"].tolist()

  tc1, tc2 = st.columns(2)
  with tc1:
    going_t = st.selectbox(
        "馬場状態 (天皇賞秋)", ["良", "稍重", "重", "不良"], key="g_ten"
    )
  with tc2:
    pace_t = st.selectbox(
        "展開ペース指定 (天皇賞秋)",
        ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"],
        key="p_ten",
    )

  selected_horses_t = st.multiselect(
      "出走馬選択 (天皇賞秋)",
      options=df_all_t["horse"].tolist(),
      default=st.session_state.sel_ten,
      key="ms_ten",
  )

  if len(selected_horses_t) >= 2:
    df_race_t = (
        df_all_t[df_all_t["horse"].isin(selected_horses_t)]
        .copy()
        .reset_index(drop=True)
    )
    num_cols_t = st.columns(min(3, len(selected_horses_t)))
    custom_numbers_t = {}
    for idx, r in df_race_t.iterrows():
      with num_cols_t[idx % min(3, len(selected_horses_t))]:
        custom_numbers_t[r["horse"]] = st.number_input(
            f"{r['horse']} ({r['jockey']}) 馬番",
            1,
            24,
            int(r["num"]),
            key=f"num_t_{r['horse']}",
        )
    df_race_t["num"] = df_race_t["horse"].map(custom_numbers_t)
    df_race_t = df_race_t.sort_values(by="num").reset_index(drop=True)

    drain_t = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going_t]
    top_jt = ["C.ルメール", "C.デムーロ", "川田将雅", "戸崎圭太", "横山典弘"]
    df_race_t["jockey_bonus"] = df_race_t["jockey"].apply(
        lambda x: 5.0 if x in top_jt else 1.2
    )
    df_race_t["gate_bonus"] = df_race_t["num"].apply(
        lambda n: 3.0 if n <= 6 else (-3.0 if n >= 14 else 1.0)
    )
    df_race_t["pace_effect"] = (
        df_race_t["style"].apply(lambda s: 5.0 if s in ["差し", "追込"] else -5.0)
        if pace_t == "ハイペース (H)"
        else (
            df_race_t["style"].apply(
                lambda s: 5.0 if s in ["先行", "自在"] else -4.0
            )
            if pace_t == "スローペース (S)"
            else 0.0
        )
    )

    best_t = df_race_t.sort_values(by="speed", ascending=False).iloc[0]
    st.warning(
        f"🍁 **天皇賞（秋） 注目本命**: {best_t['num']}番"
        f" {best_t['horse']} ({best_t['jockey']})"
    )

    horses_js_t = df_race_t.to_dict(orient="records")
    race_cfg_t = {"drain": drain_t, "going": going_t, "pace": pace_t}
    st.components.v1.html(get_sim_html(horses_js_t, race_cfg_t), height=880)
