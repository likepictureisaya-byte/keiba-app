import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ページ基本設定
st.set_page_config(page_title="競馬展開・レース予想シミュレーター", layout="wide")

st.title("🏇 競馬重賞データ分析 & 展開シミュレーター")
st.caption("過去の重賞データおよび脚質・血統・馬場適性を網羅した総合分析ツール")

# 1. サンプル＆データベース構築（内蔵データ）
@st.cache_data
def get_builtin_data():
    # 競走馬マスターデータ
    horses_data = [
        {"horse": "イクイノックス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 95, "speed": 98, "power": 90, "heavy_track": 85},
        {"horse": "ドウデュース", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 90, "speed": 96, "power": 95, "heavy_track": 90},
        {"horse": "リバティアイランド", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 88, "speed": 97, "power": 88, "heavy_track": 82},
        {"horse": "ジャックドール", "sire": "モーリス", "sire_line": "グラスワンダー系", "style": "逃げ", "stamina": 85, "speed": 94, "power": 92, "heavy_track": 88},
        {"horse": "タイトルホルダー", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "逃げ", "stamina": 98, "speed": 88, "power": 96, "heavy_track": 95},
        {"horse": "スターズオンアース", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "追い込み", "stamina": 92, "speed": 93, "power": 89, "heavy_track": 85},
        {"horse": "ソダシ", "sire": "クロフネ", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 82, "speed": 92, "power": 90, "heavy_track": 80},
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 96, "speed": 82, "power": 94, "heavy_track": 98},
    ]
    df = pd.DataFrame(horses_data)
    return df

df_raw = get_builtin_data()

# サイドバー: 条件設定
st.sidebar.header("⚙️ レース条件設定")

venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
dist = st.sidebar.selectbox("距離 (m)", [1600, 2000, 2400, 2500, 3200])
weather = st.sidebar.selectbox("予想天気", ["晴", "曇", "小雨", "雨"])
going = st.sidebar.selectbox("想定馬場状態", ["良", "稍重", "重", "不良"])

st.sidebar.markdown("---")
favored_line = st.sidebar.selectbox("注目の血統ライン", ["サンデーサイレンス系", "キングカメハメハ系", "グラスワンダー系", "ノーザンダンサー系"])

# 馬場状態補正計算
going_penalty = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}
penalty = going_penalty.get(going, 1.0)

# 総合能力スコア算出
df_calc = df_raw.copy()
df_calc["score"] = (
    df_calc["speed"] * 0.4 + 
    df_calc["stamina"] * 0.3 + 
    df_calc["power"] * 0.2 + 
    df_calc["heavy_track"] * (1.1 - penalty) * 10
)

# 血統ボーナス
df_calc.loc[df_calc["sire_line"] == favored_line, "score"] += 5.0
df_calc = df_calc.sort_values(by="score", ascending=False).reset_index(drop=True)

# 2. メイン表示エリア
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 登録馬・能力総合判定")
    st.dataframe(df_calc[["horse", "sire", "style", "score"]].style.format({"score": "{:.1f}"}))

with col2:
    st.subheader("📊 能力レーダー比較")
    selected_horse = st.selectbox("分析対象馬を選択", df_calc["horse"].tolist())
    horse_info = df_calc[df_calc["horse"] == selected_horse].iloc[0]
    
    categories = ["スピード", "スタミナ", "パワー", "重馬場適性"]
    values = [horse_info["speed"], horse_info["stamina"], horse_info["power"], horse_info["heavy_track"]]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(categories, values, color=["#3498db", "#2ecc71", "#e67e22", "#9b59b6"])
    ax.set_ylim(50, 100)
    ax.set_ylabel("評価値")
    st.pyplot(fig)

# 3. 直線展開シミュレーション可視化
st.markdown("---")
st.subheader("🏁 直線展開シミュレーター (最終コーナー〜ゴール前)")

# 脚質ごとの初期位置
style_positions = {
    "逃げ": 85,
    "先行": 65,
    "差し": 40,
    "追い込み": 15
}

# 最終直線での脚色計算
fig_sim, ax_sim = plt.subplots(figsize=(10, 4))

for idx, row in df_calc.iterrows():
    base_pos = style_positions.get(row["style"], 50)
    # スピードとスタミナによる最後の伸び計算
    final_spurt = (row["speed"] * penalty + row["stamina"] * (dist / 2000)) * 0.15
    final_pos = base_pos + final_spurt
    
    # 描画
    ax_sim.scatter(final_pos, idx, s=200, label=f"{row['horse']} ({row['style']})")
    ax_sim.text(final_pos + 1, idx, f" {row['horse']}", verticalalignment='center', fontsize=11, fontweight='bold')

ax_sim.set_xlim(0, 140)
ax_sim.set_yticks(range(len(df_calc)))
ax_sim.set_yticklabels(df_calc["horse"])
ax_sim.set_xlabel("ゴール前の到達予測位置 (右に行くほど優勢)")
ax_sim.axvline(x=120, color='red', linestyle='--', label='G1ゴールライン')
ax_sim.grid(True, linestyle=':', alpha=0.6)
ax_sim.invert_yaxis()  # 上位を上に配置

st.pyplot(fig_sim)

st.success("展開予想シミュレーション完了！コース条件や血統条件を変えて分析してみてください。")
