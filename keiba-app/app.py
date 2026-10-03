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

st.title("🏇 本格競馬シミュレーター")
st.caption("18頭対応 / 競馬場別坂道＆スタート位置 / 展開ダイナミクス完全対応版")

# 2. データベース（毎日王冠＋京都大賞典 競走馬データ）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠 出走馬 ---
        {"horse": "サトノシャイニング", "sire": "キズナ", "style": "先行", "stamina": 82, "speed": 89, "power": 84, "heavy": 88, "opt_dist": 1800},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "style": "先行", "stamina": 83, "speed": 87, "power": 86, "heavy": 95, "opt_dist": 1800},
        {"horse": "ホウオウビスケッツ", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 83, "speed": 88, "power": 87, "heavy": 92, "opt_dist": 1800},
        {"horse": "レイニング", "sire": "サートゥルナーリア", "style": "差し", "stamina": 82, "speed": 89, "power": 83, "heavy": 88, "opt_dist": 1800},
        {"horse": "リアライズシリウス", "sire": "ポアゾンブラック", "style": "先行", "stamina": 80, "speed": 89, "power": 82, "heavy": 90, "opt_dist": 1600},
        {"horse": "ダノンエアズロック", "sire": "モーリス", "style": "先行", "stamina": 83, "speed": 88, "power": 86, "heavy": 86, "opt_dist": 1800},
        {"horse": "シャンパンカラー", "sire": "ドゥラメンテ", "style": "追込", "stamina": 80, "speed": 90, "power": 88, "heavy": 94, "opt_dist": 1600},
        {"horse": "セイウンハーデス", "sire": "シルバーステート", "style": "逃げ", "stamina": 84, "speed": 85, "power": 86, "heavy": 90, "opt_dist": 1800},
        {"horse": "レディネス", "sire": "リアルスティール", "style": "先行", "stamina": 81, "speed": 84, "power": 82, "heavy": 85, "opt_dist": 1800},
        {"horse": "クルゼイロドスル", "sire": "ファインニードル", "style": "追込", "stamina": 78, "speed": 85, "power": 83, "heavy": 82, "opt_dist": 1600},
        {"horse": "ライヒスアドラー", "sire": "シスキン", "style": "差し", "stamina": 80, "speed": 88, "power": 81, "heavy": 86, "opt_dist": 1800},
        {"horse": "ロングラン", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 82, "speed": 83, "power": 85, "heavy": 92, "opt_dist": 1800},
        {"horse": "ビーアストニッシド", "sire": "アメリカンペイトリオット", "style": "逃げ", "stamina": 80, "speed": 84, "power": 85, "heavy": 88, "opt_dist": 1800},
        {"horse": "ドラゴンブースト", "sire": "ディーマジェスティ", "style": "差し", "stamina": 81, "speed": 85, "power": 83, "heavy": 87, "opt_dist": 1800},
        {"horse": "ランスオブカオス", "sire": "シルバーステート", "style": "差し", "stamina": 81, "speed": 86, "power": 84, "heavy": 86, "opt_dist": 1800},
        {"horse": "レガーロデルシエロ", "sire": "ロードカナロア", "style": "差し", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1600},
        {"horse": "アドマイヤクワッズ", "sire": "リアルスティール", "style": "差し", "stamina": 79, "speed": 88, "power": 81, "heavy": 85, "opt_dist": 1600},

        # --- 京都大賞典 出走馬 ---
        {"horse": "ヘデントール", "sire": "ルーラーシップ", "style": "差し", "stamina": 93, "speed": 88, "power": 87, "heavy": 102, "opt_dist": 2400},
        {"horse": "ディープモンスター", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 85, "power": 88, "heavy": 112, "opt_dist": 2400},
        {"horse": "アクアヴァーナル", "sire": "エピファネイア", "style": "差し", "stamina": 88, "speed": 86, "power": 84, "heavy": 98, "opt_dist": 2400},
        {"horse": "ダノンシーマ", "sire": "キタサンブラック", "style": "先行", "stamina": 89, "speed": 86, "power": 86, "heavy": 95, "opt_dist": 2400},
        {"horse": "ショウナンラプンタ", "sire": "キズナ", "style": "追込", "stamina": 89, "speed": 86, "power": 87, "heavy": 96, "opt_dist": 2400},
        {"horse": "ヴェルテンベルク", "sire": "キタサンブラック", "style": "追込", "stamina": 90, "speed": 81, "power": 85, "heavy": 100, "opt_dist": 2400},
        {"horse": "サヴォーナ", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 84, "power": 88, "heavy": 96, "opt_dist": 2400},
        {"horse": "リビアングラス", "sire": "キズナ", "style": "逃げ", "stamina": 89, "speed": 83, "power": 86, "heavy": 94, "opt_dist": 2400},
        {"horse": "ウエストナウ", "sire": "キズナ", "style": "先行", "stamina": 87, "speed": 84, "power": 85, "heavy": 92, "opt_dist": 2400},
        {"horse": "ヴェルミセル", "sire": "ゴールドシップ", "style": "追込", "stamina": 92, "speed": 78, "power": 86, "heavy": 110, "opt_dist": 2400},
        {"horse": "エコロディノス", "sire": "キタサンブラック", "style": "先行", "stamina": 86, "speed": 83, "power": 84, "heavy": 90, "opt_dist": 2200},
        {"horse": "キングスコール", "sire": "ドゥラメンテ", "style": "差し", "stamina": 88, "speed": 85, "power": 87, "heavy": 88, "opt_dist": 2400},
        {"horse": "サフィラ", "sire": "ハーツクライ", "style": "差し", "stamina": 86, "speed": 87, "power": 82, "heavy": 88, "opt_dist": 2200},
        {"horse": "ファミリータイム", "sire": "リアルスティール", "style": "差し", "stamina": 88, "speed": 82, "power": 85, "heavy": 90, "opt_dist": 2400},
        {"horse": "マイネルエンペラー", "sire": "ゴールドシップ", "style": "追込", "stamina": 91, "speed": 81, "power": 87, "heavy": 108, "opt_dist": 2400},
        {"horse": "ミクニインスパイア", "sire": "エピファネイア", "style": "差し", "stamina": 87, "speed": 85, "power": 84, "heavy": 92, "opt_dist": 2200},
        {"horse": "ミステリーウェイ", "sire": "ジャスタウェイ", "style": "先行", "stamina": 88, "speed": 82, "power": 86, "heavy": 95, "opt_dist": 2400},
        {"horse": "メイショウブレゲ", "sire": "ゴールドシップ", "style": "追込", "stamina": 95, "speed": 77, "power": 85, "heavy": 115, "opt_dist": 3000}
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 全馬データ"])

