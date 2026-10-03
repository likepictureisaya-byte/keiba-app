import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ページ基本設定
st.set_page_config(page_title="競馬展開・レース予想シミュレーター", layout="wide")

st.title("🏇 競馬重賞データ分析 & 動く展開シミュレーター")
st.caption("2020年以降の重賞馬（G1/G2/G3）を網羅！コース・馬場・血統・展開による自動実況シミュレーション")

# 1. 重賞馬データベース（G1〜G3の多彩な名馬・重賞常連馬）
@st.cache_data
def get_extended_horse_data():
    horses_data = [
        # G1・王道主力馬
        {"horse": "イクイノックス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 95, "speed": 98, "power": 92, "heavy_track": 88},
        {"horse": "ドウデュース", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 92, "speed": 97, "power": 96, "heavy_track": 90},
        {"horse": "コントレイル", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 93, "speed": 97, "power": 88, "heavy_track": 80},
        {"horse": "アーモンドアイ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 90, "speed": 99, "power": 90, "heavy_track": 82},
        {"horse": "リバティアイランド", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 97, "power": 90, "heavy_track": 84},
        {"horse": "エフフォーリア", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "先行", "stamina": 94, "speed": 94, "power": 95, "heavy_track": 91},
        {"horse": "クロノジェネシス", "sire": "バゴ", "sire_line": "ナスルーラ系", "style": "差し", "stamina": 95, "speed": 91, "power": 96, "heavy_track": 99},

        # 個性派・逃げ馬（G1〜G3活躍馬）
        {"horse": "パンサラッサ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "逃げ", "stamina": 88, "speed": 95, "power": 90, "heavy_track": 92},
        {"horse": "ジャックドール", "sire": "モーリス", "sire_line": "グラスワンダー系", "style": "逃げ", "stamina": 87, "speed": 94, "power": 91, "heavy_track": 86},
        {"horse": "タイトルホルダー", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "逃げ", "stamina": 99, "speed": 88, "power": 97, "heavy_track": 96},
        {"horse": "ユニコーンライオン", "sire": "No Nay Never", "sire_line": "ノーザンダンサー系", "style": "逃げ", "stamina": 86, "speed": 86, "power": 88, "heavy_track": 89},
        {"horse": "アフリカンゴールド", "sire": "ステイゴールド", "sire_line": "サンデーサイレンス系", "style": "逃げ", "stamina": 88, "speed": 80, "power": 85, "heavy_track": 90},

        # 先行・粘り強さ（G2・G3含）
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 97, "speed": 83, "power": 95, "heavy_track": 98},
        {"horse": "ソーヴァリアント", "sire": "オルフェーヴル", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 86, "speed": 90, "power": 92, "heavy_track": 90},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 88, "speed": 96, "power": 88, "heavy_track": 87},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 90, "speed": 91, "power": 93, "heavy_track": 93},
        {"horse": "ソダシ", "sire": "クロフネ", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 83, "speed": 93, "power": 91, "heavy_track": 80},
        {"horse": "ウインマリリン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "先行", "stamina": 90, "speed": 88, "power": 89, "heavy_track": 91},

        # 差し・追い込み（強力な決め手）
        {"horse": "スターズオンアース", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "追い込み", "stamina": 93, "speed": 94, "power": 90, "heavy_track": 86},
        {"horse": "シャフリヤール", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 90, "speed": 95, "power": 86, "heavy_track": 78},
        {"horse": "ジャスティンパレス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 96, "speed": 92, "power": 89, "heavy_track": 85},
        {"horse": "ヴェラアズール", "sire": "エイシンフラッシュ", "sire_line": "キングカメハメハ系", "style": "追い込み", "stamina": 91, "speed": 94, "power": 88, "heavy_track": 84},
        {"horse": "ポタジェ", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 88, "speed": 87, "power": 90, "heavy_track": 88},
        {"horse": "ヒシイグアス", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 87, "speed": 90, "power": 91, "heavy_track": 89},

        # 重馬場・荒れた馬場の鬼
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 91, "speed": 86, "power": 93, "heavy_track": 95},
        {"horse": "カラテ", "sire": "トゥザグローリー", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 88, "speed": 85, "power": 94, "heavy_track": 97},
        {"horse": "メイショウハリマオ", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 85, "speed": 82, "power": 88, "heavy_track": 92},
    ]
    return pd.DataFrame(horses_data)

df_all = get_extended_horse_data()

# サイドバー: 条件設定
st.sidebar.header("⚙️ レース条件設定")

venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
dist = st.sidebar.selectbox("距離 (m)", [1600, 2000, 2400, 2500, 3200])
weather = st.sidebar.selectbox("予想天気", ["晴", "曇", "小雨", "雨"])
going = st.sidebar.selectbox("想定馬場状態", ["良", "稍重", "重", "不良"])

favored_line = st.sidebar.selectbox("注目の血統ライン", ["サンデーサイレンス系", "キングカメハメハ系", "グラスワンダー系", "ノーザンダンサー系", "ロベルト系"])

# 出走馬の絞り込み/選択
st.sidebar.markdown("---")
selected_horses = st.sidebar.multiselect(
    "出走予定馬を選択 (最大8頭推奨)",
    df_all["horse"].tolist(),
    default=["イクイノックス", "ドウデュース", "パンサラッサ", "タイトルホルダー", "スターズオンアース", "ディープボンド"]
)

if len(selected_horses) == 0:
    st.warning("サイドバーから出走馬を1頭以上選択してください。")
    st.stop()

df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)

