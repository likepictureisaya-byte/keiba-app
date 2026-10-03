import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定（モバイル最適化）
st.set_page_config(
    page_title="本格競馬シミュレーター",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# モバイルフレンドリー & タッチイベント修正CSS
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
st.caption("毎日王冠・京都大賞典 全馬収録！完全楕円軌道スムーズ周回版")

# 2. データベース（毎日王冠17頭 ＋ 京都大賞典18頭 ＋ 主力古馬）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠 (17頭) ---
        {"horse": "セイウンハーデス", "sire": "シルバーステート", "style": "逃げ", "stamina": 84, "speed": 85, "power": 86, "heavy": 90, "opt_dist": 1800, "desc": "果敢にハナを奪いロングスパートをかける。"},
        {"horse": "リアライズシリウス", "sire": "ポアゾンブラック", "style": "先行", "stamina": 80, "speed": 89, "power": 82, "heavy": 90, "opt_dist": 1600, "desc": "マイル〜1800mで鋭いスピードを見せる3歳勢。"},
        {"horse": "レディネス", "sire": "リアルスティール", "style": "先行", "stamina": 81, "speed": 84, "power": 82, "heavy": 85, "opt_dist": 1800, "desc": "好位で立ち回る堅実な走り。"},
        {"horse": "サトノシャイニング", "sire": "キズナ", "style": "先行", "stamina": 82, "speed": 89, "power": 84, "heavy": 88, "opt_dist": 1800, "desc": "抜群のスピード持続力を持つ注目馬。"},
        {"horse": "クルゼイロドスル", "sire": "ファインニードル", "style": "追込", "stamina": 78, "speed": 85, "power": 83, "heavy": 82, "opt_dist": 1600, "desc": "一瞬のキレ味で一発を狙う。"},
        {"horse": "ライヒスアドラー", "sire": "シスキン", "style": "差し", "stamina": 80, "speed": 88, "power": 81, "heavy": 86, "opt_dist": 1800, "desc": "皐月賞上位入着の実力派3歳馬。"},
        {"horse": "ロングラン", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 82, "speed": 83, "power": 85, "heavy": 92, "opt_dist": 1800, "desc": "展開が向けば後方から一気に押し寄せる。"},
        {"horse": "ビーアストニッシド", "sire": "アメリカンペイトリオット", "style": "逃げ", "stamina": 80, "speed": 84, "power": 85, "heavy": 88, "opt_dist": 1800, "desc": "粘り強さを生かして先頭で粘る。"},
        {"horse": "ドラゴンブースト", "sire": "ディーマジェスティ", "style": "差し", "stamina": 81, "speed": 85, "power": 83, "heavy": 87, "opt_dist": 1800, "desc": "中団からしぶとく足を伸ばす。"},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "style": "先行", "stamina": 83, "speed": 87, "power": 86, "heavy": 95, "opt_dist": 1800, "desc": "勝負根性と重馬場こなすパワーが武器。"},
        {"horse": "ランスオブカオス", "sire": "シルバーステート", "style": "差し", "stamina": 81, "speed": 86, "power": 84, "heavy": 86, "opt_dist": 1800, "desc": "直線の長いコースで伸びを見せる。"},
        {"horse": "レガーロデルシエロ", "sire": "ロードカナロア", "style": "差し", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1600, "desc": "マイル〜1800mでの差し脚に定評あり。"},
        {"horse": "ホウオウビスケッツ", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 83, "speed": 88, "power": 87, "heavy": 92, "opt_dist": 1800, "desc": "絶妙なペース配分で押し切る先頭主張派。"},
        {"horse": "レイニング", "sire": "サートゥルナーリア", "style": "差し", "stamina": 82, "speed": 89, "power": 83, "heavy": 88, "opt_dist": 1800, "desc": "名手ルメールの手綱でキレ味を発揮。"},
        {"horse": "シャンパンカラー", "sire": "ドゥラメンテ", "style": "追込", "stamina": 80, "speed": 90, "power": 88, "heavy": 94, "opt_dist": 1600, "desc": "NHKマイルC勝ち馬。爆発力は抜群。"},
        {"horse": "アドマイヤクワッズ", "sire": "リアルスティール", "style": "差し", "stamina": 79, "speed": 88, "power": 81, "heavy": 85, "opt_dist": 1600, "desc": "鋭い決め脚を持つ3歳期待馬。"},
        {"horse": "ダノンエアズロック", "sire": "モーリス", "style": "先行", "stamina": 83, "speed": 88, "power": 86, "heavy": 86, "opt_dist": 1800, "desc": "東京1800mで高いパフォーマンスを発揮。"},

        # --- 京都大賞典 (18頭) ---
        {"horse": "アクアヴァーナル", "sire": "エピファネイア", "style": "差し", "stamina": 88, "speed": 86, "power": 84, "heavy": 98, "opt_dist": 2400, "desc": "万葉S勝ち＆天皇賞春4着の実力派牝馬。"},
        {"horse": "ウエストナウ", "sire": "キズナ", "style": "先行", "stamina": 87, "speed": 84, "power": 85, "heavy": 92, "opt_dist": 2400, "desc": "京都コースで先行力を活かして押し切る。"},
        {"horse": "ヴェルテンベルク", "sire": "キタサンブラック", "style": "追込", "stamina": 90, "speed": 81, "power": 85, "heavy": 100, "opt_dist": 2400, "desc": "長距離戦で堅実に足を伸ばすステイヤー。"},
        {"horse": "ヴェルミセル", "sire": "ゴールドシップ", "style": "追込", "stamina": 92, "speed": 78, "power": 86, "heavy": 110, "opt_dist": 2400, "desc": "ゴールドシップ産駒らしいタフなスタミナ型。"},
        {"horse": "エコロディノス", "sire": "キタサンブラック", "style": "先行", "stamina": 86, "speed": 83, "power": 84, "heavy": 90, "opt_dist": 2200, "desc": "先行ポジションからレースを作る。"},
        {"horse": "キングスコール", "sire": "ドゥラメンテ", "style": "差し", "stamina": 88, "speed": 85, "power": 87, "heavy": 88, "opt_dist": 2400, "desc": "力強い脚取りで坂を駆け上がる。"},
        {"horse": "サヴォーナ", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 84, "power": 88, "heavy": 96, "opt_dist": 2400, "desc": "重傷戦で常に上位争いに入るしぶとさ。"},
        {"horse": "サフィラ", "sire": "ハーツクライ", "style": "差し", "stamina": 86, "speed": 87, "power": 82, "heavy": 88, "opt_dist": 2200, "desc": "良血牝馬。末脚の伸ばしどころが鍵。"},
        {"horse": "ショウナンラプンタ", "sire": "キズナ", "style": "追込", "stamina": 89, "speed": 86, "power": 87, "heavy": 96, "opt_dist": 2400, "desc": "G1常連。久々の一戦で一変を狙う。"},
        {"horse": "ダノンシーマ", "sire": "キタサンブラック", "style": "先行", "stamina": 89, "speed": 86, "power": 86, "heavy": 95, "opt_dist": 2400, "desc": "重賞で連続3着。安定感が魅力。"},
        {"horse": "ディープモンスター", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 85, "power": 88, "heavy": 112, "opt_dist": 2400, "desc": "昨年の京都大賞典覇者。タフな馬場も苦にしない。"},
        {"horse": "ファミリータイム", "sire": "リアルスティール", "style": "差し", "stamina": 88, "speed": 82, "power": 85, "heavy": 90, "opt_dist": 2400, "desc": "宝塚記念6着。京都芝2400mに適性あり。"},
        {"horse": "ヘデントール", "sire": "ルーラーシップ", "style": "差し", "stamina": 93, "speed": 88, "power": 87, "heavy": 102, "opt_dist": 2400, "desc": "2025年天皇賞（春）勝ち馬。能力は随一。"},
        {"horse": "マイネルエンペラー", "sire": "ゴールドシップ", "style": "追込", "stamina": 91, "speed": 81, "power": 87, "heavy": 108, "opt_dist": 2400, "desc": "タフな馬場で真価を発揮するステイヤー。"},
        {"horse": "ミクニインスパイア", "sire": "エピファネイア", "style": "差し", "stamina": 87, "speed": 85, "power": 84, "heavy": 92, "opt_dist": 2200, "desc": "デムーロ騎手の手綱で一発を秘める。"},
        {"horse": "ミステリーウェイ", "sire": "ジャスタウェイ", "style": "先行", "stamina": 88, "speed": 82, "power": 86, "heavy": 95, "opt_dist": 2400, "desc": "スタミナを生かした粘り込み。"},
        {"horse": "メイショウブレゲ", "sire": "ゴールドシップ", "style": "追込", "stamina": 95, "speed": 77, "power": 85, "heavy": 115, "opt_dist": 3000, "desc": "超長距離＆極悪馬場の鬼。"},
        {"horse": "リビアングラス", "sire": "キズナ", "style": "逃げ", "stamina": 89, "speed": 83, "power": 86, "heavy": 94, "opt_dist": 2400, "desc": "逃げ脚を伸ばしての粘り残りを得意とする。"}
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 全馬データ検索"])

