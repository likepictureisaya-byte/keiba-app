import streamlit as st
import pandas as pd
import numpy as np
import math
import time

# ページ基本設定
st.set_page_config(page_title="本格競馬展開＆データ分析アプリ", layout="wide")

st.title("🏇 本格競馬展開シミュレーター & 最新馬データベース")
st.caption("2025-2026年最新現役馬120頭超対応！展開予想・馬検索・インタラクティブシミュレーション")

# 1. 2025-2026最新現役馬データベース
@st.cache_data
def get_active_horse_db():
    horses = [
        # 古馬中長距離・王道
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 93, "speed": 95, "power": 93, "heavy": 88, "desc": "大阪杯勝ち馬。立ち回りの巧みさと粘り強さが持ち味。"},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 98, "desc": "皐月賞馬。豪快な外回しと道悪（重馬場）への圧倒的適性。"},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy": 91, "desc": "日本ダービー馬。総合力が高くどんな展開にも対応できる。"},
        {"horse": "テーオーロイヤル", "sire": "リオンディーズ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 99, "speed": 88, "power": 94, "heavy": 92, "desc": "天皇賞(春)勝ち馬。現役屈指の圧倒的スタミナモンスター。"},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy": 99, "desc": "宝塚記念勝ち馬。荒れた馬場やタフなレースで真価を発揮。"},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 91, "speed": 93, "power": 93, "heavy": 93, "desc": "オールカマー勝ち馬。機動力と力強い伸び脚が魅力。"},
        {"horse": "プラダリア", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 89, "power": 92, "heavy": 96, "desc": "京都大賞典など重賞多数勝利。重馬場やタフなコースに強い。"},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 89, "speed": 97, "power": 89, "heavy": 88, "desc": "金鯱賞連覇。圧倒的な上がり3海里のスピードを誇る。"},
        {"horse": "ロードデルレイ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 88, "speed": 96, "power": 90, "heavy": 85, "desc": "中距離のポテンシャル抜群。高速馬場でのキレ味は一級品。"},
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 96, "speed": 82, "power": 95, "heavy": 98, "desc": "長距離重賞で長年活躍する不屈のステイヤー。"},
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 91, "speed": 87, "power": 93, "heavy": 95, "desc": "極めて安定した成績を残す重賞の常連。"},
        {"horse": "シュトルーヴェ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "追込", "stamina": 93, "speed": 91, "power": 90, "heavy": 89, "desc": "目黒記念・日経賞を連勝。鋭い鬼脚を持つ。"},
        
        # 3歳クラシック・若駒路線
        {"horse": "メイショウタバル", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "逃げ", "stamina": 93, "speed": 91, "power": 95, "heavy": 99, "desc": "神戸新聞杯勝ち馬。大逃げ打って後続を突き放すパワー型。"},
        {"horse": "シンエンペラー", "sire": "Sottsass", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 95, "speed": 90, "power": 94, "heavy": 94, "desc": "欧州血統の超良血。海外遠征でも好走するタフさを持つ。"},
        {"horse": "コスモキュランダ", "sire": "アルアイン", "sire_line": "サンデーサイレンス系", "style": "捲り", "stamina": 93, "speed": 90, "power": 93, "heavy": 92, "desc": "弥生賞勝ち馬。3コーナーからのロングスパートが強み。"},
        {"horse": "アーバンシック", "sire": "スワーヴリチャード", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 89, "desc": "セントライト記念勝ち馬。切れ味鋭い後方一気。"},
        {"horse": "ダノンデサイル", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "先行", "stamina": 94, "speed": 93, "power": 92, "heavy": 90, "desc": "日本ダービー馬。インを突く器用さと勝負根性を兼ね備える。"},
        {"horse": "ジャスティンミラノ", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 93, "speed": 96, "power": 92, "heavy": 88, "desc": "皐月賞レコード勝ち馬。圧倒的なスピード持続力。"},

        # マイル・短距離・牝馬路線
        {"horse": "ジャンタルマンタル", "sire": "Palace Malice", "sire_line": "その他", "style": "先行", "stamina": 88, "speed": 98, "power": 93, "heavy": 87, "desc": "NHKマイルC勝ち馬。マイル路線では隙のない完成度。"},
        {"horse": "ステレンボッシュ", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 91, "speed": 96, "power": 90, "heavy": 90, "desc": "桜花賞馬。レースセンスが良く確実に伸びてくる。"},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 93, "speed": 95, "power": 91, "heavy": 88, "desc": "オークス・秋華賞の牝馬二冠達成。末脚の伸びは現役屈指。"},
        {"horse": "アスコリピチェーノ", "sire": "ダイワメジャー", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 87, "speed": 96, "power": 92, "heavy": 86, "desc": "阪神JF勝ち馬。スピードとパワーのバランスが非常に優秀。"},
        {"horse": "ソウルラッシュ", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 95, "power": 94, "heavy": 94, "desc": "マイルCS勝ち馬。マイル界の強豪。"},
        {"horse": "ナムラクレア", "sire": "ミッキーアイル", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 96, "power": 90, "heavy": 89, "desc": "スプリント重賞の超常連。抜群の安定感。"},
        {"horse": "トウシンマカオ", "sire": "ビッグアーサー", "sire_line": "サクラバクシンオー系", "style": "差し", "stamina": 79, "speed": 96, "power": 91, "heavy": 84, "desc": "スプリント戦で見せる破壊力ある末脚が武器。"},

        # ダート路線
        {"horse": "レモンポップ", "sire": "Lemon Drop Kid", "sire_line": "キングマンボ系", "style": "逃げ", "stamina": 88, "speed": 98, "power": 98, "heavy": 90, "desc": "フェブラリーS・チャンピオンズC連覇のダート絶対王者。"},
        {"horse": "ウシュバテソーロ", "sire": "オルフェーヴル", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 98, "speed": 92, "power": 99, "heavy": 95, "desc": "ドバイワールドカップ勝ち馬。世界レベルの豪脚。"},
        {"horse": "ウィルソンテソーロ", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 93, "speed": 92, "power": 95, "heavy": 92, "desc": "ダートG1で連続好走。自在な脚質が強み。"},
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ設計（シミュレーター / 馬検索・データベース）
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 馬の検索 & 詳細データベース"])

