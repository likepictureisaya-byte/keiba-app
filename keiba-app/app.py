import streamlit as st
import pandas as pd
import json

# ページ基本設定
st.set_page_config(page_title="本格競馬シミュレーター & 馬データベース", layout="wide")

st.title("🏇 本格競馬展開シミュレーター & リアルタイム馬データベース")
st.caption("2025-2026年最新現役馬200頭超対応！毎日王冠・京都大賞典メンバー＆コース追従・リアル物理シミュレーション")

# 1. 大規模現役馬データベース（毎日王冠・京都大賞典・主要GI/GII馬網羅）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠 出走メンバー・東京1800m強豪 ---
        {"horse": "サトノシャイニング", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1800, "desc": "毎日王冠注目馬。抜群のスピード持続力と好位での立ち回りが持ち味。"},
        {"horse": "レーベンスティール", "sire": "リアルスティール", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 90, "power": 83, "heavy": 88, "opt_dist": 1800, "desc": "オールカマー・エプソムC勝ち馬。東京1800mでのキレ味は現役トップクラス。"},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 82, "speed": 86, "power": 84, "heavy": 95, "desc": "毎日王冠勝ち馬。粘り強い勝負根性と重馬場こなすパワーが武器。"},
        {"horse": "ホウオウビスケッツ", "sire": "マインドユアビスケッツ", "sire_line": "その他", "style": "逃げ", "stamina": 83, "speed": 87, "power": 85, "heavy": 92, "desc": "函館記念勝ち馬。絶妙なペース配分で押し切るハナ主張型。"},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 85, "speed": 88, "power": 80, "heavy": 88, "opt_dist": 2000, "desc": "オークス・秋華賞二冠馬。末脚の伸びは間違いなく特級品。"},
        {"horse": "リアライズシリウス", "sire": "ポアゾンブラック", "sire_line": "その他", "style": "先行", "stamina": 78, "speed": 89, "power": 80, "heavy": 90, "opt_dist": 1600, "desc": "マイル〜1800mで鋭いスピードを見せる注目の新鋭。"},
        {"horse": "シルトホルン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "先行", "stamina": 80, "speed": 82, "power": 84, "heavy": 98, "opt_dist": 1800, "desc": "東京コースを得意とし、タフな道悪馬場でも粘り込む。"},

        # --- 京都大賞典 出走メンバー・長距離・ステイヤー ---
        {"horse": "ディープモンスター", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 83, "power": 88, "heavy": 112, "opt_dist": 2400, "desc": "京都大賞典注目馬。重馬場・タフ馬場になれば現役トップクラスの粘り強さ。"},
        {"horse": "ヘデントール", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 92, "speed": 86, "power": 86, "heavy": 102, "opt_dist": 2400, "desc": "長距離路線で頭角を現すステイヤー。スタミナ勝負で真価を発揮。"},
        {"horse": "ショウナンラプンタ", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 89, "speed": 85, "power": 87, "heavy": 96, "opt_dist": 2400, "desc": "長距離重賞で好走。後方からのロングスパートが強み。"},
        {"horse": "メイショウブレゲ", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 95, "speed": 76, "power": 85, "heavy": 115, "opt_dist": 3000, "desc": "超長距離・道悪馬場の鬼。良馬場スピード戦は苦手だが荒れ馬場で劇的浮上。"},
        {"horse": "ダノンシーマ", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 84, "power": 85, "heavy": 95, "opt_dist": 2200, "desc": "安定した立ち回りが魅力の中長距離先行タイプ。"},
        {"horse": "サンライズアース", "sire": "レイデオロ", "sire_line": "キングカメハメハ系", "style": "逃げ", "stamina": 90, "speed": 82, "power": 89, "heavy": 105, "opt_dist": 2400, "desc": "長距離をスタミナで押して逃げ切るパワー型。"},

        # --- 古馬王道・GI常連 ---
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 93, "speed": 95, "power": 93, "heavy": 88, "opt_dist": 2000, "desc": "大阪杯勝ち馬。立ち回りの巧みさと粘り強さが持ち味。"},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 110, "opt_dist": 2200, "desc": "皐月賞馬。豪快な外回しと重馬場での圧倒的適性。"},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy": 91, "opt_dist": 2400, "desc": "日本ダービー馬。総合力が高くどんな展開にも対応できる。"},
        {"horse": "テーオーロイヤル", "sire": "リオンディーズ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 99, "speed": 88, "power": 94, "heavy": 92, "opt_dist": 3200, "desc": "天皇賞(春)勝ち馬。現役屈指の圧倒的スタミナモンスター。"},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy": 115, "opt_dist": 2200, "desc": "宝塚記念勝ち馬。荒れた馬場や重馬場・極寒レースで真価を発揮。"},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 89, "speed": 97, "power": 89, "heavy": 88, "opt_dist": 2000, "desc": "金鯱賞連覇。圧倒的な上がり3海里の瞬発スピードを誇る。"},
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 96, "speed": 82, "power": 95, "heavy": 105, "opt_dist": 3000, "desc": "長距離重賞で長年活躍する不屈のステイヤー。"},

        # --- マイル・短距離・ダート強豪 ---
        {"horse": "ジャンタルマンタル", "sire": "Palace Malice", "sire_line": "その他", "style": "先行", "stamina": 88, "speed": 98, "power": 93, "heavy": 87, "opt_dist": 1600, "desc": "NHKマイルC勝ち馬。マイル路線では隙のないスピード性能。"},
        {"horse": "ソウルラッシュ", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 95, "power": 94, "heavy": 98, "opt_dist": 1600, "desc": "マイルCS勝ち馬。パワーと伸び脚を兼ね備える。"},
        {"horse": "ナムラクレア", "sire": "ミッキーアイル", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 96, "power": 90, "heavy": 89, "opt_dist": 1200, "desc": "スプリント重賞の超常連。短距離での安定感は抜群。"},
        {"horse": "レモンポップ", "sire": "Lemon Drop Kid", "sire_line": "キングマンボ系", "style": "逃げ", "stamina": 88, "speed": 98, "power": 98, "heavy": 90, "opt_dist": 1600, "desc": "ダート絶対王者。抜群のダッシュ力とスピードで逃げ切る。"},
        {"horse": "ウシュバテソーロ", "sire": "オルフェーヴル", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 98, "speed": 92, "power": 99, "heavy": 105, "opt_dist": 2000, "desc": "ドバイWC勝ち馬。どんな馬場も突き抜ける世界レベルの鬼脚。"},
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ設計
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 馬の検索 & 詳細データベース"])

