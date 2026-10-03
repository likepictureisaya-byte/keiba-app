import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time

# 日本語フォント設定（文字化け対策）
plt.rcParams['font.family'] = 'DejaVu Sans' # 標準フォント設定（英語・数値用）
plt.rcParams['axes.unicode_minus'] = False

# ページ基本設定
st.set_page_config(page_title="最新競馬展開＆レース予想シミュレーター", layout="wide")

st.title("🏇 最新競馬データ分析 & 展開シミュレーター")
st.caption("2025-2026年最新現役馬データ対応！馬番設定・着順判定・展開実況機能付き")

# 1. 最新現役馬データベース（2025-2026年中心）
@st.cache_data
def get_active_horse_data():
    horses_data = [
        # 現役古馬・中長距離主力
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 92, "speed": 95, "power": 93, "heavy_track": 88},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追い込み", "stamina": 93, "speed": 94, "power": 91, "heavy_track": 96},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy_track": 90},
        {"horse": "テーオーロイヤル", "sire": "リオンディーズ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 99, "speed": 88, "power": 94, "heavy_track": 92},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy_track": 99},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 90, "speed": 93, "power": 93, "heavy_track": 92},
        {"horse": "プラダリア", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 89, "power": 92, "heavy_track": 95},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 89, "speed": 97, "power": 89, "heavy_track": 88},
        {"horse": "ロードデルレイ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 87, "speed": 95, "power": 90, "heavy_track": 85},

        # 3歳・マイル・個性派現役馬
        {"horse": "ジャンタルマンタル", "sire": "Palace Malice", "sire_line": "その他", "style": "先行", "stamina": 88, "speed": 97, "power": 92, "heavy_track": 86},
        {"horse": "ステレンボッシュ", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 91, "speed": 95, "power": 90, "heavy_track": 89},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 93, "speed": 94, "power": 91, "heavy_track": 88},
        {"horse": "メイショウタバル", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "逃げ", "stamina": 92, "speed": 90, "power": 95, "heavy_track": 98},
        {"horse": "シンエンペラー", "sire": "Sottsass", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 95, "speed": 89, "power": 94, "heavy_track": 93},
        {"horse": "ガイアフォース", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 87, "speed": 93, "power": 91, "heavy_track": 85},
        {"horse": "ウインカーネリアン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "逃げ", "stamina": 85, "speed": 92, "power": 90, "heavy_track": 84},
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 91, "speed": 87, "power": 93, "heavy_track": 95},
        {"horse": "チャックネイト", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 92, "speed": 86, "power": 91, "heavy_track": 94},
    ]
    return pd.DataFrame(horses_data)

df_all = get_active_horse_data()

# サイドバー: レース条件
st.sidebar.header("⚙️ レース条件設定")

venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
dist = st.sidebar.selectbox("距離 (m)", [1600, 2000, 2400, 2500, 3200])
weather = st.sidebar.selectbox("予想天気", ["晴", "曇", "小雨", "雨"])
going = st.sidebar.selectbox("想定馬場状態", ["良", "稍重", "重", "不良"])
favored_line = st.sidebar.selectbox("注目血統", ["サンデーサイレンス系", "キングカメハメハ系", "ノーザンダンサー系", "ロベルト系", "グラスワンダー系"])

st.sidebar.markdown("---")
st.sidebar.subheader("🐎 出走馬 & 馬番設定")

selected_horses = st.sidebar.multiselect(
    "出走馬を選択 (2〜8頭)",
    df_all["horse"].tolist(),
    default=["ベラジオオペラ", "ソールオリエンス", "ブローザホーン", "メイショウタバル", "タスティエーラ", "ジャンタルマンタル"]
)

if len(selected_horses) < 2:
    st.warning("シミュレーションを行うために出走馬を2頭以上選択してください。")
    st.stop()

# 馬番の指定
horse_numbers = {}
st.sidebar.write("各馬の馬番を指定:")
for i, name in enumerate(selected_horses):
    horse_numbers[name] = st.sidebar.number_input(f"{name} の馬番", min_value=1, max_value=18, value=i+1, key=f"num_{name}")

df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
df_race["num"] = df_race["horse"].map(horse_numbers)
df_race = df_race.sort_values(by="num").reset_index(drop=True)

# 指数計算
going_penalty = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}
penalty = going_penalty.get(going, 1.0)

df_race["score"] = (
    df_race["speed"] * 0.35 +
    df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
    df_race["power"] * 0.2 +
    df_race["heavy_track"] * (1.15 - penalty) * 12
)
df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