with tab_sim:
    st.subheader("⚙️️ レース条件設定")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        venue = st.selectbox("開催競馬場", ["東京", "中山", "京都", "阪神"])
    with col_c2:
        dist = st.selectbox("距離(m)", [1600, 1800, 2000, 2400])
    with col_c3:
        going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.markdown("---")
    st.subheader("🐎 出走馬選択（最大18頭）")
    
    btn_col1, btn_col2 = st.columns(2)
    
    main_default = df_all["horse"].tolist()[:18]
    
    if btn_col1.button("🎯 毎日王冠 出走馬セット（17頭）"):
        main_default = [h for h in df_all["horse"] if h in [
            "サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "レイニング", 
            "リアライズシリウス", "ダノンエアズロック", "シャンパンカラー", "セイウンハーデス",
            "レディネス", "クルゼイロドスル", "ライヒスアドラー", "ロングラン", "ビーアストニッシド",
            "ドラゴンブースト", "ランスオブカオス", "レガーロデルシエロ", "アドマイヤクワッズ"
        ]]
    if btn_col2.button("🏆 京都大賞典 出走馬セット（18頭）"):
        main_default = [h for h in df_all["horse"] if h in [
            "ヘデントール", "ディープモンスター", "アクアヴァーナル", "ダノンシーマ", 
            "ショウナンラプンタ", "ヴェルテンベルク", "サヴォーナ", "リビアングラス",
            "ウエストナウ", "ヴェルミセル", "エコロディノス", "キングスコール", "サフィラ",
            "ファミリータイム", "マイネルエンペラー", "ミクニインスパイア", "ミステリーウェイ", "メイショウブレゲ"
        ]]

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
            df_race[["num", "horse", "style", "opt_dist", "sire"]]
            .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "opt_dist": "適性距離", "sire": "父"}),
            hide_index=True,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🏁 完全コース再現＆ランダム波乱シミュレーション")

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
                    height: 50px;
                    background: linear-gradient(135deg, #ff4b4b, #d32f2f);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-bottom: 10px;
                }}
                .status-box {{ font-size: 15px; font-weight: bold; color: #3498db; min-height: 24px; margin-bottom: 6px; }}
                .svg-wrapper {{ width: 100%; background: #05140e; border-radius: 12px; border: 2px solid #1e3d30; }}
                .results-box {{ margin-top: 10px; background: #161b22; padding: 10px; border-radius: 8px; text-align: left; }}
                .results-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 6px; margin-top: 6px; }}
                .rank-card {{ background: #21262d; padding: 6px 8px; border-radius: 6px; font-size: 12px; display: flex; align-items: center; justify-content: space-between; }}
                .waku-tag {{ padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; margin-right: 4px; }}
            </style>
        </head>
        <body>
            <div class="sim-container">
                <button id="startBtn" class="start-btn">▶ レース発走！</button>
                <div id="statusBox" class="status-box">「レース発走」を押してください</div>
                
                <div class="svg-wrapper">
                    <svg id="trackSvg" viewBox="0 0 600 320" width="100%">
                        <!-- コース描画 -->
                        <ellipse cx="300" cy="160" rx="240" ry="120" fill="#1b4d3e" stroke="#2e8b57" stroke-width="12"/>
                        <ellipse cx="300" cy="160" rx="140" ry="50" fill="#0e1117" stroke="#2e8b57" stroke-width="6"/>
                        
                        <!-- 坂道区間（ビジュアル表示） -->
                        <path id="slopePath" d="" fill="none" stroke="rgba(230,126,34,0.6)" stroke-width="14" stroke-dasharray="6,4"/>

                        <!-- ゴールライン -->
                        <g id="goalGroup"></g>
                        <!-- スタートライン -->
                        <g id="startGroup"></g>

                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 15px;">🏆 入線結果（全頭確定）</div>
                    <div id="resultsList" class="results-grid">スタート待ち...</div>
                </div>
            </div>

            <script>
                const horsesData = {json.dumps(horses_js)};
                const raceConfig = {json.dumps(race_config_js)};
                let animId = null;

                // 枠色定義（JRA基準）
                function getWakuStyle(num, total) {{
                    let waku = 1;
                    if (total <= 8) waku = num;
                    else waku = Math.ceil((num / total) * 8);
                    
                    const colors = [
                        {{ bg: '#ffffff', text: '#000000' }}, // 1枠: 白
                        {{ bg: '#222222', text: '#ffffff' }}, // 2枠: 黒
                        {{ bg: '#e74c3c', text: '#ffffff' }}, // 3枠: 赤
                        {{ bg: '#3498db', text: '#ffffff' }}, // 4枠: 青
                        {{ bg: '#f1c40f', text: '#000000' }}, // 5枠: 黄
                        {{ bg: '#2ecc71', text: '#ffffff' }}, // 6枠: 緑
                        {{ bg: '#e67e22', text: '#ffffff' }}, // 7枠: 橙
                        {{ bg: '#9b59b6', text: '#ffffff' }}  // 8枠: 桃
                    ];
                    return colors[Math.min(Math.max(waku - 1, 0), 7)];
                }}

                // 競馬場別の坂道・周回方向設定
                const TRACK_SPECS = {{
                    "東京": {{ dir: -1, slopeStart: 0.15, slopeEnd: 0.35, slopeType: "up", finishAngle: Math.PI / 2 }}, // 左回り
                    "中山": {{ dir: 1, slopeStart: 0.82, slopeEnd: 0.98, slopeType: "up", finishAngle: -Math.PI / 2 }}, // 右回り
                    "京都": {{ dir: 1, slopeStart: 0.35, slopeEnd: 0.55, slopeType: "down", finishAngle: -Math.PI / 2 }}, // 右回り・下り坂
                    "阪神": {{ dir: 1, slopeStart: 0.80, slopeEnd: 0.95, slopeType: "up", finishAngle: -Math.PI / 2 }}  // 右回り
                }};

                const spec = TRACK_SPECS[raceConfig.venue] || TRACK_SPECS["東京"];

                // 距離によるスタート位置ズレ
                const lapRatio = raceConfig.dist / 2000.0;
                const startOffset = (1.0 - (lapRatio % 1.0)) % 1.0;

                // スタート・ゴール位置の描画
                function drawLines() {{
                    const goalGroup = document.getElementById('goalGroup');
                    const startGroup = document.getElementById('startGroup');

                    // ゴール位置
                    const gAng = spec.finishAngle;
                    const gx1 = 300 + 140 * Math.cos(gAng);
                    const gy1 = 160 + 50 * Math.sin(gAng);
                    const gx2 = 300 + 240 * Math.cos(gAng);
                    const gy2 = 160 + 120 * Math.sin(gAng);

                    goalGroup.innerHTML = `
                        <line x1="${{gx1}}" y1="${{gy1}}" x2="${{gx2}}" y2="${{gy2}}" stroke="#ff4b4b" stroke-width="4" stroke-dasharray="4"/>
                        <text x="${{gx2}}" y="${{gy2 + 15}}" fill="#ff4b4b" font-size="11" font-weight="bold" text-anchor="middle">GOAL</text>
                    `;

                    // スタート位置
                    const sAng = spec.finishAngle + (startOffset * Math.PI * 2 * spec.dir);
                    const sx1 = 300 + 140 * Math.cos(sAng);
                    const sy1 = 160 + 50 * Math.sin(sAng);
                    const sx2 = 300 + 240 * Math.cos(sAng);
                    const sy2 = 160 + 120 * Math.sin(sAng);

                    startGroup.innerHTML = `
                        <line x1="${{sx1}}" y1="${{sy1}}" x2="${{sx2}}" y2="${{sy2}}" stroke="#2ecc71" stroke-width="3"/>
                        <text x="${{sx2}}" y="${{sy2 - 8}}" fill="#2ecc71" font-size="10" font-weight="bold" text-anchor="middle">START</text>
                    `;
                }}
                drawLines();

                document.getElementById('startBtn').addEventListener('click', startSimulation);

                function startSimulation() {{
                    if (animId) cancelAnimationFrame(animId);

                    const group = document.getElementById('horsesGroup');
                    const status = document.getElementById('statusBox');
                    const resultsList = document.getElementById('resultsList');
                    
                    group.innerHTML = '';
                    resultsList.innerHTML = '⏱ レース展開中...';

                    // 当日の気まぐれ・スパートタイミングのランダム生成（着順の固定化防止）
                    const runners = horsesData.map((h, i) => {{
                        const laneOffset = (i - (horsesData.length - 1) / 2) * 3.5;
                        const wakuStyle = getWakuStyle(h.num, horsesData.length);

                        // 能力ブレ
                        const conditionMod = 0.92 + Math.random() * 0.16; 
                        const spurtPoint = 0.60 + Math.random() * 0.20;

                        return {{
                            ...h,
                            laneOffset: laneOffset,
                            wakuStyle: wakuStyle,
                            progress: startOffset,
                            staminaRem: h.stamina * 10,
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
                                // スピード計算
                                let curSpeed = h.speed * h.conditionMod * 0.00008;

                                // 脚質スパート
                                if (h.progress > h.spurtPoint) {{
                                    if (h.style === "差し" || h.style === "追込") curSpeed *= 1.25;
                                    else curSpeed *= 1.10;
                                }}

                                // 坂道判定
                                const pNormalized = (h.progress % 1.0);
                                if (pNormalized >= spec.slopeStart && pNormalized <= spec.slopeEnd) {{
                                    if (spec.slopeType === "up") {{
                                        curSpeed *= 0.85; // 上り坂で減速
                                    }} else {{
                                        curSpeed *= 1.10; // 下り坂で加速
                                    }}
                                }}

                                // スタミナ切れ
                                h.staminaRem -= 0.05;
                                if (h.staminaRem <= 0) curSpeed *= 0.7;

                                h.progress += curSpeed;

                                if (h.progress >= startOffset + 1.0) {{
                                    h.finished = true;
                                    finishedCount++;
                                    h.rank = finishedCount;
                                }}
                            }}

                            // 楕円極座標補間
                            const angle = spec.finishAngle + (h.progress * Math.PI * 2 * spec.dir);
                            const rx = 190 + h.laneOffset;
                            const ry = 85 + h.laneOffset * 0.4;

                            const x = 300 + rx * Math.cos(angle);
                            const y = 160 + ry * Math.sin(angle);

                            // 馬描画
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
                            status.innerText = "🏁 坂を越え、直線へ向かって各馬スパート！";
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = `🏁 ${{finishedCount}}頭ゴール！続々入線！`;
                        }} else {{
                            status.innerText = "🏆 全頭ゴールイン！着順確定！";
                        }}

                        if (finishedCount < totalHorses) {{
                            animId = requestAnimationFrame(animate);
                        }} else {{
                            runners.sort((a, b) => a.rank - b.rank);
                            resultsList.innerHTML = '';
                            runners.forEach((h) => {{
                                const rankText = h.rank === 1 ? '🥇 1着' : h.rank === 2 ? '🥈 2着' : h.rank === 3 ? '🥉 3着' : `${{h.rank}}着`;
                                resultsList.innerHTML += `
                                    <div class="rank-card">
                                        <div>
                                            <span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span>
                                            <strong>${{h.name}}</strong>
                                        </div>
                                        <div style="color:#f1c40f; font-weight:bold;">${{rankText}}</div>
                                    </div>
                                `;
                            }});
                        }}
                    }}

                    animId = requestAnimationFrame(animate);
                }}
            </script>
        </body>
        </html>
        """
        st.components.v1.html(html_code, height=540)

with tab_db:
    st.subheader("🔍 馬データ一覧")
    st.dataframe(df_all, use_container_width=True, hide_index=True)
