import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定
st.set_page_config(
    page_title="JRAリアルコース競馬シミュレーター",
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

st.title("🏇 JRAリアルコース競馬シミュレーター")
st.caption("最新全出走馬完全収録 / 競馬場別スタート・ゴール・坂道・周回方向忠実再現")

# 2. データベース（最新の毎日王冠＋京都大賞典 現役全出走馬データ）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠（全17頭） ---
        {"horse": "サトノシャイニング", "race_type": "毎日王冠", "sire": "キズナ", "style": "先行", "stamina": 82, "speed": 89, "power": 84, "heavy": 88, "opt_dist": 1800, "wins": "2-1-0-1"},
        {"horse": "エルトンバローズ", "race_type": "毎日王冠", "sire": "ディープブリランテ", "style": "先行", "stamina": 83, "speed": 87, "power": 86, "heavy": 95, "opt_dist": 1800, "wins": "4-1-2-5"},
        {"horse": "ホウオウビスケッツ", "race_type": "毎日王冠", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 83, "speed": 88, "power": 87, "heavy": 92, "opt_dist": 1800, "wins": "4-2-1-6"},
        {"horse": "レイニング", "race_type": "毎日王冠", "sire": "サートゥルナーリア", "style": "差し", "stamina": 82, "speed": 89, "power": 83, "heavy": 88, "opt_dist": 1800, "wins": "3-1-0-2"},
        {"horse": "リアライズシリウス", "race_type": "毎日王冠", "sire": "ポアゾンブラック", "style": "先行", "stamina": 80, "speed": 89, "power": 82, "heavy": 90, "opt_dist": 1600, "wins": "2-0-1-3"},
        {"horse": "ダノンエアズロック", "race_type": "毎日王冠", "sire": "モーリス", "style": "先行", "stamina": 83, "speed": 88, "power": 86, "heavy": 86, "opt_dist": 1800, "wins": "3-0-0-3"},
        {"horse": "シャンパンカラー", "race_type": "毎日王冠", "sire": "ドゥラメンテ", "style": "追込", "stamina": 80, "speed": 90, "power": 88, "heavy": 94, "opt_dist": 1600, "wins": "3-0-1-5"},
        {"horse": "セイウンハーデス", "race_type": "毎日王冠", "sire": "シルバーステート", "style": "逃げ", "stamina": 84, "speed": 85, "power": 86, "heavy": 90, "opt_dist": 1800, "wins": "3-2-1-5"},
        {"horse": "レディネス", "race_type": "毎日王冠", "sire": "リアルスティール", "style": "先行", "stamina": 81, "speed": 84, "power": 82, "heavy": 85, "opt_dist": 1800, "wins": "2-2-1-4"},
        {"horse": "クルゼイロドスル", "race_type": "毎日王冠", "sire": "ファインニードル", "style": "追込", "stamina": 78, "speed": 85, "power": 83, "heavy": 82, "opt_dist": 1600, "wins": "3-1-1-6"},
        {"horse": "ライヒスアドラー", "race_type": "毎日王冠", "sire": "シスキン", "style": "差し", "stamina": 80, "speed": 88, "power": 81, "heavy": 86, "opt_dist": 1800, "wins": "2-1-1-3"},
        {"horse": "ロングラン", "race_type": "毎日王冠", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 82, "speed": 83, "power": 85, "heavy": 92, "opt_dist": 1800, "wins": "5-2-1-10"},
        {"horse": "ビーアストニッシド", "race_type": "毎日王冠", "sire": "アメリカンペイトリオット", "style": "逃げ", "stamina": 80, "speed": 84, "power": 85, "heavy": 88, "opt_dist": 1800, "wins": "2-2-2-12"},
        {"horse": "ドラゴンブースト", "race_type": "毎日王冠", "sire": "ディーマジェスティ", "style": "差し", "stamina": 81, "speed": 85, "power": 83, "heavy": 87, "opt_dist": 1800, "wins": "2-1-1-5"},
        {"horse": "ランスオブカオス", "race_type": "毎日王冠", "sire": "シルバーステート", "style": "差し", "stamina": 81, "speed": 86, "power": 84, "heavy": 86, "opt_dist": 1800, "wins": "2-2-0-4"},
        {"horse": "レガーロデルシエロ", "race_type": "毎日王冠", "sire": "ロードカナロア", "style": "差し", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1600, "wins": "3-1-2-4"},
        {"horse": "アドマイヤクワッズ", "race_type": "毎日王冠", "sire": "リアルスティール", "style": "差し", "stamina": 79, "speed": 88, "power": 81, "heavy": 85, "opt_dist": 1600, "wins": "2-1-0-3"},

        # --- 京都大賞典（全18頭） ---
        {"horse": "ヘデントール", "race_type": "京都大賞典", "sire": "ルーラーシップ", "style": "差し", "stamina": 93, "speed": 88, "power": 87, "heavy": 102, "opt_dist": 2400, "wins": "4-2-0-1"},
        {"horse": "ディープモンスター", "race_type": "京都大賞典", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 85, "power": 88, "heavy": 112, "opt_dist": 2400, "wins": "5-3-2-9"},
        {"horse": "アクアヴァーナル", "race_type": "京都大賞典", "sire": "エピファネイア", "style": "差し", "stamina": 88, "speed": 86, "power": 84, "heavy": 98, "opt_dist": 2400, "wins": "3-2-1-6"},
        {"horse": "ダノンシーマ", "race_type": "京都大賞典", "sire": "キタサンブラック", "style": "先行", "stamina": 89, "speed": 86, "power": 86, "heavy": 95, "opt_dist": 2400, "wins": "3-3-1-4"},
        {"horse": "ショウナンラプンタ", "race_type": "京都大賞典", "sire": "キズナ", "style": "追込", "stamina": 89, "speed": 86, "power": 87, "heavy": 96, "opt_dist": 2400, "wins": "2-2-2-5"},
        {"horse": "ヴェルテンベルク", "race_type": "京都大賞典", "sire": "キタサンブラック", "style": "追込", "stamina": 90, "speed": 81, "power": 85, "heavy": 100, "opt_dist": 2400, "wins": "3-1-2-8"},
        {"horse": "サヴォーナ", "race_type": "京都大賞典", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 84, "power": 88, "heavy": 96, "opt_dist": 2400, "wins": "3-5-2-7"},
        {"horse": "リビアングラス", "race_type": "京都大賞典", "sire": "キズナ", "style": "逃げ", "stamina": 89, "speed": 83, "power": 86, "heavy": 94, "opt_dist": 2400, "wins": "3-2-1-7"},
        {"horse": "ウエストナウ", "race_type": "京都大賞典", "sire": "キズナ", "style": "先行", "stamina": 87, "speed": 84, "power": 85, "heavy": 92, "opt_dist": 2400, "wins": "2-1-0-3"},
        {"horse": "ヴェルミセル", "race_type": "京都大賞典", "sire": "ゴールドシップ", "style": "追込", "stamina": 92, "speed": 78, "power": 86, "heavy": 110, "opt_dist": 2400, "wins": "4-1-2-11"},
        {"horse": "エコロディノス", "race_type": "京都大賞典", "sire": "キタサンブラック", "style": "先行", "stamina": 86, "speed": 83, "power": 84, "heavy": 90, "opt_dist": 2200, "wins": "3-2-0-5"},
        {"horse": "キングスコール", "race_type": "京都大賞典", "sire": "ドゥラメンテ", "style": "差し", "stamina": 88, "speed": 85, "power": 87, "heavy": 88, "opt_dist": 2400, "wins": "2-1-1-2"},
        {"horse": "サフィラ", "race_type": "京都大賞典", "sire": "ハーツクライ", "style": "差し", "stamina": 86, "speed": 87, "power": 82, "heavy": 88, "opt_dist": 2200, "wins": "1-2-1-3"},
        {"horse": "ファミリータイム", "race_type": "京都大賞典", "sire": "リアルスティール", "style": "差し", "stamina": 88, "speed": 82, "power": 85, "heavy": 90, "opt_dist": 2400, "wins": "3-1-2-6"},
        {"horse": "マイネルエンペラー", "race_type": "京都大賞典", "sire": "ゴールドシップ", "style": "追込", "stamina": 91, "speed": 81, "power": 87, "heavy": 108, "opt_dist": 2400, "wins": "4-3-2-8"},
        {"horse": "ミクニインスパイア", "race_type": "京都大賞典", "sire": "エピファネイア", "style": "差し", "stamina": 87, "speed": 85, "power": 84, "heavy": 92, "opt_dist": 2200, "wins": "2-2-1-5"},
        {"horse": "ミステリーウェイ", "race_type": "京都大賞典", "sire": "ジャスタウェイ", "style": "先行", "stamina": 88, "speed": 82, "power": 86, "heavy": 95, "opt_dist": 2400, "wins": "3-4-1-8"},
        {"horse": "メイショウブレゲ", "race_type": "京都大賞典", "sire": "ゴールドシップ", "style": "追込", "stamina": 95, "speed": 77, "power": 85, "heavy": 115, "opt_dist": 3000, "wins": "5-2-2-15"}
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 レースシミュレーション", "📊 出走馬データベース"])

with tab_sim:
    st.subheader("⚙ レース条件設定")
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
    
    default_list = df_all[df_all["race_type"] == "毎日王冠"]["horse"].tolist()
    
    if btn_col1.button("🎯 毎日王冠（全17頭をセット）"):
        default_list = df_all[df_all["race_type"] == "毎日王冠"]["horse"].tolist()
    if btn_col2.button("🏆 京都大賞典（全18頭をセット）"):
        default_list = df_all[df_all["race_type"] == "京都大賞典"]["horse"].tolist()

    selected_horses = st.multiselect(
        "出走馬を選択（2〜18頭）",
        options=df_all["horse"].tolist(),
        default=default_list
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ 出走馬を【2頭以上】選択してください。")
    else:
        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        if len(df_race) > 18:
            df_race = df_race.head(18)
        
        df_race["num"] = [i + 1 for i in range(len(df_race))]

        st.dataframe(
            df_race[["num", "horse", "race_type", "style", "opt_dist", "wins", "sire"]]
            .rename(columns={"num": "馬番", "horse": "馬名", "race_type": "該当レース", "style": "脚質", "opt_dist": "適性距離", "wins": "戦績", "sire": "父"}),
            hide_index=True,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🏁 リアルコース再現レース実況")

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
                .status-box {{ font-size: 15px; font-weight: bold; color: #2ecc71; min-height: 28px; margin-bottom: 8px; }}
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
                    <svg id="trackSvg" viewBox="0 0 600 340" width="100%">
                        <!-- コース芝生 -->
                        <path id="outerTrack" d="M 180 50 L 420 50 A 100 100 0 0 1 420 250 L 180 250 A 100 100 0 0 1 180 50 Z" fill="#1b4d3e" stroke="#2e8b57" stroke-width="24"/>
                        <path id="innerTrack" d="M 180 62 L 420 62 A 88 88 0 0 1 420 238 L 180 238 A 88 88 0 0 1 180 62 Z" fill="#0e1117" stroke="#0e1117" stroke-width="2"/>

                        <!-- ポケット線（東京1800m用） -->
                        <path id="pocketLine" d="M 420 50 L 500 20" stroke="#2e8b57" stroke-width="14" fill="none" style="display:none;"/>

                        <!-- 坂道区間示標 -->
                        <path id="slopeIndicator" d="" fill="none" stroke="rgba(230,126,34,0.7)" stroke-width="8" stroke-dasharray="6,4"/>

                        <!-- スタート＆ゴールライン -->
                        <g id="goalGroup"></g>
                        <g id="startGroup"></g>
                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 16px;">🏆 着順確定結果</div>
                    <div id="resultsContent">発走準備完了</div>
                </div>
            </div>

            <script>
                const horsesData = {json.dumps(horses_js)};
                const raceConfig = {json.dumps(race_config_js)};
                let animId = null;

                function getWakuStyle(num, total) {{
                    let waku = Math.ceil((num / total) * 8);
                    if (total <= 8) waku = num;
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

                const COURSE_SPECS = {{
                    "東京": {{
                        dir: -1,
                        goalP: 0.10,
                        startP: raceConfig.dist === 1800 ? 0.68 : (raceConfig.dist === 1600 ? 0.58 : 0.20),
                        hasPocket: raceConfig.dist === 1800,
                        slopeP: [0.02, 0.12]
                    }},
                    "中山": {{
                        dir: 1,
                        goalP: 0.10,
                        startP: raceConfig.dist === 2000 ? 0.02 : (raceConfig.dist === 1600 ? 0.55 : 0.30),
                        slopeP: [0.02, 0.08]
                    }},
                    "京都": {{
                        dir: 1,
                        goalP: 0.10,
                        startP: raceConfig.dist === 2400 ? 0.10 : 0.60,
                        slopeP: [0.40, 0.60]
                    }},
                    "阪神": {{
                        dir: 1,
                        goalP: 0.10,
                        startP: raceConfig.dist === 2000 ? 0.20 : 0.55,
                        slopeP: [0.02, 0.08]
                    }}
                }};

                const spec = COURSE_SPECS[raceConfig.venue] || COURSE_SPECS["東京"];

                function getTrackPoint(p, laneOffset = 0) {{
                    p = (p % 1.0 + 1.0) % 1.0;
                    const r = 100 + laneOffset;
                    const lenStr = 240;
                    const circumference = 2 * Math.PI * r + 2 * lenStr;
                    const distOnTrack = p * circumference;

                    let x, y, angle;

                    if (distOnTrack <= lenStr) {{
                        x = 420 - distOnTrack;
                        y = 250 + laneOffset;
                        angle = Math.PI;
                    }} else if (distOnTrack <= lenStr + Math.PI * r) {{
                        const arcLen = distOnTrack - lenStr;
                        const theta = Math.PI / 2 + (arcLen / r);
                        x = 180 + r * Math.cos(theta);
                        y = 150 + r * Math.sin(theta);
                        angle = theta + Math.PI / 2;
                    }} else if (distOnTrack <= 2 * lenStr + Math.PI * r) {{
                        const strLen2 = distOnTrack - (lenStr + Math.PI * r);
                        x = 180 + strLen2;
                        y = 50 - laneOffset;
                        angle = 0;
                    }} else {{
                        const arcLen2 = distOnTrack - (2 * lenStr + Math.PI * r);
                        const theta = -Math.PI / 2 + (arcLen2 / r);
                        x = 420 + r * Math.cos(theta);
                        y = 150 + r * Math.sin(theta);
                        angle = theta + Math.PI / 2;
                    }}

                    if (spec.dir === -1) {{
                        x = 600 - x;
                        angle = Math.PI - angle;
                    }}

                    return {{ x, y, angle }};
                }}

                function drawCourse() {{
                    const pocket = document.getElementById('pocketLine');
                    if (spec.hasPocket) pocket.style.display = 'block';

                    const goalPt = getTrackPoint(spec.goalP);
                    const goalGroup = document.getElementById('goalGroup');
                    goalGroup.innerHTML = `
                        <line x1="${{goalPt.x}}" y1="${{goalPt.y - 15}}" x2="${{goalPt.x}}" y2="${{goalPt.y + 15}}" stroke="#ff4b4b" stroke-width="4" stroke-dasharray="3"/>
                        <text x="${{goalPt.x}}" y="${{goalPt.y + 28}}" fill="#ff4b4b" font-size="12" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
                    `;

                    const startPt = getTrackPoint(spec.startP);
                    const startGroup = document.getElementById('startGroup');
                    startGroup.innerHTML = `
                        <line x1="${{startPt.x}}" y1="${{startPt.y - 12}}" x2="${{startPt.x}}" y2="${{startPt.y + 12}}" stroke="#2ecc71" stroke-width="3"/>
                        <text x="${{startPt.x}}" y="${{startPt.y - 16}}" fill="#2ecc71" font-size="11" font-weight="bold" text-anchor="middle">START</text>
                    `;
                }}
                drawCourse();

                document.getElementById('startBtn').addEventListener('click', startSimulation);

                function startSimulation() {{
                    if (animId) cancelAnimationFrame(animId);

                    const group = document.getElementById('horsesGroup');
                    const status = document.getElementById('statusBox');
                    const resultsContent = document.getElementById('resultsContent');
                    
                    group.innerHTML = '';
                    resultsContent.innerHTML = '<div style="padding:10px; color:#8b949e;">⏱ ゲートが開きました！レース観戦中...</div>';

                    const totalDistRaps = raceConfig.dist / 2000.0;

                    const runners = horsesData.map((h, i) => {{
                        const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                        const wakuStyle = getWakuStyle(h.num, horsesData.length);

                        const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                        const distPenalty = Math.max(0, (distDiff - 200) * 0.05);

                        const conditionMod = 0.94 + Math.random() * 0.12; 
                        const spurtPoint = spec.startP + (totalDistRaps * (0.65 + Math.random() * 0.15));

                        return {{
                            ...h,
                            laneOffset: laneOffset,
                            wakuStyle: wakuStyle,
                            progress: spec.startP,
                            targetProgress: spec.startP + totalDistRaps,
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
                                let curSpeed = h.speed * h.conditionMod * 0.000035;

                                if (h.progress >= h.spurtPoint) {{
                                    if (h.style === "差し" || h.style === "追込") curSpeed *= 1.28;
                                    else curSpeed *= 1.12;
                                }}

                                const pNorm = (h.progress % 1.0);
                                if (pNorm >= spec.slopeP[0] && pNorm <= spec.slopeP[1]) {{
                                    curSpeed *= 0.88;
                                }}

                                h.staminaRem -= 0.04;
                                if (h.staminaRem <= 0) curSpeed *= 0.65;

                                h.progress += curSpeed;

                                if (h.progress >= h.targetProgress) {{
                                    h.finished = true;
                                    finishedCount++;
                                    h.rank = finishedCount;
                                }}
                            }}

                            const pt = getTrackPoint(h.progress, h.laneOffset);

                            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                            g.setAttribute('transform', `translate(${{pt.x}}, ${{pt.y}})`);
                            g.innerHTML = `
                                <circle cx="0" cy="0" r="7" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="0" y="3" font-size="9" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                                <text x="10" y="3" font-size="9" font-weight="bold" fill="white">${{h.name}}</text>
                            `;
                            group.appendChild(g);
                        }});

                        if (finishedCount === 0) {{
                            status.innerText = '🏇 ' + raceConfig.venue + ' ' + raceConfig.dist + 'm 各馬一斉にスタート！';
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = '🏁 ' + finishedCount + '頭ゴール！直線での激しい叩き合い！';
                        }} else {{
                            status.innerText = '🏆 全頭ゴールイン！確定着順を一覧表示します';
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
        st.components.v1.html(html_code, height=600)

with tab_db:
    st.subheader("📊 登録馬一覧＆データ")
    st.dataframe(
        df_all[["horse", "race_type", "style", "opt_dist", "wins", "speed", "stamina", "power", "sire"]]
        .rename(columns={
            "horse": "馬名", "race_type": "該当レース", "style": "脚質", "opt_dist": "適性距離",
            "wins": "戦績(1着-2着-3着-着外)", "speed": "スピード",
            "stamina": "スタミナ", "power": "パワー", "sire": "父"
        }),
        use_container_width=True,
        hide_index=True
    )