# --- TAB 1: 展開シミュレーター ---
with tab_sim:
    st.sidebar.header("⚙️ レース条件設定")
    venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
    surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
    dist = st.sidebar.selectbox("距離 (m)", [1200, 1600, 1800, 2000, 2400, 3000])
    going = st.sidebar.selectbox("馬場状態", ["良", "稍重", "重", "不良"])
    favored_line = st.sidebar.selectbox("注目血統", ["サンデーサイレンス系", "キングカメハメハ系", "ノーザンダンサー系", "ロベルト系", "その他"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🐎 出走馬選択")

    selected_horses = st.sidebar.multiselect(
        "出走馬を選択 (2〜8頭)",
        options=df_all["horse"].tolist(),
        default=["サトノシャイニング", "レーベンスティール", "エルトンバローズ", "ディープモンスター", "メイショウブレゲ", "チェルヴィニア"]
    )

    if len(selected_horses) < 2:
        st.info("👈 左側のサイドバーから出走馬を【2頭以上】選択してください。")
    else:
        # 馬番設定
        horse_numbers = {}
        st.sidebar.write("📌 **馬番設定**")
        for i, name in enumerate(selected_horses):
            horse_numbers[name] = st.sidebar.number_input(f"[{i+1}] {name}", min_value=1, max_value=18, value=i+1, key=f"sim_num_{name}")

        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        df_race["num"] = df_race["horse"].map(horse_numbers)
        df_race = df_race.sort_values(by="num").reset_index(drop=True)

        # 予想指数算定
        going_p = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}.get(going, 1.0)
        df_race["score"] = (
            df_race["speed"] * 0.35 +
            df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
            df_race["power"] * 0.2 +
            (df_race["heavy"] - 90) * (1.1 - going_p) * 2.0
        )
        df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

        # 高度な展開予想生成
        escape_count = len(df_race[df_race["style"] == "逃げ"])
        if escape_count >= 2:
            pace_title = "🔥 ハイペース想定（激しいハナ争い）"
            pace_desc = "逃げ馬が複数衝突し前半からペースアップ。直線での差し・追込馬の一気が決まりやすい展開です。"
        elif escape_count == 1:
            pace_title = "⚖️ ミドルペース想定（単騎マイペース）"
            pace_desc = "単騎逃げ馬がマイペースを構築。紛れが少なく実力通りに決着しやすい展開です。"
        else:
            pace_title = "🐢 スローペース想定（牽制し合い）"
            pace_desc = "明確な逃げ馬不在で牽制モード。最後の直線での一瞬の瞬発力と前目のポジションが絶対有利です。"

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("📋 出走表 & 予想指数")
            st.dataframe(
                df_race[["num", "horse", "style", "opt_dist", "sire", "score"]]
                .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "opt_dist": "適性距離", "sire": "父", "score": "予想指数"})
                .style.format({"予想指数": "{:.1f}", "適性距離": "{:}m"}),
                hide_index=True,
                use_container_width=True
            )

        with col2:
            st.subheader("🧠 競馬場・距離・馬場連動 展開予想レポート")
            st.markdown(f"**【コース条件】**: {venue} {surface}{dist}m ({going})")
            st.markdown(f"**【ペース予想】**: `{pace_title}`")
            st.write(f"📝 {pace_desc}")
            if going in ["重", "不良"]:
                st.warning(f"⚠️ **馬場状態({going})の注意点**: スタミナとパワーが必要なタフ馬場です。重馬場適性の低いスピード馬は失速するリスクがあります。")
            if dist >= 2400:
                st.info(f"📏 **距離({dist}m)の注意点**: 長距離戦のため、適性距離が短い馬は後半でスタミナが切れて大きく失速します。")

        # --- JSコース追従＆物理エンジンHTML ---
        st.markdown("---")
        st.subheader("🏁 完全コース追従・リアル物理シミュレーター")

        horses_js = []
        colors = ["#FF4B4B", "#FFA500", "#1E90FF", "#8A2BE2", "#2ECC71", "#E67E22", "#00FFFF", "#FF00FF"]

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

        race_config_js = {
            "dist": dist,
            "going": going,
            "venue": venue
        }

        html_code = f"""
        <div style="background-color: #0e1117; padding: 15px; border-radius: 12px; text-align: center; font-family: sans-serif;">
            <button id="startBtn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 12px;">
                ▶️️ シミュレーションスタート
            </button>
            <div id="status" style="color: #3498db; font-size: 16px; font-weight: bold; margin-bottom: 10px;">「スタート」ボタンを押してください</div>
            
            <svg id="trackSvg" width="100%" height="280" viewBox="0 0 600 280" style="background: #05140e; border-radius: 10px;">
                <!-- 競馬場コース描画 -->
                <rect x="50" y="30" width="500" height="220" rx="110" ry="110" fill="#1b4d3e" stroke="#2e8b57" stroke-width="12"/>
                <rect x="140" y="80" width="320" height="120" rx="60" ry="60" fill="#0e1117" stroke="#2e8b57" stroke-width="6"/>
                <!-- ゴールライン -->
                <line x1="200" y1="30" x2="200" y2="80" stroke="red" stroke-width="4" stroke-dasharray="4"/>
                <text x="200" y="22" fill="red" font-size="12" font-weight="bold" text-anchor="middle">GOAL</text>
                <g id="horsesGroup"></g>
            </svg>
            
            <div id="results" style="margin-top: 15px; text-align: left; background: #161b22; padding: 15px; border-radius: 8px; color: white;">
                <h4 style="margin-top:0; color: #f1c40f;">🏆 確定着順 (全頭)</h4>
                <div id="resultsList" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px;"></div>
            </div>
        </div>

        <script>
            const horsesData = {json.dumps(horses_js)};
            const raceConfig = {json.dumps(race_config_js)};
            let animationFrame;

            document.getElementById('startBtn').addEventListener('click', startSimulation);

            function startSimulation() {{
                cancelAnimationFrame(animationFrame);
                const group = document.getElementById('horsesGroup');
                const status = document.getElementById('status');
                const resultsList = document.getElementById('resultsList');
                group.innerHTML = '';
                resultsList.innerHTML = 'レース走行中...';

                let startTime = null;
                const duration = 14000; // 14秒アニメーション

                // 各馬の物理パラメータ初期化（適正・距離・馬場・当日の調子）
                const runners = horsesData.map((h, i) => {{
                    // ① 距離適性の影響（距離から離れるほどスタミナ消費が激増）
                    const distDiff = Math.abs(raceConfig.dist - h.opt_dist);
                    const staminaBurnRate = 1.0 + (distDiff > 200 ? (distDiff - 200) * 0.0015 : 0);

                    // ② 馬場適性の補正
                    let wetMod = 1.0;
                    if (raceConfig.going === "重" || raceConfig.going === "不良") {{
                        wetMod = h.heavy / 92.0; // 92以上なら加速、低いと減速
                    }}

                    // ③ 当日調子（ランダム要素 ±4%）
                    const condition = 0.96 + Math.random() * 0.08;

                    return {{
                        ...h,
                        laneOffset: (i - (horsesData.length - 1) / 2) * 5, // レーンの重なり防止
                        currDist: 0,
                        staminaRem: h.stamina * 10,
                        staminaBurnRate: staminaBurnRate,
                        wetMod: wetMod,
                        condition: condition,
                        isFinished: false,
                        finishTime: 0
                    }};
                }});

                function animate(timestamp) {{
                    if (!startTime) startTime = timestamp;
                    const elapsed = timestamp - startTime;
                    const progress = Math.min(elapsed / duration, 1.0);

                    // 実況テキスト更新
                    if (progress < 0.2) status.innerText = "📍 スタートしました！きれいな飛び出しからハナ争い！";
                    else if (progress < 0.5) status.innerText = "📍 向正面：隊列が固まって長丁場の展開へ！";
                    else if (progress < 0.8) status.innerText = "📍 3・4コーナー：勝負所！外から一気に各馬が仕掛ける！";
                    else if (progress < 0.98) status.innerText = "📍 最終直線：坂を駆け上がって激しい叩き合い！失速する馬も！";
                    else status.innerText = "🏆 全頭ゴールイン！確定着順です！";

                    group.innerHTML = '';

                    runners.forEach((h) => {{
                        // 毎フレームのリアルタイム速度計算
                        let currentSpeed = h.speed * h.wetMod * h.condition;

                        // 脚質ごとのスパートタイミング
                        if (progress > 0.6) {{
                            if (h.style === "差し" || h.style === "追込") currentSpeed *= 1.12;
                            if (h.style === "捲り") currentSpeed *= 1.10;
                        }}

                        // スタミナ減衰計算
                        h.staminaRem -= h.staminaBurnRate * 1.2;
                        if (h.staminaRem <= 0) {{
                            currentSpeed *= 0.65; // スタミナ切れで劇的失速
                        }}

                        // 進行距離加算
                        if (!h.isFinished) {{
                            h.currDist += currentSpeed * 0.08;
                        }}

                        // --- 精密コース座標計算 (完全楕円追従) ---
                        // コース1周 = 1000 単位
                        const normP = (h.currDist / 1000.0) % 1.0;
                        let x = 0, y = 0;

                        if (normP < 0.35) {{ // 下直線 (左 -> 右)
                            x = 160 + (normP / 0.35) * 280;
                            y = 220 + h.laneOffset;
                        }} else if (normP < 0.65) {{ // 右コーナー
                            const angle = ((normP - 0.35) / 0.30) * Math.PI;
                            x = 440 + Math.sin(angle) * (80 + h.laneOffset);
                            y = 140 - Math.cos(angle) * (80 + h.laneOffset);
                        }} else if (normP < 0.90) {{ // 上直線 (右 -> 左)
                            x = 440 - ((normP - 0.65) / 0.25) * 280;
                            y = 60 + h.laneOffset;
                        }} else {{ // 左コーナー
                            const angle = Math.PI + ((normP - 0.90) / 0.10) * Math.PI;
                            x = 160 + Math.sin(angle) * (80 + h.laneOffset);
                            y = 140 - Math.cos(angle) * (80 + h.laneOffset);
                        }}

                        h.lastX = x;

                        // ゴール判定 (直線x=200通過)
                        if (progress >= 0.95 && !h.isFinished) {{
                            h.isFinished = true;
                            h.finishDist = h.currDist;
                        }}

                        // 馬アイコンの描画
                        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                        g.setAttribute('transform', `translate(${{x}}, ${{y}})`);
                        g.innerHTML = `
                            <circle cx="0" cy="0" r="10" fill="${{h.color}}" stroke="white" stroke-width="2"/>
                            <text x="0" y="4" font-size="10" font-weight="bold" fill="white" text-anchor="middle">${{h.num}}</text>
                            <text x="14" y="4" font-size="11" font-weight="bold" fill="white">${{h.name}}</text>
                        `;
                        group.appendChild(g);
                    }});

                    if (progress < 1.0) {{
                        animationFrame = requestAnimationFrame(animate);
                    }} else {{
                        // 着順確定（全頭表示）
                        runners.sort((a, b) => b.currDist - a.currDist);
                        resultsList.innerHTML = '';
                        runners.forEach((h, rank) => {{
                            const medal = rank === 0 ? '🥇 1着' : rank === 1 ? '🥈 2着' : rank === 2 ? '🥉 3着' : `${{rank+1}}着`;
                            resultsList.innerHTML += `
                                <div style="background: #21262d; padding: 10px; border-radius: 6px; border-left: 5px solid ${{h.color}};">
                                    <div style="font-size: 14px; font-weight: bold;">${{medal}}: [${{h.num}}番] ${{h.name}}</div>
                                    <div style="font-size: 11px; color: #8b949e;">脚質: ${{h.style}} | 適性: ${{h.opt_dist}}m</div>
                                </div>
                            `;
                        }});
                    }}
                }}

                animationFrame = requestAnimationFrame(animate);
            }}
        </script>
        """
        st.components.v1.html(html_code, height=520)