# --- TAB 1: シミュレーター ---
with tab_sim:
    st.subheader("⚙️ レース条件")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        venue = st.selectbox("競馬場", ["東京", "京都", "中山", "阪神"])
    with col_c2:
        dist = st.selectbox("距離(m)", [1800, 2400, 1600, 2000, 3000])
    with col_c3:
        going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.markdown("---")
    st.subheader("🐎 出走馬セット（ワンタップ選択）")
    
    # クイックセットボタン
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    main_default = ["サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "ヘデントール", "ディープモンスター", "アクアヴァーナル"]
    
    if btn_col1.button("🎯 毎日王冠（全17頭）"):
        main_default = [h for h in df_all["horse"] if h in [
            "サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "レイニング", 
            "リアライズシリウス", "ダノンエアズロック", "シャンパンカラー", "セイウンハーデス"
        ]]
    if btn_col2.button("🏆 京都大賞典（全18頭）"):
        main_default = [h for h in df_all["horse"] if h in [
            "ヘデントール", "ディープモンスター", "アクアヴァーナル", "ダノンシーマ", 
            "ショウナンラプンタ", "ヴェルテンベルク", "サヴォーナ", "リビアングラス"
        ]]

    selected_horses = st.multiselect(
        "出走馬を選択（2〜8頭）",
        options=df_all["horse"].tolist(),
        default=main_default
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ 出走馬を【2頭以上】選択してください。")
    else:
        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        if len(df_race) > 8:
            df_race = df_race.head(8) # 描画崩れ防止のため8頭制限
            st.info("※シミュレーション画面での見やすさのため、上位8頭を表示しています。")
        
        df_race["num"] = [i + 1 for i in range(len(df_race))]

        # 出走表
        st.dataframe(
            df_race[["num", "horse", "style", "opt_dist", "sire"]]
            .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "opt_dist": "適性距離", "sire": "父"}),
            hide_index=True,
            use_container_width=True
        )

        # --- HTML5 / JS (完全極座標・スムーズ楕円エンジン) ---
        st.markdown("---")
        st.subheader("🏁 完全スムーズ楕円周回アニメーション")

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
                .results-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 6px; margin-top: 6px; }}
                .rank-card {{ background: #21262d; padding: 6px 8px; border-radius: 6px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="sim-container">
                <button id="startBtn" class="start-btn">▶ レーススタート</button>
                <div id="statusBox" class="status-box">「スタート」を押してください</div>
                
                <div class="svg-wrapper">
                    <svg id="trackSvg" viewBox="0 0 600 300" width="100%">
                        <!-- トラック描画 (外楕円 R_x=220, R_y=100 / 内楕円 R_x=140, R_y=50) -->
                        <ellipse cx="300" cy="150" rx="230" ry="110" fill="#1b4d3e" stroke="#2e8b57" stroke-width="8"/>
                        <ellipse cx="300" cy="150" rx="140" ry="50" fill="#0e1117" stroke="#2e8b57" stroke-width="6"/>
                        
                        <!-- ゴールライン (下直線右側 x=420, y=200〜260) -->
                        <line x1="420" y1="200" x2="420" y2="260" stroke="#ff4b4b" stroke-width="4" stroke-dasharray="3"/>
                        <text x="420" y="195" fill="#ff4b4b" font-size="11" font-weight="bold" text-anchor="middle">GOAL</text>
                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 15px;">🏆 着順確定</div>
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

                    // 馬の初期設定
                    const runners = horsesData.map((h, i) => {{
                        const laneOffset = (i - (horsesData.length - 1) / 2) * 6; // レーン幅
                        return {{
                            ...h,
                            laneOffset: laneOffset,
                            angle: Math.PI / 2, // 下側中央スタート (+90度)
                            distanceMoved: 0,
                            maxDistance: Math.PI * 2, // 1周分
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
                                // ゆっくり滑らかな速度
                                let step = h.speed * 0.00012;

                                // 脚質スパート
                                if (h.distanceMoved > Math.PI * 1.3) {{
                                    if (h.style === "差し" || h.style === "追込") step *= 1.18;
                                }}

                                h.distanceMoved += step;
                                h.angle = (Math.PI / 2) + h.distanceMoved; // 反時計回りに周回

                                if (h.distanceMoved >= h.maxDistance) {{
                                    h.finished = true;
                                    finishedCount++;
                                    h.rank = finishedCount;
                                }}
                            }}

                            // --- 真の数学的楕円パラメータ計算 ---
                            // 中心(300, 150), 基本半径 (Rx=185, Ry=80)
                            const rx = 185 + h.laneOffset;
                            const ry = 80 + h.laneOffset * 0.4;

                            const x = 300 + rx * Math.cos(h.angle);
                            const y = 150 + ry * Math.sin(h.angle);

                            // 馬アイコン描画
                            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                            g.setAttribute('transform', `translate(${{x}}, ${{y}})`);
                            g.innerHTML = `
                                <circle cx="0" cy="0" r="9" fill="${{h.color}}" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="0" y="3" font-size="9" font-weight="bold" fill="white" text-anchor="middle">${{h.num}}</text>
                                <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${{h.name}}</text>
                            `;
                            group.appendChild(g);
                        }});

                        if (finishedCount === 0) {{
                            status.innerText = "🏁 各馬が綺麗に楕円コースを周回中！";
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = `🏁 ${{finishedCount}}頭ゴール！`;
                        }} else {{
                            status.innerText = "🏆 全頭ゴールイン！";
                        }}

                        if (finishedCount < totalHorses) {{
                            animId = requestAnimationFrame(animate);
                        }} else {{
                            runners.sort((a, b) => a.rank - b.rank);
                            resultsList.innerHTML = '';
                            runners.forEach((h) => {{
                                const rankText = h.rank === 1 ? '🥇 1着' : h.rank === 2 ? '🥈 2着' : h.rank === 3 ? '🥉 3着' : `${{h.rank}}着`;
                                resultsList.innerHTML += `
                                    <div class="rank-card" style="border-left: 4px solid ${{h.color}};">
                                        <div style="font-weight:bold; color:#fff;">${{rankText}}: [${{h.num}}] ${{h.name}}</div>
                                        <div style="color:#8b949e; font-size:11px;">${{h.style}} | ${{h.sire}}</div>
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
        st.components.v1.html(html_code, height=520)

# --- TAB 2: 全馬データベース ---
with tab_db:
    st.subheader("🔍 馬データ検索（全35頭収録）")
    search_q = st.text_input("🔎 馬名や血統で検索", "")

    df_show = df_all.copy()
    if search_q:
        df_show = df_show[
            df_show["horse"].str.contains(search_q, case=False) |
            df_show["sire"].str.contains(search_q, case=False)
        ]

    st.dataframe(
        df_show[["horse", "sire", "style", "opt_dist", "speed", "stamina", "power", "heavy", "desc"]]
        .rename(columns={
            "horse": "馬名", "sire": "父", "style": "脚質", "opt_dist": "適性距離",
            "speed": "スピード", "stamina": "スタミナ", "power": "パワー", "heavy": "重馬場", "desc": "特徴"
        }),
        hide_index=True,
        use_container_width=True
    )
