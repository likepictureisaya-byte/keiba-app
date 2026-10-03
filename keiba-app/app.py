import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="競馬重賞データ分析＆展開シミュレーター", layout="wide")

st.title("🐎 競馬重賞データ分析 ＆ 展開シミュレーター")
st.caption("データ分析に基づく「血統」「馬場・天気」「コース適性」分析および直線展開図の可視化")

@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_excel(filepath, sheet_name='確認済みデータ')
    except Exception as e:
        st.error(f"ファイル読み込みエラー: {e}")
        return pd.DataFrame()
    
    df = df.dropna(subset=['horse', 'corner_positions']).copy()
    
    def parse_corner_data(c_str):
        if not isinstance(c_str, str) or c_str == '—':
            return "不明", 99.0
        parts = [p.strip() for p in c_str.split('-') if p.strip().isdigit()]
        if not parts:
            return "不明", 99.0
        positions = [int(p) for p in parts]
        first_pos = positions[0]
        avg_pos = sum(positions) / len(positions)
        last_pos = positions[-1]
        
        if first_pos == 1:
            style = "逃げ"
        elif avg_pos <= 3.5:
            style = "先行"
        elif avg_pos <= 7.5:
            style = "差し"
        else:
            style = "追込"
            
        return style, last_pos

    res = df['corner_positions'].apply(parse_corner_data)
    df['running_style'] = [r[0] for r in res]
    df['4k_pos'] = [r[1] for r in res]
    
    pedigree_map = {
        'トリオンフ': {'sire': 'タートルボウル', 'sire_line': 'ノーザンダンサー系'},
        'ヒシイグアス': {'sire': 'ハーツクライ', 'sire_line': 'サンデーサイレンス系'},
        'パンサラッサ': {'sire': 'ロードカナロア', 'sire_line': 'キングカメハメハ系'},
        'レッドガラン': {'sire': 'ロードカナロア', 'sire_line': 'キングカメハメハ系'},
        'アルナシーム': {'sire': 'モーリス', 'sire_line': 'グラスワンダー系'},
        'サクラトゥジュール': {'sire': 'ネオユニヴァース', 'sire_line': 'サンデーサイレンス系'},
        'リラエンブレム': {'sire': 'キズナ', 'sire_line': 'サンデーサイレンス系'},
        'シックスペンス': {'sire': 'キズナ', 'sire_line': 'サンデーサイレンス系'},
    }
    
    sires = []
    sire_lines = []
    for h in df['horse']:
        info = pedigree_map.get(str(h).strip(), {'sire': '不明', 'sire_line': 'その他'})
        sires.append(info['sire'])
        sire_lines.append(info['sire_line'])
        
    df['sire'] = sires
    df['sire_line'] = sire_lines
    return df

EXCEL_FILE = "data.xlsx"
df_raw = load_data(EXCEL_FILE)

if df_raw.empty:
    st.warning("有効なデータを読み込めませんでした。ファイル名を確認してください。")
    st.stop()

st.sidebar.header("⚙️ レース条件設定")
venue_list = list(df_raw['venue'].unique())
selected_venue = st.sidebar.selectbox("開催競馬場", venue_list, index=0)

surface_list = list(df_raw['surface'].unique())
selected_surface = st.sidebar.selectbox("馬場種別", surface_list, index=0)

dist_list = sorted(list(df_raw['distance_m'].unique()))
selected_dist = st.sidebar.selectbox("距離 (m)", dist_list, index=0)

selected_weather = st.sidebar.selectbox("予想天気", ["晴", "曇", "小雨", "雨"])
selected_going = st.sidebar.selectbox("想定馬場状態", ["良", "稍重", "重", "不良"])

line_options = ["サンデーサイレンス系", "キングカメハメハ系", "グラスワンダー系", "ノーザンダンサー系", "その他"]
favored_line = st.sidebar.selectbox("注目・コース適合血統", line_options, index=0)

df_filtered = df_raw[
    (df_raw['venue'] == selected_venue) & 
    (df_raw['surface'] == selected_surface) & 
    (df_raw['distance_m'] == selected_dist)
].copy()