# 能力スコア計算
going_penalty = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}
penalty = going_penalty.get(going, 1.0)

df_race["score"] = (
    df_race["speed"] * 0.35 +
    df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
    df_race["power"] * 0.2 +
    df_race["heavy_track"] * (1.15 - penalty) * 12
)
# 血統補正
df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

# 画面レイアウト
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 出走馬一覧 & 指数評価")
    st.dataframe(df_race[["horse", "style", "sire", "sire_line", "score"]].sort_values(by="score", ascending=False).style.format({"score": "{:.1f}"}))

with col2:
    st.subheader("📊 個別能力分析")
    target_h = st.selectbox("分析対象馬", df_race["horse"].tolist())
    h_info = df_race[df_race["horse"] == target_h].iloc[0]
    
    cats = ["スピード", "スタミナ", "パワー", "重馬場適性"]
    vals = [h_info["speed"], h_info["stamina"], h_info["power"], h_info["heavy_track"]]
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(cats, vals, color=["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd"])
    ax.set_ylim(60, 100)
    st.pyplot(fig)

# 2. 動く展開シミュレーター
st.markdown("---")
st.subheader("🎬 アニメーション展開シミュレーター & リアルタイム実況")

start_sim = st.button("▶️ 展開シミュレーションを開始")

# 脚質別の初期・中間・最終位置定義
style_base = {"逃げ": 90, "先行": 70, "差し": 45, "追い込み": 20}

if start_sim or "sim_frame" in st.session_state:
    progress_bar = st.progress(0)
    status_text = st.empty()
    plot_spot = st.empty()
    commentary_spot = st.empty()

    steps = [
        ("スタート直後", 0.0, "ゲートが開きました！綺麗なスタートです。"),
        ("向正面 (レース中盤)", 0.3, "各馬ポジションが確定。ペースが落ち着きます。"),
        ("3・4コーナー (勝負所)", 0.6, "後方勢が徐々に進出！前を捕まえにかかります。"),
        ("最終直線 (残り200m)", 0.85, "さあ最終直線！追い比べの大激闘！"),
        ("ゴールイン！", 1.0, "栄光のゴール！激戦を制したのは...！？")
    ]

    for label, progress, comment in steps:
        # 進捗更新
        progress_bar.progress(int(progress * 100))
        status_text.subheader(f"📍 現在地点: {label}")
        commentary_spot.info(f"🎤 **レース実況**: {comment}")

        # 位置の計算
        fig_sim, ax_sim = plt.subplots(figsize=(10, 4.5))
        
        positions = []
        for idx, row in df_race.iterrows():
            base_pos = style_base.get(row["style"], 50)
            
            # 進行度(progress)に応じた位置計算
            if progress < 0.5:
                # 序盤〜中盤：脚質通りの位置関係
                current_pos = base_pos * (progress * 2)
            else:
                # 終盤：スピード・スタミナ・パワーに応じた最後の伸び脚
                stamina_factor = row["stamina"] if dist >= 2400 else 90
                spurt = (row["speed"] * penalty + stamina_factor * 0.5) * (progress - 0.5) * 2.2
                current_pos = (base_pos * 1.0) + spurt
            
            positions.append((current_pos, row["horse"], row["style"]))

        # 順位順に描画
        positions.sort(key=lambda x: x[0], reverse=True)
        
        for i, (pos, name, style) in enumerate(positions):
            ax_sim.scatter(pos, len(positions) - i, s=250)
            ax_sim.text(pos + 2, len(positions) - i, f"{name} ({style})", fontsize=11, fontweight='bold', verticalalignment='center')

        ax_sim.set_xlim(0, 160)
        ax_sim.set_xlabel("進行距離 / ゴール位置 (右端がゴール)")
        ax_sim.axvline(x=140, color='red', linestyle='--', label='ゴール')
        ax_sim.get_yaxis().set_visible(False)
        ax_sim.grid(True, linestyle=':', alpha=0.5)
        
        plot_spot.pyplot(fig_sim)
        time.sleep(1.2)  # コマ送りアニメーションの間隔

    st.balloons()
    st.success("🎉 レース終了！上位予想馬の動きをご確認ください。")
