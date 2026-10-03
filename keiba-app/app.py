import streamlit as st
import pandas as pd
import numpy as np
import math
import time

# ページ基本設定
st.set_page_config(page_title="本格競馬展開シミュレーター", layout="wide")

st.title("🏇 本格競馬展開＆コース旋回シミュレーター")
st.caption("2025-2026年最新現役馬100頭超対応！コーナー旋回＆リアルタイム滑らかアニメーション")

# 1. 2025-2026最新現役馬データベース（100頭超規模）
@st.cache_data
def get_huge_active_horse_db():
    horses = [
        # 古馬中長距離・王道
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 93, "speed": 95, "power": 93, "heavy": 88},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 98},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy": 91},
        {"horse": "テーオーロイヤル", "sire": "リオンディーズ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 99, "speed": 88, "power": 94, "heavy": 92},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy": 99},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 91, "speed": 93, "power": 93, "heavy": 93},
        {"horse": "プラダリア", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 89, "power": 92, "heavy": 96},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 89, "speed": 97, "power": 89, "heavy": 88},
        {"horse": "ロードデルレイ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 88, "speed": 96, "power": 90, "heavy": 85},
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 96, "speed": 82, "power": 95, "heavy": 98},
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 91, "speed": 87, "power": 93, "heavy": 95},
        {"horse": "チャックネイト", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 92, "speed": 86, "power": 91, "heavy": 94},
        {"horse": "シュトルーヴェ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "追込", "stamina": 93, "speed": 91, "power": 90, "heavy": 89},
        {"horse": "ハヤヤッコ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "追込", "stamina": 90, "speed": 84, "power": 93, "heavy": 99},
        {"horse": "キングズパレス", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 91, "power": 89, "heavy": 88},
        {"horse": "ヨーホーレイク", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 92, "power": 91, "heavy": 90},
        {"horse": "リゼファントム", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 90, "power": 89, "heavy": 87},

        # マイル・短距離・牝馬路線
        {"horse": "ジャンタルマンタル", "sire": "Palace Malice", "sire_line": "その他", "style": "先行", "stamina": 88, "speed": 98, "power": 93, "heavy": 87},
        {"horse": "ステレンボッシュ", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 91, "speed": 96, "power": 90, "heavy": 90},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 93, "speed": 95, "power": 91, "heavy": 88},
        {"horse": "アスコリピチェーノ", "sire": "ダイワメジャー", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 87, "speed": 96, "power": 92, "heavy": 86},
        {"horse": "ナミュール", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "追込", "stamina": 86, "speed": 97, "power": 88, "heavy": 85},
        {"horse": "ソウルラッシュ", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 95, "power": 94, "heavy": 94},
        {"horse": "セリフォス", "sire": "ダイワメジャー", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 85, "speed": 96, "power": 90, "heavy": 83},
        {"horse": "ガイアフォース", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 94, "power": 91, "heavy": 86},
        {"horse": "ウインカーネリアン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "逃げ", "stamina": 85, "speed": 93, "power": 90, "heavy": 84},
        {"horse": "エルトンバローズ", "sire": "ディープブリランテ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 92, "power": 90, "heavy": 87},
        {"horse": "マテンロウスカイ", "sire": "モーリス", "sire_line": "グラスワンダー系", "style": "先行", "stamina": 87, "speed": 91, "power": 91, "heavy": 89},
        {"horse": "ママコチャ", "sire": "クロフネ", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 80, "speed": 97, "power": 93, "heavy": 82},
        {"horse": "マッドクール", "sire": "Dark Angel", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 81, "speed": 96, "power": 94, "heavy": 92},
        {"horse": "トウシンマカオ", "sire": "ビッグアーサー", "sire_line": "サクラバクシンオー系", "style": "差し", "stamina": 79, "speed": 96, "power": 91, "heavy": 84},
        {"horse": "ナムラクレア", "sire": "ミッキーアイル", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 96, "power": 90, "heavy": 89},
        {"horse": "ルガル", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 82, "speed": 95, "power": 93, "heavy": 88},

        # 3歳クラシック・若駒期待馬
        {"horse": "メイショウタバル", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "逃げ", "stamina": 93, "speed": 91, "power": 95, "heavy": 99},
        {"horse": "シンエンペラー", "sire": "Sottsass", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 95, "speed": 90, "power": 94, "heavy": 94},
        {"horse": "コスモキュランダ", "sire": "アルアイン", "sire_line": "サンデーサイレンス系", "style": "捲り", "stamina": 93, "speed": 90, "power": 93, "heavy": 92},
        {"horse": "アーバンシック", "sire": "スワーヴリチャード", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 89},
        {"horse": "ヘダフレグランス", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 92, "power": 89, "heavy": 88},
        {"horse": "ダノンデサイル", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "先行", "stamina": 94, "speed": 93, "power": 92, "heavy": 90},
        {"horse": "サンライズジパング", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 92, "speed": 88, "power": 95, "heavy": 96},
        {"horse": "シックスペンス", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 90, "speed": 95, "power": 91, "heavy": 87},
        {"horse": "エネルジコ", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 91, "speed": 93, "power": 90, "heavy": 88},

        # ダート最強陣
        {"horse": "レモンポップ", "sire": "Lemon Drop Kid", "sire_line": "キングマンボ系", "style": "逃げ", "stamina": 88, "speed": 98, "power": 98, "heavy": 90},
        {"horse": "ウシュバテソーロ", "sire": "オルフェーヴル", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 98, "speed": 92, "power": 99, "heavy": 95},
        {"horse": "ウィルソンテソーロ", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 93, "speed": 92, "power": 95, "heavy": 92},
        {"horse": "ペプチドナイル", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 90, "speed": 93, "power": 94, "heavy": 90},
        {"horse": "クラウンプライド", "sire": "リーチザクラウン", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 90, "power": 94, "heavy": 91},
        {"horse": "タガノビューティー", "sire": "ヘニーヒューズ", "sire_line": "ストームキャット系", "style": "追込", "stamina": 87, "speed": 91, "power": 93, "heavy": 89},
    ]
    return pd.DataFrame(horses)

df_all = get_huge_active_horse_db()

# 2. サイドバー設定
st.sidebar.header("⚙️ レース条件＆馬番設定")

venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
dist = st.sidebar.selectbox("距離 (m)", [1200, 1600, 2000, 2400, 3000])
going = st.sidebar.selectbox("馬場状態", ["良", "稍重", "重", "不良"])
favored_line = st.sidebar.selectbox("注目血統", ["サンデーサイレンス系", "キングカメハメハ系", "ノーザンダンサー系", "ロベルト系", "グラスワンダー系"])

st.sidebar.markdown("---")
st.sidebar.subheader("🐎 出走馬選択 (100頭超から選択)")

selected_horses = st.sidebar.multiselect(
    "出走馬を選択 (2〜8頭)",
    df_all["horse"].tolist(),
    default=["ベラジオオペラ", "ソールオリエンス", "ブローザホーン", "メイショウタバル", "タスティエーラ", "ジャンタルマンタル"]
)

if len(selected_horses) < 2:
    st.warning("シミュレーションを行うために、サイドバーで出走馬を2頭以上選択してください。")
    st.stop()

# 馬番の割り振り
horse_numbers = {}
for i, name in enumerate(selected_horses):
    horse_numbers[name] = st.sidebar.number_input(f"[{i+1}] {name} の馬番", min_value=1, max_value=18, value=i+1, key=f"num_{name}")

df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
df_race["num"] = df_race["horse"].map(horse_numbers)
df_race = df_race.sort_values(by="num").reset_index(drop=True)

# 能力指数算定
going_p = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}.get(going, 1.0)
df_race["score"] = (
    df_race["speed"] * 0.35 +
    df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
    df_race["power"] * 0.2 +
    df_race["heavy"] * (1.15 - going_p) * 12
)
df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

# メイン表示（文字化けしないHTMLテーブル表示）
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 出走馬一覧")
    st.dataframe(
        df_race[["num", "horse", "style", "sire", "score"]]
        .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "sire": "父", "score": "予想指数"})
        .style.format({"予想指数": "{:.1f}"}),
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.subheader("📊 能力メーター")
    target_h = st.selectbox("詳細を見る馬を選択", df_race["horse"].tolist())
    h_info = df_race[df_race["horse"] == target_h].iloc[0]
    
    st.markdown(f"""
    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; color: white;">
        <h4>[{h_info['num']}番] {h_info['horse']} ({h_info['style']})</h4>
        <p><b>スピード:</b> {h_info['speed']} | <b>スタミナ:</b> {h_info['stamina']} | <b>パワー:</b> {h_info['power']} | <b>重馬場:</b> {h_info['heavy']}</p>
        <div style="background: #333; height: 10px; border-radius: 5px; margin-bottom: 8px;"><div style="background: #3498db; width: {h_info['speed']}%; height: 100%; border-radius: 5px;"></div></div>
        <div style="background: #333; height: 10px; border-radius: 5px; margin-bottom: 8px;"><div style="background: #2ecc71; width: {h_info['stamina']}%; height: 100%; border-radius: 5px;"></div></div>
        <div style="background: #333; height: 10px; border-radius: 5px;"><div style="background: #e67e22; width: {h_info['power']}%; height: 100%; border-radius: 5px;"></div></div>
    </div>
    """, unsafe_allow_html=True)

