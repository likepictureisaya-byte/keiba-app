import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定
st.set_page_config(
    page_title="本格競馬シミュレーター",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stMultiSelect, .stSelectbox, .stButton, input, select {
        touch-action: manipulation !important;
        pointer-events: auto !important;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            height: 48px;
            font-size: 16px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🏇 本格競馬シミュレーター Pro")
st.caption("有名馬・重賞馬多数収録 / コース別スタート・ゴール完全対応 / 戦績データ表示")

# 2. データベース（G1馬・重賞馬・毎日王冠・京都大賞典 競走馬データ＋戦績）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- スターホース・G1馬 ---
        {"horse": "イクイノックス", "sire": "キタサンブラック", "style": "先行", "stamina": 98, "speed": 99, "power": 96, "heavy": 95, "opt_dist": 2000, "wins": "8-2-1-0"},
        {"horse": "ドウデュース", "sire": "ハーツクライ", "style": "追込", "stamina": 95, "speed": 98, "power": 97, "heavy": 92, "opt_dist": 2400, "wins": "6-1-1-6"},
        {"horse": "リバティアイランド", "sire": "ドゥラメンテ", "style": "差し", "stamina": 94, "speed": 98, "power": 93, "heavy": 90, "opt_dist": 2000, "wins": "5-2-1-1"},
        {"horse": "ジャスティンパレス", "sire": "ディープインパクト", "style": "差し", "stamina": 96, "speed": 93, "power": 92, "heavy": 88, "opt_dist": 2400, "wins": "5-2-2-7"},
        {"horse": "タイトルホルダー", "sire": "ドゥラメンテ", "style": "逃げ", "stamina": 99, "speed": 91, "power": 96, "heavy": 98, "opt_dist": 2500, "wins": "7-1-2-9"},
        {"horse": "ソダシ", "sire": "クロフネ", "style": "先行", "stamina": 88, "speed": 95, "power": 90, "heavy": 85, "opt_dist": 1600, "wins": "7-1-2-6"},
        {"horse": "ソングライン", "sire": "キズナ", "style": "差し", "stamina": 86, "speed": 97, "power": 89, "heavy": 88, "opt_dist": 1600, "wins": "7-2-1-6"},
        {"horse": "シュネルマイスター", "sire": "Kingman", "style": "差し", "stamina": 85, "speed": 96, "power": 88, "heavy": 86, "opt_dist": 1600, "wins": "5-3-3-6"},

        # --- 毎日王冠 出走馬 ---
        {"horse": "サトノシャイニング", "sire": "キズナ", "style": "先行", "stamina": 82, "speed": 89, "power": 84, "heavy": 88, "opt_dist": 1800, "wins": "2-1-0-1"},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "style": "先行", "stamina": 83, "speed": 87, "power": 86, "heavy": 95, "opt_dist": 1800, "wins": "4-1-2-5"},
        {"horse": "ホウオウビスケッツ", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 83, "speed": 88, "power": 87, "heavy": 92, "opt_dist": 1800, "wins": "4-2-1-6"},
        {"horse": "レイニング", "sire": "サートゥルナーリア", "style": "差し", "stamina": 82, "speed": 89, "power": 83, "heavy": 88, "opt_dist": 1800, "wins": "3-1-0-2"},
        {"horse": "ダノンエアズロック", "sire": "モーリス", "style": "先行", "stamina": 83, "speed": 88, "power": 86, "heavy": 86, "opt_dist": 1800, "wins": "3-0-0-3"},
        {"horse": "シャンパンカラー", "sire": "ドゥラメンテ", "style": "追込", "stamina": 80, "speed": 90, "power": 88, "heavy": 94, "opt_dist": 1600, "wins": "3-0-1-5"},
        {"horse": "セイウンハーデス", "sire": "シルバーステート", "style": "逃げ", "stamina": 84, "speed": 85, "power": 86, "heavy": 90, "opt_dist": 1800, "wins": "3-2-1-5"},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "style": "差し", "stamina": 89, "speed": 92, "power": 90, "heavy": 91, "opt_dist": 2000, "wins": "6-2-1-4"},

        # --- 京都大賞典 出走馬 ---
        {"horse": "ヘデントール", "sire": "ルーラーシップ", "style": "差し", "stamina": 93, "speed": 88, "power": 87, "heavy": 102, "opt_dist": 2400, "wins": "4-2-0-1"},
        {"horse": "ディープモンスター", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 85, "power": 88, "heavy": 112, "opt_dist": 2400, "wins": "5-3-2-9"},
        {"horse": "プラダリア", "sire": "ディープインパクト", "style": "先行", "stamina": 92, "speed": 87, "power": 89, "heavy": 96, "opt_dist": 2400, "wins": "4-2-3-8"},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "style": "差し", "stamina": 96, "speed": 91, "power": 94, "heavy": 105, "opt_dist": 2400, "wins": "6-4-3-6"},
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "style": "先行", "stamina": 92, "speed": 88, "power": 90, "heavy": 95, "opt_dist": 2400, "wins": "7-10-5-8"},
        {"horse": "サヴォーナ", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 84, "power": 88, "heavy": 96, "opt_dist": 2400, "wins": "3-5-2-7"},
        {"horse": "シュヴァリエローズ", "sire": "ディープインパクト", "style": "差し", "stamina": 88, "speed": 86, "power": 85, "heavy": 90, "opt_dist": 2200, "wins": "4-4-3-12"}
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "📊 全馬データ・戦績一覧"])