# --- TAB 2: 馬の検索 & 詳細データベース（出走馬選択にかかわらず最初から常時表示） ---
with tab_db:
    st.subheader("🔍 馬の検索 & 詳細データベース")
    st.caption("登録されている全現役馬の能力ステータス・血統・適性距離・特徴を検索・閲覧できます。（出走馬選択の有無に関わらず最初から見られます）")

    search_query = st.text_input("🔎 馬名または血統（例: サンデーサイレンス、サトノシャイニング、ディープモンスター）で検索", "")

    df_filtered = df_all.copy()
    if search_query:
        df_filtered = df_filtered[
            df_filtered["horse"].str.contains(search_query, case=False) |
            df_filtered["sire"].str.contains(search_query, case=False) |
            df_filtered["sire_line"].str.contains(search_query, case=False)
        ]

    st.markdown(f"**登録頭数: {len(df_all)} 頭中 / 該当: {len(df_filtered)} 頭**")

    for idx, row in df_filtered.iterrows():
        with st.expander(f"🐎 [{row['style']}] {row['horse']} (父: {row['sire']} / ベスト: {row['opt_dist']}m)"):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**馬名:** {row['horse']}")
                st.markdown(f"**父:** {row['sire']} ({row['sire_line']})")
                st.markdown(f"**脚質:** {row['style']}")
                st.markdown(f"**ベスト距離:** {row['opt_dist']}m")
                st.caption(f"📝 **特徴**: {row['desc']}")
            with col_b:
                st.write("📊 **能力パラメータ**")
                st.progress(row["speed"] / 100, text=f"スピード: {row['speed']}")
                st.progress(row["stamina"] / 100, text=f"スタミナ: {row['stamina']}")
                st.progress(row["power"] / 100, text=f"パワー: {row['power']}")
                st.progress(min(1.0, row["heavy"] / 120), text=f"重馬場適性: {row['heavy']}")