# メイン表示
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 出走馬一覧（馬番順）")
    st.dataframe(
        df_race[["num", "horse", "style", "sire", "score"]]
        .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "sire": "父", "score": "予想指数"})
        .style.format({"予想指数": "{:.1f}"}),
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.subheader("📊 能力パラメーター比較")
    target_h = st.selectbox("詳細を見る馬を選択", df_race["horse"].tolist())
    h_info = df_race[df_race["horse"] == target_h].iloc[0]
    
    cats = ["Speed", "Stamina", "Power", "HeavyTrack"]
    vals = [h_info["speed"], h_info["stamina"], h_info["power"], h_info["heavy_track"]]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(cats, vals, color=["#3498db", "#2ecc71", "#e67e22", "#9b59b6"])
    ax.set_ylim(50, 100)
    ax.set_ylabel("Score")
    ax.set_title(f"[{h_info['num']}] {target_h}")
    st.pyplot(fig)

# 2. 展開シミュレーター
st.markdown("---")
st.subheader("🏁 展開シミュレーション & 着順結果")

start_sim = st.button("▶️ 展開シミュレーションをスタート", type="primary")

style_base = {"逃げ": 90, "先行": 70, "差し": 45, "追い込み": 20}

if start_sim or "sim_done" in st.session_state:
    st.session_state["sim_done"] = True
    progress_bar = st.progress(0)
    status_text = st.empty()
    plot_spot = st.empty()
    commentary_spot = st.empty()

    steps = [
        ("スタート直後", 0.1, "各馬綺麗なスタート！ダッシュを利かせてポジションを取りに行きます。"),
        ("向正面 (レース中盤)", 0.4, "隊列が決まりました。各馬折り合いをつけて勝負どころへ。"),
        ("3・4コーナー (勝負所)", 0.7, "4コーナー手前！後方待機組が外から一気に手応え良く進出！"),
        ("最終直線 (ゴール前)", 1.0, "さあ直線！残り200mの叩き合い！ゴールイン！")
    ]

    final_results = []

    for label, progress, comment in steps:
        progress_bar.progress(int(progress * 100))
        status_text.markdown(f"### 📍 地点: {label}")
        commentary_spot.info(f"🎤 **実況ログ**: {comment}")

        fig_sim, ax_sim = plt.subplots(figsize=(10, 4.5))
        positions = []

        for idx, row in df_race.iterrows():
            base_pos = style_base.get(row["style"], 50)
            if progress < 0.5:
                current_pos = base_pos * (progress * 2) + (row["speed"] * 0.1)
            else:
                stamina_factor = row["stamina"] if dist >= 2400 else 90
                spurt = (row["speed"] * penalty + stamina_factor * 0.4) * (progress - 0.4) * 2.2
                current_pos = base_pos + spurt
            
            positions.append({
                "num": row["num"],
                "name": row["horse"],
                "style": row["style"],
                "pos": current_pos
            })

        positions.sort(key=lambda x: x["pos"], reverse=True)
        final_results = positions

        # 描画
        for rank, p in enumerate(positions):
            y_pos = len(positions) - rank
            ax_sim.scatter(p["pos"], y_pos, s=300, zorder=3)
            # 馬番と名前をはっきり描画
            label_text = f" [{p['num']}] {p['name']} ({p['style']})"
            ax_sim.text(p["pos"] + 2, y_pos, label_text, fontsize=11, fontweight='bold', verticalalignment='center')

        ax_sim.set_xlim(0, 180)
        ax_sim.set_xlabel("進行位置 (右に行くほど優勢・右端がゴール)")
        ax_sim.axvline(x=150, color='red', linestyle='--', linewidth=2, label='GOAL')
        ax_sim.get_yaxis().set_visible(False)
        ax_sim.grid(True, linestyle=':', alpha=0.5)
        
        plot_spot.pyplot(fig_sim)
        time.sleep(1.0)

    # 確定着順の表示
    st.balloons()
    st.subheader("🏆 シミュレーション確定着順")
    
    res_cols = st.columns(min(3, len(final_results)))
    for rank, res in enumerate(final_results):
        rank_name = ["1着 🥇", "2着 🥈", "3着 🥉"][rank] if rank < 3 else f"{rank+1}着"
        with res_cols[rank % len(res_cols)]:
            st.metric(
                label=f"{rank_name}",
                value=f"[{res['num']}番] {res['name']}",
                delta=f"脚質: {res['style']}"
            )