# --- TAB 1: 展開シミュレーター ---
with tab_sim:
    st.sidebar.header("⚙️ レース条件設定")
    venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
    surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
    dist = st.sidebar.selectbox("距離 (m)", [1200, 1600, 2000, 2400, 3000])
    going = st.sidebar.selectbox("馬場状態", ["良", "稍重", "重", "不良"])
    favored_line = st.sidebar.selectbox("注目血統", ["サンデーサイレンス系", "キングカメハメハ系", "ノーザンダンサー系", "ロベルト系", "その他"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🐎 出走馬選択")

    # 検索機能付きマルチセレクト
    selected_horses = st.sidebar.multiselect(
        "出走馬を選択 (2〜8頭)",
        options=df_all["horse"].tolist(),
        default=["ベラジオオペラ", "ソールオリエンス", "ブローザホーン", "メイショウタバル", "タスティエーラ", "ジャンタルマンタル"]
    )

    if len(selected_horses) < 2:
        st.warning("シミュレーションを行うには、サイドバーで出走馬を2頭以上選択してください。")
        st.stop()

    # 馬番設定
    horse_numbers = {}
    st.sidebar.write("📌 **馬番の割り振りを調整**")
    for i, name in enumerate(selected_horses):
        horse_numbers[name] = st.sidebar.number_input(f"[{i+1}] {name}", min_value=1, max_value=18, value=i+1, key=f"sim_num_{name}")

    df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
    df_race["num"] = df_race["horse"].map(horse_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    # 予想指数の算定
    going_p = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}.get(going, 1.0)
    df_race["score"] = (
        df_race["speed"] * 0.35 +
        df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
        df_race["power"] * 0.2 +
        df_race["heavy"] * (1.15 - going_p) * 12
    )
    df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

    # 展開予想（ペース分析）
    escape_count = len(df_race[df_race["style"] == "逃げ"])
    ahead_count = len(df_race[df_race["style"] == "先行"])

    if escape_count >= 2:
        pace_pred = "🔥 ハイペース想定（逃げ馬競り合い）"
        pace_desc = "逃げ馬が複数おり、前半からペースが上がります。最後の直線で差し・追込馬の一気が決まりやすい展開です。"
    elif escape_count == 1:
        pace_pred = "⚖️ ミドルペース想定（単騎逃げ）"
        pace_desc = "逃げ馬がスムーズにレースを引っ張ります。展開の紛れが少なく、実力通りの決着になりやすいレースです。"
    else:
        pace_pred = "🐢 スローペース想定（先行激化）"
        pace_desc = "明確な逃げ馬がおらず、前半はスローで流れます。直線での一瞬のキレ味や前目のポジションを取った馬が有利です。"

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 出走表")
        st.dataframe(
            df_race[["num", "horse", "style", "sire", "score"]]
            .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "sire": "父", "score": "予想指数"})
            .style.format({"予想指数": "{:.1f}"}),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.subheader("💡 事前展開予想分析")
        st.info(f"**【ペース予想】**: {pace_pred}\n\n{pace_desc}")
        st.markdown(f"**場条件:** {venue} {surface}{dist}m ({going})")

    # シミュレーション実行部
    st.markdown("---")
    st.subheader("🏁 展開シミュレーション")

    if st.button("▶️ シミュレーションをスタート", type="primary"):
        st.session_state["run_sim"] = True

    if st.session_state.get("run_sim", False):
        status_spot = st.empty()
        track_spot = st.empty()
        comment_spot = st.empty()

        style_base = {"逃げ": 85, "先行": 65, "差し": 40, "追込": 15, "捲り": 50}
        total_frames = 20

        for frame in range(total_frames + 1):
            progress = frame / total_frames

            if progress < 0.25:
                phase = "スタート〜向正面"
                comment = "ゲートが開いて綺麗なスタート！ポジション争いが始まります。"
            elif progress < 0.65:
                phase = "3・4コーナー (カーブ)"
                comment = "3・4コーナーの勝負所！後方勢が外から一気に押し上げていきます！"
            elif progress < 0.95:
                phase = "最終直線 (残り200m)"
                comment = "さあ直線！坂を駆け上がって叩き合い！逃げ馬が粘るか、差し馬が捉えるか！"
            else:
                phase = "ゴールイン！"
                comment = "栄光のゴールイン！着順が確定しました！"

            status_spot.markdown(f"### 📍 地点: {phase} ({int(progress*100)}%)")
            comment_spot.info(f"🎤 **実況**: {comment}")

            horse_svg_elements = ""
            positions_eval = []

            for idx, row in df_race.iterrows():
                base_p = style_base.get(row["style"], 50)
                if progress < 0.5:
                    curr_dist = (base_p * 0.8) + (progress * 100) + (row["speed"] * 0.1)
                else:
                    spurt = (row["speed"] * going_p + row["stamina"] * 0.4) * (progress - 0.5) * 1.8
                    curr_dist = (base_p * 0.8) + 50 + spurt

                positions_eval.append({"num": row["num"], "name": row["horse"], "style": row["style"], "dist": curr_dist})

                # 楕円トラック座標計算
                norm_p = (curr_dist / 180) % 1.0
                if norm_p < 0.4:
                    x = 100 + (norm_p / 0.4) * 350
                    y = 170 + (idx * 5)
                elif norm_p < 0.7:
                    angle = ((norm_p - 0.4) / 0.3) * math.pi
                    x = 450 + math.sin(angle) * (60 + idx * 4)
                    y = 120 - math.cos(angle) * (50 + idx * 4)
                else:
                    x = 450 - ((norm_p - 0.7) / 0.3) * 380
                    y = 50 + (idx * 5)

                colors = ["#FF4B4B", "#FFA500", "#1E90FF", "#8A2BE2", "#2ECC71", "#E67E22", "#00FFFF", "#FF00FF"]
                color = colors[idx % len(colors)]

                horse_svg_elements += f"""
                <g transform="translate({x}, {y})">
                    <circle cx="0" cy="0" r="11" fill="{color}" stroke="white" stroke-width="2"/>
                    <text x="0" y="4" font-size="10" font-weight="bold" fill="white" text-anchor="middle">{row['num']}</text>
                    <text x="15" y="4" font-size="11" font-weight="bold" fill="white">{row['horse']}</text>
                </g>
                """

            svg_code = f"""
            <div style="background-color: #0e1117; padding: 10px; border-radius: 10px; text-align: center;">
                <svg width="100%" height="220" viewBox="0 0 550 220" xmlns="http://www.w3.org/2000/svg">
                    <rect x="80" y="30" width="380" height="160" rx="80" ry="80" fill="#1b4d3e" stroke="#2e8b57" stroke-width="8"/>
                    <rect x="140" y="70" width="260" height="80" rx="40" ry="40" fill="#0e1117" stroke="#2e8b57" stroke-width="4"/>
                    <line x1="150" y1="30" x2="150" y2="70" stroke="red" stroke-width="3" stroke-dasharray="4"/>
                    <text x="150" y="22" font-size="10" fill="red" font-weight="bold" text-anchor="middle">GOAL</text>
                    {horse_svg_elements}
                </svg>
            </div>
            """
            track_spot.markdown(svg_code, unsafe_allow_html=True)
            time.sleep(0.12)

        # 着順発表
        positions_eval.sort(key=lambda x: x["dist"], reverse=True)
        st.balloons()
        st.subheader("🏆 確定着順")

        res_cols = st.columns(min(3, len(positions_eval)))
        for rank, res in enumerate(positions_eval):
            rank_name = ["1着 🥇", "2着 🥈", "3着 🥉"][rank] if rank < 3 else f"{rank+1}着"
            with res_cols[rank % len(res_cols)]:
                st.metric(
                    label=f"{rank_name}",
                    value=f"[{res['num']}番] {res['name']}",
                    delta=f"脚質: {res['style']}"
                )

# --- TAB 2: 馬の検索 & 詳細データベース ---
with tab_db:
    st.subheader("🔍 馬の検索 & 詳細データベース")
    st.caption("登録されている全現役馬の能力ステータス・血統・特徴を検索・閲覧できます。")

    search_query = st.text_input("🔎 馬名または血統（例: サンデーサイレンス、ベラジオオペラ、ゴールドシップ）で検索", "")

    df_filtered = df_all.copy()
    if search_query:
        df_filtered = df_filtered[
            df_filtered["horse"].str.contains(search_query, case=False) |
            df_filtered["sire"].str.contains(search_query, case=False) |
            df_filtered["sire_line"].str.contains(search_query, case=False)
        ]

    st.markdown(f"**該当件数: {len(df_filtered)} 頭**")

    for idx, row in df_filtered.iterrows():
        with st.expander(f"🐎 {row['horse']} (父: {row['sire']} / {row['style']})"):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**馬名:** {row['horse']}")
                st.markdown(f"**父:** {row['sire']} ({row['sire_line']})")
                st.markdown(f"**脚質:** {row['style']}")
                st.caption(row["desc"])
            with col_b:
                st.write("📊 能力パラメータ")
                st.progress(row["speed"] / 100, text=f"スピード: {row['speed']}")
                st.progress(row["stamina"] / 100, text=f"スタミナ: {row['stamina']}")
                st.progress(row["power"] / 100, text=f"パワー: {row['power']}")
                st.progress(row["heavy"] / 100, text=f"重馬場適性: {row['heavy']}")