if len(df_filtered) < 2:
    st.warning(f"※{selected_venue} {selected_surface}{selected_dist}m のデータ件数が少ないため全件表示しています。")
    df_filtered = df_raw.copy()

def evaluate_aptitude(row):
    score = 60.0
    if row['sire_line'] == favored_line:
        score += 20.0
    elif row['sire_line'] in ["サンデーサイレンス系", "キングカメハメハ系"]:
        score += 10.0
    if selected_going in ["重", "不良"]:
        if row['sire_line'] in ["グラスワンダー系", "ノーザンダンサー系"]:
            score += 10.0
    if selected_venue == "中山" and row['running_style'] in ["逃げ", "先行"]:
        score += 10.0
    return min(score, 100.0)

df_filtered['適性スコア'] = df_filtered.apply(evaluate_aptitude, axis=1)

st.subheader(f"🏟️ 対象条件: 【{selected_venue}】 {selected_surface}{selected_dist}m ({selected_weather} / 馬場: {selected_going})")

col1, col2 = st.columns([6, 4])
with col1:
    st.markdown("### 📊 出走・過去データ馬の適合度診断")
    st.dataframe(
        df_filtered[['horse', 'sire', 'sire_line', 'running_style', 'corner_positions', 'last3f', '適性スコア']].rename(
            columns={'horse': '馬名', 'sire': '父', 'sire_line': '父系統', 'running_style': '推定脚質', 'corner_positions': '通過順位', 'last3f': '上がり3F'}
        ),
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown("### ⏱️ 展開・ペース判定")
    n_escape = (df_filtered['running_style'] == "逃げ").sum()
    n_ahead = (df_filtered['running_style'] == "先行").sum()
    if n_escape >= 2:
        st.error("想定ペース: 🔥 ハイペース")
    elif n_escape == 1 and n_ahead <= 2:
        st.success("想定ペース: 🧊 スローペース")
    else:
        st.info("想定ペース: ⚖️ ミドルペース")
    st.write(f"- 逃げ傾向馬: **{n_escape}頭**")
    st.write(f"- 先行傾向馬: **{n_ahead}頭**")

st.divider()
st.subheader("🎯 4コーナー〜最終直線 展開シミュレーション")

if not df_filtered.empty:
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.set_xlim(-1, 13)
    ax.set_ylim(0, 6)
    track_color = 'lightgreen' if selected_surface == "芝" else 'wheat'
    ax.add_patch(patches.Rectangle((-1, 0.5), 14, 4.5, facecolor=track_color, alpha=0.3))
    ax.axhline(y=0.8, color='darkgreen', linewidth=3)
    ax.axhline(y=4.8, color='brown', linewidth=2, linestyle='--')
    ax.annotate('← ゴール方向 (最終直線)', xy=(0.5, 5.2), xytext=(5.0, 5.2),
                arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8), fontsize=10, fontweight='bold')

    df_sorted = df_filtered.sort_values(by='4k_pos').reset_index(drop=True)
    for idx, row in df_sorted.iterrows():
        pos = row['4k_pos']
        x_pos = pos * 1.1 if pos < 15 else 12.0
        frame_val = row['frame'] if pd.notnull(row['frame']) else (idx + 1)
        y_pos = 1.3 + ((frame_val * 3) % 8) * 0.4
        color_map = {"逃げ": "#FF4B4B", "先行": "#FFA500", "差し": "#1E90FF", "追込": "#8A2BE2"}
        face_color = color_map.get(row['running_style'], "gray")
        
        circle = patches.Circle((x_pos, y_pos), 0.4, edgecolor='black', facecolor=face_color, alpha=0.85)
        ax.add_patch(circle)
        horse_name = str(row['horse'])[:4]
        ax.text(x_pos, y_pos, f"{int(frame_val) if pd.notnull(frame_val) else ''}\n{horse_name}", 
                horizontalalignment='center', verticalalignment='center', fontsize=8, color='white', fontweight='bold')

    ax.set_title(f"【{selected_venue} {selected_surface}{selected_dist}m】 4角通過時〜直線展開予想図", fontsize=12)
    ax.axis('off')
    st.pyplot(fig)