with tab_sim:
    st.subheader("⚙ レース条件設定")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        venue = st.selectbox("開催競馬場", ["東京", "中山", "京都", "阪神"])
    with col_c2:
        dist = st.selectbox("距離(m)", [1600, 1800, 2000, 2400, 2500])
    with col_c3:
        going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.markdown("---")
    st.subheader("🐎 出走馬選択（最大18頭）")
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    main_default = ["イクイノックス", "ドウデュース", "リバティアイランド", "ジャスティンパレス", "タイトルホルダー", "ソダシ", "ヘデントール", "ホウオウビスケッツ"]
    
    if btn_col1.button("🌟 オールスターG1対決（8頭）"):
        main_default = ["イクイノックス", "ドウデュース", "リバティアイランド", "ジャスティンパレス", "タイトルホルダー", "ソダシ", "ソングライン", "シュネルマイスター"]
    if btn_col2.button("🎯 毎日王冠 注目馬セット"):
        main_default = ["サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "レイニング", "ダノンエアズロック", "シャンパンカラー", "セイウンハーデス", "ローシャムパーク"]
    if btn_col3.button("🏆 京都大賞典 注目馬セット"):
        main_default = ["ヘデントール", "ディープモンスター", "プラダリア", "ブローザホーン", "ボッケリーニ", "サヴォーナ", "シュヴァリエローズ"]

    selected_horses = st.multiselect(
        "出走馬を選択（2〜18頭）",
        options=df_all["horse"].tolist(),
        default=main_default
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ 出走馬を【2頭以上】選択してください。")
    else:
        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        if len(df_race) > 18:
            df_race = df_race.head(18)
        
        df_race["num"] = [i + 1 for i in range(len(df_race))]

        st.dataframe(
            df_race[["num", "horse", "style", "opt_dist", "wins", "sire"]]
            .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "opt_dist": "適性距離", "wins": "戦績(1-2-3-着外)", "sire": "父"}),
            hide_index=True,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🏁 レース実況＆シミュレーション")

        horses_js = []
        for idx, r in df_race.iterrows():
            horses_js.append({
                "num": int(r["num"]),
                "name": str(r["horse"]),
                "style": str(r["style"]),
                "speed": float(r["speed"]),
                "stamina": float(r["stamina"]),
                "power": float(r["power"]),
                "heavy": float(r["heavy"]),
                "opt_dist": float(r["opt_dist"]),
            })

        race_config_js = {"venue": venue, "dist": dist, "going": going}

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                * {{ box-sizing: border-box; touch-action: manipulation; }}
                body {{ margin: 0; padding: 0; font-family: -apple-system, sans-serif; background-color: #0e1117; color: white; }}
                .sim-container {{ width: 100%; max-width: 800px; margin: 0 auto; padding: 5px; text-align: center; }}
                .start-btn {{
                    width: 100%;
                    height: 52px;
                    background: linear-gradient(135deg, #27ae60, #1e824c);
                    color: white;
                    border: none;
                    border-radius: 26px;
                    font-size: 19px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-bottom: 12px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }}
                .status-box {{ font-size: 16px; font-weight: bold; color: #2ecc71; min-height: 28px; margin-bottom: 8px; }}
                .svg-wrapper {{ width: 100%; background: #05140e; border-radius: 12px; border: 2px solid #1e3d30; padding: 6px; }}
                .results-box {{ margin-top: 14px; background: #161b22; padding: 14px; border-radius: 10px; border: 1px solid #30363d; text-align: left; }}
                .results-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
                .results-table th {{ background: #21262d; padding: 8px; font-size: 13px; text-align: left; color: #8b949e; border-bottom: 1px solid #30363d; }}
                .results-table td {{ padding: 8px; font-size: 14px; border-bottom: 1px solid #21262d; }}
                .waku-tag {{ display: inline-block; width: 22px; height: 22px; line-height: 22px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 6px; }}
                .rank-badge {{ font-weight: bold; font-size: 15px; }}
                .rank-1 {{ color: #f1c40f; }}
                .rank-2 {{ color: #bdc3c7; }}
                .rank-3 {{ color: #e67e22; }}
            </style>
        </head>
        <body>
            <div class="sim-container">
                <button id="startBtn" class="start-btn">▶ レース発走（GATE OPEN）</button>
                <div id="statusBox" class="status-box">「レース発走」を押してください</div>
                
                <div class="svg-wrapper">
                    <svg id="trackSvg" viewBox="0 0 600 320" width="100%">
                        <!-- コース描画 -->
                        <ellipse cx="300" cy="160" rx="240" ry="120" fill="#1b4d3e" stroke="#2e8b57" stroke-width="12"/>
                        <ellipse cx="300" cy="160" rx="140" ry="50" fill="#0e1117" stroke="#2e8b57" stroke-width="6"/>

                        <!-- ゴールライン（手前中央・下部固定） -->
                        <g id="goalGroup"></g>
                        <!-- スタートライン（距離応じて変化） -->
                        <g id="startGroup"></g>

                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 16px;">🏆 確定着順一覧</div>
                    <div id="resultsContent">スタート待ち...</div>
                </div>
            </div>

            <script>
                const horsesData = {json.dumps(horses_js)};
                const raceConfig = {json.dumps(race_config_js)};
                let animId = null;

                function getWakuStyle(num, total) {{
                    let waku = 1;
                    if (total <= 8) waku = num;
                    else waku = Math.ceil((num / total) * 8);
                    
                    const colors = [
                        {{ bg: '#ffffff', text: '#000000' }},
                        {{ bg: '#222222', text: '#ffffff' }},
                        {{ bg: '#e74c3c', text: '#ffffff' }},
                        {{ bg: '#3498db', text: '#ffffff' }},
                        {{ bg: '#f1c40f', text: '#000000' }},
                        {{ bg: '#2ecc71', text: '#ffffff' }},
                        {{ bg: '#e67e22', text: '#ffffff' }},
                        {{ bg: '#9b59b6', text: '#ffffff' }}
                    ];
                    return colors[Math.min(Math.max(waku - 1, 0), 7)];
                }}

                const TRACK_SPECS = {{
                    "東京": {{ dir: -1, slopeStart: 0.20, slopeEnd: 0.40, slopeType: "up" }}, // 左回り
                    "中山": {{ dir: 1, slopeStart: 0.75, slopeEnd: 0.95, slopeType: "up" }},  // 右回り
                    "京都": {{ dir: 1, slopeStart: 0.30, slopeEnd: 0.50, slopeType: "down" }},// 右回り
                    "阪神": {{ dir: 1, slopeStart: 0.75, slopeEnd: 0.95, slopeType: "up" }}   // 右回り
                }};

                const spec = TRACK_SPECS[raceConfig.venue] || TRACK_SPECS["東京"];

                // ゴール位置は手前中央（角度: Math.PI / 2）
                const FINISH_ANGLE = Math.PI / 2;

                // 距離に応じたスタート位置の計算（1周2000m換算）
                const lapRatio = raceConfig.dist / 2000.0;
                // スタートからゴールまでのトータル進行周回数
                const startOffset = (1.0 - (lapRatio % 1.0)) % 1.0;

                function drawLines() {{
                    const goalGroup = document.getElementById('goalGroup');
                    const startGroup = document.getElementById('startGroup');

                    // ゴール描画（手前直線）
                    const gx1 = 300; const gy1 = 210;
                    const gx2 = 300; const gy2 = 280;

                    goalGroup.innerHTML = `
                        <line x1="${{gx1}}" y1="${{gy1}}" x2="${{gx2}}" y2="${{gy2}}" stroke="#ff4b4b" stroke-width="4" stroke-dasharray="4"/>
                        <text x="${{gx1}}" y="${{gy2 + 15}}" fill="#ff4b4b" font-size="12" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
                    `;

                    // スタート描画
                    const sAng = FINISH_ANGLE - (startOffset * Math.PI * 2 * spec.dir);
                    const sx1 = 300 + 140 * Math.cos(sAng);
                    const sy1 = 160 + 50 * Math.sin(sAng);
                    const sx2 = 300 + 240 * Math.cos(sAng);
                    const sy2 = 160 + 120 * Math.sin(sAng);

                    startGroup.innerHTML = `
                        <line x1="${{sx1}}" y1="${{sy1}}" x2="${{sx2}}" y2="${{sy2}}" stroke="#2ecc71" stroke-width="3"/>
                        <text x="${{sx2}}" y="${{sy2 - 8}}" fill="#2ecc71" font-size="11" font-weight="bold" text-anchor="middle">START</text>
                    `;
                }}
                drawLines();

                document.getElementById('startBtn').addEventListener('click', startSimulation);

                function startSimulation() {{
                    if (animId) cancelAnimationFrame(animId);

                    const group = document.getElementById('horsesGroup');
                    const status = document.getElementById('statusBox');
                    const resultsContent = document.getElementById('resultsContent');
                    
                    group.innerHTML = '';
                    resultsContent.innerHTML = '<div style="padding:10px; color:#8b949e;">⏱ レース進行中... 各馬が一斉にスタートしました！</div>';

                    // 距離適性ペナルティ計算
                    const runners = horsesData.map((h, i) => {{
                        const laneOffset = (i - (horsesData.length - 1) / 2) * 3.5;
                        const wakuStyle = getWakuStyle(h.num, horsesData.length);

                        // 距離ズレによるスタミナペナルティ
                        const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                        const distPenalty = Math.max(0, (distDiff - 200) * 0.05);

                        const conditionMod = 0.94 + Math.random() * 0.12; 
                        const spurtPoint = startOffset + (lapRatio * (0.65 + Math.random() * 0.15));

                        return {{
                            ...h,
                            laneOffset: laneOffset,
                            wakuStyle: wakuStyle,
                            progress: startOffset,
                            targetProgress: startOffset + lapRatio,
                            staminaRem: (h.stamina - distPenalty) * 12,
                            conditionMod: conditionMod,
                            spurtPoint: spurtPoint,
                            finished: false,
                            rank: 0
                        }};
                    }});

                    let finishedCount = 0;
                    const totalHorses = runners.length;

                    function animate() {{
                        group.innerHTML = '';

                        runners.forEach((h) => {{
                            if (!h.finished) {{
                                // スピード（じっくり観戦できるよう減速調整）
                                let curSpeed = h.speed * h.conditionMod * 0.000038;

                                // 脚質スパート
                                if (h.progress >= h.spurtPoint) {{
                                    if (h.style === "差し" || h.style === "追込") curSpeed *= 1.28;
                                    else curSpeed *= 1.12;
                                }}

                                // 坂道効果
                                const pNormalized = (h.progress % 1.0);
                                if (pNormalized >= spec.slopeStart && pNormalized <= spec.slopeEnd) {{
                                    if (spec.slopeType === "up") curSpeed *= 0.88;
                                    else curSpeed *= 1.08;
                                }}

                                // スタミナ減衰
                                h.staminaRem -= 0.04;
                                if (h.staminaRem <= 0) curSpeed *= 0.65;

                                h.progress += curSpeed;

                                if (h.progress >= h.targetProgress) {{
                                    h.finished = true;
                                    finishedCount++;
                                    h.rank = finishedCount;
                                }}
                            }}

                            // 楕円上の位置計算
                            const angle = FINISH_ANGLE + ((h.progress - (startOffset + lapRatio)) * Math.PI * 2 * spec.dir);
                            const rx = 190 + h.laneOffset;
                            const ry = 85 + h.laneOffset * 0.4;

                            const x = 300 + rx * Math.cos(angle);
                            const y = 160 + ry * Math.sin(angle);

                            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                            g.setAttribute('transform', `translate(${{x}}, ${{y}})`);
                            g.innerHTML = `
                                <circle cx="0" cy="0" r="8" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="0" y="3" font-size="9" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                                <text x="11" y="3" font-size="9" font-weight="bold" fill="white">${{h.name}}</text>
                            `;
                            group.appendChild(g);
                        }});

                        if (finishedCount === 0) {{
                            status.innerText = "🏇 各馬第4コーナーをまわって直線コースへ！";
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = `🏁 ${{finishedCount}}頭ゴールイン！激しい着順争い！`;
                        }} else {{
                            status.innerText = "🏆 全馬ゴールイン！着順が確定しました！";
                        }}

                        if (finishedCount < totalHorses) {{
                            animId = requestAnimationFrame(animate);
                        }} else {{
                            runners.sort((a, b) => a.rank - b.rank);
                            
                            let html = `
                                <table class="results-table">
                                    <thead>
                                        <tr>
                                            <th>着順</th>
                                            <th>馬番</th>
                                            <th>馬名</th>
                                            <th>脚質</th>
                                            <th>適性距離</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                            `;

                            runners.forEach((h) => {{
                                const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                                html += `
                                    <tr>
                                        <td class="rank-badge ${{rankClass}}">${{h.rank}}着</td>
                                        <td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td>
                                        <td><strong>${{h.name}}</strong></td>
                                        <td>${{h.style}}</td>
                                        <td>${{h.opt_dist}}m</td>
                                    </tr>
                                `;
                            }});
                            html += '</tbody></table>';
                            resultsContent.innerHTML = html;
                        }}
                    }}

                    animId = requestAnimationFrame(animate);
                }}
            </script>
        </body>
        </html>
        """
        st.components.v1.html(html_code, height=580)

with tab_db:
    st.subheader("📊 登録馬一覧＆過去戦績データ")
    
    # 勝率・連対率の計算関数
    def calc_stats(wins_str):
        try:
            parts = [int(x) for x in wins_str.split("-")]
            total = sum(parts)
            if total == 0: return "0%", "0%"
            win_rate = f"{(parts[0] / total * 100):.1f}%"
            top2_rate = f"{((parts[0] + parts[1]) / total * 100):.1f}%"
            return win_rate, top2_rate
        except:
            return "N/A", "N/A"

    df_display = df_all.copy()
    stats = df_display["wins"].apply(calc_stats)
    df_display["勝率"] = [s[0] for s in stats]
    df_display["連対率(2着以内)"] = [s[1] for s in stats]

    st.dataframe(
        df_display[["horse", "style", "opt_dist", "wins", "勝率", "連対率(2着以内)", "speed", "stamina", "power", "sire"]]
        .rename(columns={
            "horse": "馬名", "style": "脚質", "opt_dist": "適性距離",
            "wins": "戦績(1着-2着-3着-着外)", "speed": "スピード",
            "stamina": "スタミナ", "power": "パワー", "sire": "父"
        }),
        use_container_width=True,
        hide_index=True
    )
