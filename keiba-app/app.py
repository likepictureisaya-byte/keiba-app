import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定（モバイル最適化）
st.set_page_config(
    page_title="本格競馬シミュレーター",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# モバイルフレンドリーなスタイルCSS調整
st.markdown("""
<style>
    /* スマホ画面での操作性向上のためのCSS */
    .stMultiSelect, .stSelectbox, .stButton {
        touch-action: manipulation;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            height: 50px;
            font-size: 18px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🏇 本格競馬シミュレーター")
st.caption("最新出走馬データ対応！コーナー滑らか周回＆スマホ完全対応レスポンシブ版")

# 2. データベース
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠 出走メンバー ---
        {"horse": "サトノシャイニング", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1800, "desc": "抜群のスピード持続力と好位での立ち回りが持ち味。"},
        {"horse": "レーベンスティール", "sire": "リアルスティール", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 90, "power": 83, "heavy": 88, "opt_dist": 1800, "desc": "東京1800mでのキレ味は現役トップクラス。"},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 82, "speed": 86, "power": 84, "heavy": 95, "desc": "粘り強い勝負根性と重馬場こなすパワーが武器。"},
        {"horse": "ホウオウビスケッツ", "sire": "マインドユアビスケッツ", "sire_line": "その他", "style": "逃げ", "stamina": 83, "speed": 87, "power": 85, "heavy": 92, "desc": "絶妙なペース配分で押し切るハナ主張型。"},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 85, "speed": 88, "power": 80, "heavy": 88, "opt_dist": 2000, "desc": "オークス・秋華賞二冠馬。末脚の伸びは特級品。"},
        {"horse": "リアライズシリウス", "sire": "ポアゾンブラック", "sire_line": "その他", "style": "先行", "stamina": 78, "speed": 89, "power": 80, "heavy": 90, "opt_dist": 1600, "desc": "マイル〜1800mで鋭いスピードを見せる。"},
        {"horse": "シルトホルン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "先行", "stamina": 80, "speed": 82, "power": 84, "heavy": 98, "opt_dist": 1800, "desc": "タフな道悪馬場でも粘り込む。"},

        # --- 京都大賞典 出走メンバー ---
        {"horse": "ディープモンスター", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 83, "power": 88, "heavy": 112, "opt_dist": 2400, "desc": "重馬場・タフ馬場になれば抜群の粘り強さ。"},
        {"horse": "ヘデントール", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 92, "speed": 86, "power": 86, "heavy": 102, "opt_dist": 2400, "desc": "長距離路線で頭角を現すステイヤー。"},
        {"horse": "ショウナンラプンタ", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 89, "speed": 85, "power": 87, "heavy": 96, "opt_dist": 2400, "desc": "後方からのロングスパートが強み。"},
        {"horse": "メイショウブレゲ", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 95, "speed": 76, "power": 85, "heavy": 115, "opt_dist": 3000, "desc": "超長距離・道悪馬場の鬼。"},
        {"horse": "ダノンシーマ", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 84, "power": 85, "heavy": 95, "opt_dist": 2200, "desc": "安定した立ち回りが魅力の先行タイプ。"},
        {"horse": "サンライズアース", "sire": "レイデオロ", "sire_line": "キングカメハメハ系", "style": "逃げ", "stamina": 90, "speed": 82, "power": 89, "heavy": 105, "opt_dist": 2400, "desc": "長距離をスタミナで押して逃げ切る。"},

        # --- 主要GI古馬 ---
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 93, "speed": 95, "power": 93, "heavy": 88, "opt_dist": 2000, "desc": "大阪杯勝ち馬。立ち回りの巧みさが強み。"},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 110, "opt_dist": 2200, "desc": "皐月賞馬。重馬場での圧倒的適性。"},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy": 91, "opt_dist": 2400, "desc": "日本ダービー馬。総合力が高い。"},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy": 115, "opt_dist": 2200, "desc": "宝塚記念勝ち馬。荒れた馬場に強い。"},
        {"horse": "ドウデュース", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 92, "speed": 98, "power": 96, "heavy": 90, "opt_dist": 2000, "desc": "驚異のピッチ走法と破格の爆発的末脚。"}
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ設計
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 馬の検索 & データベース"])

# --- TAB 1: シミュレーター ---
with tab_sim:
    st.sidebar.header("⚙️ レース条件設定")
    venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
    surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
    dist = st.sidebar.selectbox("距離 (m)", [1200, 1600, 1800, 2000, 2400, 3000])
    going = st.sidebar.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🐎 出走馬選択")

    selected_horses = st.sidebar.multiselect(
        "出走馬を選択 (2〜8頭)",
        options=df_all["horse"].tolist(),
        default=["サトノシャイニング", "レーベンスティール", "エルトンバローズ", "ディープモンスター", "メイショウブレゲ", "チェルヴィニア"]
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ スマホをお使いの場合は左上の「＞」ボタンを押してメニューを開き、出走馬を【2頭以上】選択してください。")
    else:
        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        df_race["num"] = [i + 1 for i in range(len(df_race))]

        # 指数算出
        going_p = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}.get(going, 1.0)
        df_race["score"] = (
            df_race["speed"] * 0.35 +
            df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
            df_race["power"] * 0.2 +
            (df_race["heavy"] - 90) * (1.1 - going_p) * 2.0
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("📋 出走表")
            st.dataframe(
                df_race[["num", "horse", "style", "opt_dist", "sire", "score"]]
                .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "opt_dist": "適性距離", "sire": "父", "score": "指数"})
                .style.format({"指数": "{:.1f}", "適性距離": "{:}m"}),
                hide_index=True,
                use_container_width=True
            )

        with col2:
            st.subheader("💡 展開ポイント")
            st.write(f"・**条件**: {venue} {surface}{dist}m ({going})")
            escape_count = len(df_race[df_race["style"] == "逃げ"])
            if escape_count >= 2:
                st.info("🔥 **ハイペース想定**: 逃げ馬が競り合うため、後半の差し・追込が届きやすい展開です。")
            else:
                st.info("🐢 **スロー〜ミドル想定**: 前寄りのポジション（逃げ・先行）が粘り残りやすい展開です。")

        # --- HTML5 / JS (幾何学コース追従 & スマホレスポンシブエンジン) ---
        st.markdown("---")
        st.subheader("🏁 完全コース追従レース（スマホ対応）")

        horses_js = []
        colors = ["#FF4B4B", "#FFA500", "#1E90FF", "#9B59B6", "#2ECC71", "#E67E22", "#00FFFF", "#FF00FF"]

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
                "color": colors[idx % len(colors)]
            })

        race_config_js = {"dist": dist, "going": going}

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                * {{ box-sizing: border-box; touch-action: manipulation; }}
                body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #0e1117; color: white; }}
                .sim-container {{ width: 100%; max-width: 800px; margin: 0 auto; padding: 10px; text-align: center; }}
                .start-btn {{
                    width: 100%;
                    max-width: 320px;
                    height: 54px;
                    background: linear-gradient(135deg, #ff4b4b, #d32f2f);
                    color: white;
                    border: none;
                    border-radius: 27px;
                    font-size: 20px;
                    font-weight: bold;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
                    margin-bottom: 12px;
                }}
                .start-btn:active {{ transform: scale(0.98); }}
                .status-box {{ font-size: 15px; font-weight: bold; color: #3498db; min-height: 24px; margin-bottom: 8px; }}
                .svg-wrapper {{ width: 100%; height: auto; background: #05140e; border-radius: 12px; border: 2px solid #1e3d30; overflow: hidden; }}
                .results-box {{ margin-top: 15px; background: #161b22; padding: 12px; border-radius: 10px; text-align: left; }}
                .results-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; margin-top: 8px; }}
                .rank-card {{ background: #21262d; padding: 8px 10px; border-radius: 6px; font-size: 13px; }}
            </style>
        </head>
        <body>
            <div class="sim-container">
                <button id="startBtn" class="start-btn">▶ レーススタート</button>
                <div id="statusBox" class="status-box">「スタート」を押してください</div>
                
                <div class="svg-wrapper">
                    <svg id="trackSvg" viewBox="0 0 600 300" width="100%" height="100%">
                        <!-- トラック描画 (標準スタジアム型) -->
                        <rect x="50" y="40" width="500" height="220" rx="110" ry="110" fill="#1b4d3e" stroke="#2e8b57" stroke-width="12"/>
                        <rect x="160" y="90" width="280" height="120" rx="60" ry="60" fill="#0e1117" stroke="#2e8b57" stroke-width="6"/>
                        <!-- ゴールライン (下直線の中央) -->
                        <line x1="300" y1="200" x2="300" y2="260" stroke="#ff4b4b" stroke-width="4" stroke-dasharray="4"/>
                        <text x="300" y="192" fill="#ff4b4b" font-size="12" font-weight="bold" text-anchor="middle">GOAL</text>
                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 16px;">🏆 確定順位 (全頭)</div>
                    <div id="resultsList" class="results-grid">スタート待ち...</div>
                </div>
            </div>

            <script>
                const horsesData = {json.dumps(horses_js)};
                const raceConfig = {json.dumps(race_config_js)};
                let animId = null;

                document.getElementById('startBtn').addEventListener('click', startSimulation);

                function startSimulation() {{
                    if (animId) cancelAnimationFrame(animId);

                    const group = document.getElementById('horsesGroup');
                    const status = document.getElementById('statusBox');
                    const resultsList = document.getElementById('resultsList');
                    
                    group.innerHTML = '';
                    resultsList.innerHTML = '⏱ レース走行中...';

                    let startTime = null;
                    const TOTAL_LAPS = 1.25; // 1周分＋直線

                    // 各馬の物理設定
                    const runners = horsesData.map((h, i) => {{
                        const distDiff = Math.abs(raceConfig.dist - h.opt_dist);
                        const staminaBurn = 1.0 + (distDiff > 200 ? (distDiff - 200) * 0.0012 : 0);
                        let wetMod = 1.0;
                        if (raceConfig.going === "重" || raceConfig.going === "不良") {{
                            wetMod = h.heavy / 92.0;
                        }}
                        const dailyCond = 0.96 + Math.random() * 0.08;

                        return {{
                            ...h,
                            lane: (i - (horsesData.length - 1) / 2) * 6, // レーンずれ
                            progress: 0, // 0.0 ～ 1.0
                            staminaRem: h.stamina * 10,
                            staminaBurn: staminaBurn,
                            wetMod: wetMod,
                            cond: dailyCond,
                            finished: false,
                            rank: 0
                        }};
                    }});

                    let finishedCount = 0;
                    const totalHorses = runners.length;

                    function animate(timestamp) {{
                        if (!startTime) startTime = timestamp;

                        group.innerHTML = '';

                        runners.forEach((h) => {{
                            if (!h.finished) {{
                                // リアルタイム速度計算
                                let curSpeed = h.speed * h.wetMod * h.cond * 0.00015;

                                // 脚質スパート
                                if (h.progress > 0.6) {{
                                    if (h.style === "差し" || h.style === "追込") curSpeed *= 1.12;
                                }}

                                // スタミナ切れ失速
                                h.staminaRem -= h.staminaBurn;
                                if (h.staminaRem <= 0) curSpeed *= 0.6;

                                h.progress += curSpeed;

                                // ゴール判定
                                if (h.progress >= 1.0) {{
                                    h.progress = 1.0;
                                    h.finished = true;
                                    finishedCount++;
                                    h.rank = finishedCount;
                                }}
                            }}

                            // --- 幾何学コース追従計算 (幾何学トラック) ---
                            // 楕円＋直線の正確な滑らか座標計算
                            const p = (h.progress * TOTAL_LAPS) % 1.0;
                            let x = 0, y = 0;

                            // 4区間（下直線 -> 右コーナー -> 上直線 -> 左コーナー）
                            if (p < 0.3) {{ // 下直線
                                const t = p / 0.3;
                                x = 160 + t * 280;
                                y = 230 + h.lane;
                            }} else if (p < 0.5) {{ // 右半円カーブ
                                const t = (p - 0.3) / 0.2;
                                const angle = -Math.PI / 2 + t * Math.PI;
                                x = 440 + Math.cos(angle) * (80 - h.lane);
                                y = 150 + Math.sin(angle) * (80 - h.lane);
                            }} else if (p < 0.8) {{ // 上直線
                                const t = (p - 0.5) / 0.3;
                                x = 440 - t * 280;
                                y = 70 - h.lane;
                            }} else {{ // 左半円カーブ
                                const t = (p - 0.8) / 0.2;
                                const angle = Math.PI / 2 + t * Math.PI;
                                x = 160 + Math.cos(angle) * (80 + h.lane);
                                y = 150 + Math.sin(angle) * (80 + h.lane);
                            }}

                            // 描画
                            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                            g.setAttribute('transform', `translate(${{x}}, ${{y}})`);
                            g.innerHTML = `
                                <circle cx="0" cy="0" r="9" fill="${{h.color}}" stroke="#ffffff" stroke-width="2"/>
                                <text x="0" y="3" font-size="9" font-weight="bold" fill="white" text-anchor="middle">${{h.num}}</text>
                                <text x="12" y="3" font-size="10" font-weight="bold" fill="white">${{h.name}}</text>
                            `;
                            group.appendChild(g);
                        }});

                        // 実況表示
                        if (finishedCount === 0) {{
                            status.innerText = "🏁 最終直線！各馬一斉にスパート！";
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = `🏁 ${{finishedCount}}頭ゴール！続々入線中...`;
                        }} else {{
                            status.innerText = "🏆 全頭ゴールイン！確定着順です！";
                        }}

                        // 全頭ゴールするまでループ継続
                        if (finishedCount < totalHorses) {{
                            animId = requestAnimationFrame(animate);
                        }} else {{
                            // 全着順表示
                            runners.sort((a, b) => a.rank - b.rank);
                            resultsList.innerHTML = '';
                            runners.forEach((h) => {{
                                const rankText = h.rank === 1 ? '🥇 1着' : h.rank === 2 ? '🥈 2着' : h.rank === 3 ? '🥉 3着' : `${{h.rank}}着`;
                                resultsList.innerHTML += `
                                    <div class="rank-card" style="border-left: 4px solid ${{h.color}};">
                                        <div style="font-weight:bold; color:#fff;">${{rankText}}: [${{h.num}}] ${{h.name}}</div>
                                        <div style="color:#8b949e; font-size:11px;">${{h.style}} | 適性${{h.opt_dist}}m</div>
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
        st.components.v1.html(html_code, height=580)

# --- TAB 2: 馬データベース ---
with tab_db:
    st.subheader("🔍 馬の検索 & 詳細データベース")
    search_query = st.text_input("🔎 馬名や血統で検索", "")

    df_filtered = df_all.copy()
    if search_query:
        df_filtered = df_filtered[
            df_filtered["horse"].str.contains(search_query, case=False) |
            df_filtered["sire"].str.contains(search_query, case=False)
        ]

    for idx, row in df_filtered.iterrows():
        with st.expander(f"🐎 [{row['style']}] {row['horse']} (父: {row['sire']})"):
            st.write(f"**適性距離:** {row['opt_dist']}m | **解説:** {row['desc']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.progress(row["speed"] / 100, text=f"スピード: {row['speed']}")
                st.progress(row["stamina"] / 100, text=f"スタミナ: {row['stamina']}")
            with col_b:
                st.progress(row["power"] / 100, text=f"パワー: {row['power']}")
                st.progress(min(1.0, row["heavy"] / 120), text=f"重馬場適性: {row['heavy']}")