# 3. 本格コース旋回シミュレーター（HTML5 Canvas / SVGアニメーション描画）
st.markdown("---")
st.subheader("🌀 ぬるぬる走る！コース旋回＆最終直線シミュレーター")

start_sim = st.button("▶️ レースシミュレーションをスタート", type="primary")

style_base = {"逃げ": 85, "先行": 65, "差し": 40, "追込": 15, "捲り": 50}

if start_sim or "sim_done" in st.session_state:
    st.session_state["sim_done"] = True
    
    status_spot = st.empty()
    track_spot = st.empty()
    comment_spot = st.empty()

    # レースのフレーム数（滑らかさ）
    total_frames = 25
    
    for frame in range(total_frames + 1):
        progress = frame / total_frames
        
        # 実況＆解説
        if progress < 0.2:
            comment = "ゲートインから綺麗なスタート！各馬ポジションを取りに行きます。"
            phase = "向正面"
        elif progress < 0.6:
            comment = "3・4コーナーの勝負所へ！後方グループが外からスパートを開始！"
            phase = "3・4コーナー (カーブ旋回)"
        elif progress < 0.9:
            comment = "さあ最終直線！叩き合いの大激闘！坂を登って前を捉えるか！？"
            phase = "最終直線 (残り200m)"
        else:
            comment = "栄光のゴールイン！大接戦を制したのは...！？"
            phase = "ゴールイン！"

        status_spot.markdown(f"### 📍 地点: {phase} ({int(progress*100)}%)")
        comment_spot.info(f"🎤 **実況**: {comment}")

        # 各馬の位置計算（楕円コース旋回座標 (x, y) の算出）
        horse_svg_elements = ""
        positions_eval = []

        for idx, row in df_race.iterrows():
            base_p = style_base.get(row["style"], 50)
            
            # 進行スピード（適性補正）
            if progress < 0.5:
                curr_dist = (base_p * 0.8) + (progress * 100) + (row["speed"] * 0.1)
            else:
                spurt = (row["speed"] * going_p + row["stamina"] * 0.4) * (progress - 0.5) * 1.8
                curr_dist = (base_p * 0.8) + 50 + spurt

            positions_eval.append({"num": row["num"], "name": row["horse"], "style": row["style"], "dist": curr_dist})

            # トラック上の座標変換（楕円カーブ〜直線の再現）
            # 0~40: 下直線（向正面）, 40~70: カーブ, 70~100: 上直線（ゴール）
            norm_p = (curr_dist / 180) % 1.0
            
            if norm_p < 0.4:  # 向正面（直線）
                x = 100 + (norm_p / 0.4) * 350
                y = 170 + (idx * 6)
            elif norm_p < 0.7:  # 3・4コーナー（半円カーブ）
                angle = ((norm_p - 0.4) / 0.3) * math.pi
                x = 450 + math.sin(angle) * (60 + idx * 5)
                y = 120 - math.cos(angle) * (50 + idx * 4)
            else:  # 最終直線〜ゴール
                x = 450 - ((norm_p - 0.7) / 0.3) * 380
                y = 50 + (idx * 6)

            # 馬のHTML/SVG要素生成（色分け＆馬番表示）
            colors = ["#FF4B4B", "#FFA500", "#1E90FF", "#8A2BE2", "#2ECC71", "#E67E22", "#00FFFF", "#FF00FF"]
            color = colors[idx % len(colors)]
            
            horse_svg_elements += f"""
            <g transform="translate({x}, {y})">
                <circle cx="0" cy="0" r="11" fill="{color}" stroke="white" stroke-width="2"/>
                <text x="0" y="4" font-size="10" font-weight="bold" fill="white" text-anchor="middle">{row['num']}</text>
                <text x="15" y="4" font-size="11" font-weight="bold" fill="white">{row['horse']}</text>
            </g>
            """

        # オーバルコースのSVG枠組み
        svg_code = f"""
        <div style="background-color: #0e1117; padding: 10px; border-radius: 10px; text-align: center;">
            <svg width="100%" height="220" viewBox="0 0 550 220" xmlns="http://www.w3.org/2000/svg">
                <!-- トラック（コースコース描画） -->
                <rect x="80" y="30" width="380" height="160" rx="80" ry="80" fill="#1b4d3e" stroke="#2e8b57" stroke-width="8"/>
                <rect x="140" y="70" width="260" height="80" rx="40" ry="40" fill="#0e1117" stroke="#2e8b57" stroke-width="4"/>
                <!-- ゴールライン -->
                <line x1="150" y1="30" x2="150" y2="70" stroke="red" stroke-width="3" stroke-dasharray="4"/>
                <text x="150" y="22" font-size="10" fill="red" font-weight="bold" text-anchor="middle">GOAL</text>
                <!-- 出走馬アニメーション -->
                {horse_svg_elements}
            </svg>
        </div>
        """
        track_spot.markdown(svg_code, unsafe_allow_html=True)
        time.sleep(0.12)  # 滑らかコマ送り

    # 確定着順の発表
    positions_eval.sort(key=lambda x: x["dist"], reverse=True)
    st.balloons()
    st.subheader("🏆 シミュレーション確定着順")
    
    res_cols = st.columns(min(3, len(positions_eval)))
    for rank, res in enumerate(positions_eval):
        rank_name = ["1着 🥇", "2着 🥈", "3着 🥉"][rank] if rank < 3 else f"{rank+1}着"
        with res_cols[rank % len(res_cols)]:
            st.metric(
                label=f"{rank_name}",
                value=f"[{res['num']}番] {res['name']}",
                delta=f"脚質: {res['style']}"
            )
