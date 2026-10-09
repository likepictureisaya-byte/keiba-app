import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定
st.set_page_config(
    page_title="JRAリアルコース競馬シミュレーター2026",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .stMultiSelect, .stSelectbox, .stNumberInput, .stButton, input, select {
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
""",
    unsafe_allow_html=True,
)

st.title("🏇 JRAリアルコース競馬シミュレーター (2026年最新版)")
st.caption(
    "2026年 10/10(土) サウジアラビアRC(11頭) ＆ 10/11(日) アイルランドT(16頭) 確定枠順・穴馬分析統合モデル"
)


# 2. データベース（2026年 サウジアラビアRC & アイルランドT 確定馬全頭）
@st.cache_data
def get_active_horse_db_2026():
  base_horses = [
      # === 2026 サウジアラビアロイヤルカップ（11頭・全頭） ===
      {
          "horse": "ニシノトラノスケ",
          "gate": 1,
          "race_type": "芝・マイル",
          "sire": "キズナ",
          "dam": "ニシノアモーレ",
          "style": "先行",
          "stamina": 87,
          "speed": 89,
          "power": 88,
          "heavy": 89,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "デミアン",
          "gate": 2,
          "race_type": "芝・マイル",
          "sire": "エピファネイア",
          "dam": "サロミナ",
          "style": "先行",
          "stamina": 88,
          "speed": 92,
          "power": 90,
          "heavy": 90,
          "opt_dist": 1600,
          "wins_short": "1-1-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "サトノハクマイ",
          "gate": 3,
          "race_type": "芝・マイル",
          "sire": "サトノダイヤモンド",
          "dam": "ハクマイ",
          "style": "差し",
          "stamina": 89,
          "speed": 90,
          "power": 89,
          "heavy": 91,
          "opt_dist": 1600,
          "wins_short": "1-0-1-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ハンサム",
          "gate": 4,
          "race_type": "芝・マイル",
          "sire": "モーリス",
          "dam": "ビューティフル",
          "style": "追込",
          "stamina": 86,
          "speed": 89,
          "power": 88,
          "heavy": 88,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "フィリオソラーレ",
          "gate": 5,
          "race_type": "芝・マイル",
          "sire": "ロードカナロア",
          "dam": "ソラーレ",
          "style": "先行",
          "stamina": 90,
          "speed": 95,
          "power": 92,
          "heavy": 92,
          "opt_dist": 1600,
          "wins_short": "1-0-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ベルウッドディープ",
          "gate": 6,
          "race_type": "芝・マイル",
          "sire": "リアルスティール",
          "dam": "ベルウッド",
          "style": "差し",
          "stamina": 89,
          "speed": 94,
          "power": 91,
          "heavy": 91,
          "opt_dist": 1600,
          "wins_short": "1-0-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "アゴルディーノ",
          "gate": 7,
          "race_type": "芝・マイル",
          "sire": "エフフォーリア",
          "dam": "アゴラ",
          "style": "先行",
          "stamina": 88,
          "speed": 91,
          "power": 90,
          "heavy": 90,
          "opt_dist": 1600,
          "wins_short": "1-1-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "マイネルピエトラ",
          "gate": 8,
          "race_type": "芝・マイル",
          "sire": "スクリーンヒーロー",
          "dam": "ピエトラ",
          "style": "逃げ",
          "stamina": 89,
          "speed": 88,
          "power": 92,
          "heavy": 94,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ジップスパーク",
          "gate": 9,
          "race_type": "芝・マイル",
          "sire": "ブリックスアンドモルタル",
          "dam": "スパーク",
          "style": "差し",
          "stamina": 87,
          "speed": 92,
          "power": 90,
          "heavy": 91,
          "opt_dist": 1600,
          "wins_short": "1-0-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "コスモストーム",
          "gate": 10,
          "race_type": "芝・マイル",
          "sire": "ダノンバラード",
          "dam": "ストーム",
          "style": "差し",
          "stamina": 88,
          "speed": 89,
          "power": 91,
          "heavy": 93,
          "opt_dist": 1600,
          "wins_short": "1-0-1-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ウインアイリス",
          "gate": 11,
          "race_type": "芝・マイル",
          "sire": "ゴールドシップ",
          "dam": "アイリス",
          "style": "追込",
          "stamina": 90,
          "speed": 88,
          "power": 91,
          "heavy": 94,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      # === 2026 アイルランドトロフィー（16頭・全頭） ===
      {
          "horse": "ニシノティアモ",
          "gate": 1,
          "race_type": "芝・中距離",
          "sire": "ドゥラメンテ",
          "dam": "ニシノアモーレ",
          "style": "先行",
          "stamina": 90,
          "speed": 92,
          "power": 91,
          "heavy": 92,
          "opt_dist": 1800,
          "wins_short": "2-0-0-1",
          "wins_mid": "2-1-0-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "チェルビアット",
          "gate": 2,
          "race_type": "芝・マイル・中距離",
          "sire": "ロードカナロア",
          "dam": "チェルビア",
          "style": "差し",
          "stamina": 88,
          "speed": 93,
          "power": 90,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "2-1-0-2",
          "wins_mid": "1-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "クイーンズウォーク",
          "gate": 3,
          "race_type": "芝・中距離",
          "sire": "キズナ",
          "dam": "ウェイヴェルアベニュー",
          "style": "先行",
          "stamina": 93,
          "speed": 95,
          "power": 93,
          "heavy": 92,
          "opt_dist": 1800,
          "wins_short": "1-0-0-0",
          "wins_mid": "3-1-0-2",
          "wins_long": "0-0-0-1",
      },
      {
          "horse": "クランフォード",
          "gate": 4,
          "race_type": "芝・マイル・中距離",
          "sire": "ブリックスアンドモルタル",
          "dam": "クラン",
          "style": "差し",
          "stamina": 86,
          "speed": 90,
          "power": 88,
          "heavy": 89,
          "opt_dist": 1600,
          "wins_short": "3-1-0-3",
          "wins_mid": "0-0-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "カネラフィーナ",
          "gate": 5,
          "race_type": "芝・中距離",
          "sire": "フランケル",
          "dam": "カネラ",
          "style": "差し",
          "stamina": 90,
          "speed": 91,
          "power": 91,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "1-1-0-1",
          "wins_mid": "2-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ムイ",
          "gate": 6,
          "race_type": "芝・中距離",
          "sire": "ハーツクライ",
          "dam": "ムイ",
          "style": "追込",
          "stamina": 85,
          "speed": 87,
          "power": 86,
          "heavy": 88,
          "opt_dist": 1800,
          "wins_short": "1-0-0-4",
          "wins_mid": "1-0-0-5",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ミラビリスマジック",
          "gate": 7,
          "race_type": "芝・中距離",
          "sire": "キタサンブラック",
          "dam": "ミラビリス",
          "style": "先行",
          "stamina": 89,
          "speed": 91,
          "power": 90,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "2-0-0-2",
          "wins_mid": "1-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ルージュソリテール",
          "gate": 8,
          "race_type": "芝・中距離",
          "sire": "エピファネイア",
          "dam": "ルージュ",
          "style": "差し",
          "stamina": 89,
          "speed": 92,
          "power": 90,
          "heavy": 91,
          "opt_dist": 1800,
          "wins_short": "1-1-0-1",
          "wins_mid": "2-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ウイントワイライト",
          "gate": 9,
          "race_type": "芝・中距離",
          "sire": "レイデオロ",
          "dam": "ダイワベスパー",
          "style": "追込",
          "stamina": 92,
          "speed": 93,
          "power": 92,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "2-1-0-2",
          "wins_mid": "1-2-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "セキトバイースト",
          "gate": 10,
          "race_type": "芝・中距離",
          "sire": "デクラレーションオブウォー",
          "dam": "ベアフットレディ",
          "style": "逃げ",
          "stamina": 93,
          "speed": 95,
          "power": 94,
          "heavy": 95,
          "opt_dist": 1800,
          "wins_short": "1-1-0-2",
          "wins_mid": "4-1-1-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ラヴァンダ",
          "gate": 11,
          "race_type": "芝・中距離",
          "sire": "シルバーステート",
          "dam": "ゴッドパイレーツ",
          "style": "差し",
          "stamina": 92,
          "speed": 96,
          "power": 93,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "2-1-0-1",
          "wins_mid": "3-2-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ミアネーロ",
          "gate": 12,
          "race_type": "芝・中距離",
          "sire": "ドゥラメンテ",
          "dam": "ミスエーニョ",
          "style": "差し",
          "stamina": 91,
          "speed": 93,
          "power": 92,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "1-0-0-1",
          "wins_mid": "2-2-1-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ワタシマツワ",
          "gate": 13,
          "race_type": "芝・中距離",
          "sire": "ルーラーシップ",
          "dam": "マツワ",
          "style": "追込",
          "stamina": 87,
          "speed": 88,
          "power": 88,
          "heavy": 89,
          "opt_dist": 1800,
          "wins_short": "1-0-0-3",
          "wins_mid": "1-0-0-4",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ハワイアンティアレ",
          "gate": 14,
          "race_type": "芝・中距離",
          "sire": "ロードカナロア",
          "dam": "ハワイアン",
          "style": "差し",
          "stamina": 90,
          "speed": 92,
          "power": 91,
          "heavy": 92,
          "opt_dist": 1800,
          "wins_short": "1-1-1-2",
          "wins_mid": "1-1-0-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ジョスラン",
          "gate": 15,
          "race_type": "芝・中距離",
          "sire": "エピファネイア",
          "dam": "ケイティーズハート",
          "style": "差し",
          "stamina": 93,
          "speed": 95,
          "power": 93,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "1-0-0-0",
          "wins_mid": "3-1-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "カムニャック",
          "gate": 16,
          "race_type": "芝・中長距離",
          "sire": "ブラックタイド",
          "dam": "ダンスアミーガ",
          "style": "差し",
          "stamina": 96,
          "speed": 96,
          "power": 94,
          "heavy": 94,
          "opt_dist": 2000,
          "wins_short": "0-0-0-0",
          "wins_mid": "3-2-0-1",
          "wins_long": "1-0-0-0",
      },
  ]
  return pd.DataFrame(base_horses)


df_all = get_active_horse_db_2026()

# サウジアラビアRC（11頭・確定）
SAUDI_MEMBERS_2026 = [
    "ニシノトラノスケ",
    "デミアン",
    "サトノハクマイ",
    "ハンサム",
    "フィリオソラーレ",
    "ベルウッドディープ",
    "アゴルディーノ",
    "マイネルピエトラ",
    "ジップスパーク",
    "コスモストーム",
    "ウインアイリス",
]

# アイルランドT（16頭・確定）
IRELAND_MEMBERS_2026 = [
    "ニシノティアモ",
    "チェルビアット",
    "クイーンズウォーク",
    "クランフォード",
    "カネラフィーナ",
    "ムイ",
    "ミラビリスマジック",
    "ルージュソリテール",
    "ウイントワイライト",
    "セキトバイースト",
    "ラヴァンダ",
    "ミアネーロ",
    "ワタシマツワ",
    "ハワイアンティアレ",
    "ジョスラン",
    "カムニャック",
]

# セッション状態初期化
if "selected_horses" not in st.session_state:
  st.session_state.selected_horses = SAUDI_MEMBERS_2026
if "venue" not in st.session_state:
  st.session_state.venue = "東京"
if "dist" not in st.session_state:
  st.session_state.dist = 1600


def set_preset_saudi():
  st.session_state.selected_horses = SAUDI_MEMBERS_2026
  st.session_state.venue = "東京"
  st.session_state.dist = 1600


def set_preset_ireland():
  st.session_state.selected_horses = IRELAND_MEMBERS_2026
  st.session_state.venue = "東京"
  st.session_state.dist = 1800


# タブ構成
tab_sim, tab_db = st.tabs([
    "🏇 レースシミュレーション",
    f"📊 2026最新データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.subheader("⚡ 2026年 今週末重賞メンバー 一括セット")
  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    st.button(
        f"👑 2026/10/10(土) サウジアラビアRC（東京・1600m）全{len(SAUDI_MEMBERS_2026)}頭",
        on_click=set_preset_saudi,
        use_container_width=True,
    )
  with col_btn2:
    st.button(
        f"👑 2026/10/11(日) アイルランドT（東京・1800m）全{len(IRELAND_MEMBERS_2026)}頭",
        on_click=set_preset_ireland,
        use_container_width=True,
    )

  st.markdown("---")
  st.subheader("⚙ レース条件設定")
  col_c1, col_c2, col_c3 = st.columns(3)
  with col_c1:
    venue = st.selectbox(
        "開催競馬場", ["東京", "中山", "京都", "阪神"], key="venue"
    )
  with col_c2:
    dist = st.selectbox(
        "距離(m)", [1600, 1800, 2000, 2400, 3000], key="dist"
    )
  with col_c3:
    going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

  st.markdown("---")
  st.subheader("🐎 出走馬選択 & ゲート/馬番設定")

  selected_horses = st.multiselect(
      "出走馬を選択（2〜18頭）",
      options=df_all["horse"].tolist(),
      key="selected_horses",
  )

  if len(selected_horses) < 2:
    st.warning("⚠ 出走馬を【2頭以上】選択してください。")
  else:
    if len(selected_horses) > 18:
      st.info("💡 18頭を超える選択の場合、18頭目までが出走対象となります。")
      selected_horses = selected_horses[:18]

    df_race = (
        df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
    )

    st.markdown("##### 🔢 出走馬のゲート番号確認・調整")

    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}

    for idx, r in df_race.iterrows():
      horse_name = r["horse"]
      default_gate = int(r["gate"])
      col_target = num_cols[idx % min(3, len(selected_horses))]
      with col_target:
        custom_num = st.number_input(
            f"{horse_name} (Gate)",
            min_value=1,
            max_value=24,
            value=default_gate,
            key=f"num_input_{horse_name}",
        )
        custom_numbers[horse_name] = custom_num

    df_race["num"] = df_race["horse"].map(custom_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    if dist <= 1600:
      df_race["current_wins"] = df_race["wins_short"]
      dist_label = "短距離(1600m以下)"
    elif dist <= 2000:
      df_race["current_wins"] = df_race["wins_mid"]
      dist_label = "中距離(1800〜2000m)"
    else:
      df_race["current_wins"] = df_race["wins_long"]
      dist_label = "長距離(2200m以上)"

    st.dataframe(
        df_race[[
            "num",
            "horse",
            "race_type",
            "style",
            "opt_dist",
            "current_wins",
            "sire",
            "dam",
        ]].rename(columns={
            "num": "ゲート番",
            "horse": "馬名",
            "race_type": "タイプ",
            "style": "脚質",
            "opt_dist": "適性距離",
            "current_wins": f"戦績 ({dist_label})",
            "sire": "父",
            "dam": "母",
        }),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("🔍 精確な展開予想 ＆ 🎯 穴馬推奨枠アナライザー")

    escape_count = len(df_race[df_race["style"] == "逃げ"])
    leader_count = len(df_race[df_race["style"] == "先行"])

    if escape_count >= 2 or (escape_count == 1 and leader_count >= 4):
      pace_type = "ハイペース (H)"
      pace_desc = "先行争いが激化し前半から速いラップが踏まれます。スタミナ持続力と直線での差し・追込馬が急浮上する高配当展開です。"
    elif escape_count == 1:
      pace_type = "ミドルペース (M)"
      pace_desc = (
          "単騎逃げのマイペース。折り合いと実力通りのラストの切れ味が試されるフラットな展開です。"
      )
    else:
      pace_type = "スローペース (S)"
      pace_desc = (
          "逃げ馬不在によるスローペース。直線まで余力が残る前残り展開や、瞬発力上位馬の先行押し切りが濃厚です。"
      )

    if going in ["重", "不良"]:
      pace_desc += (
          f" 馬場状態が【{going}】のため全体的にスタミナ消費が急激に激しくなります。"
          "重馬場適性（パワー数値）の高いパワー型穴馬の一変に注意してください。"
      )

    # ✨ 穴馬推奨ロジック（重馬場適性・適性距離・ペース適性の総合判断）
    df_race["hole_score"] = (
        (df_race["power"] * 0.4)
        + (df_race["heavy"] * 0.4)
        - (np.abs(df_race["opt_dist"] - dist) * 0.05)
    )
    # スピード1位/2位の「人気想定」を除外した最高スコア馬を穴馬として抽出
    sorted_by_speed = df_race.sort_values(
        by="speed", ascending=False
    ).reset_index(drop=True)
    fav_names = sorted_by_speed.head(2)["horse"].tolist()
    hole_candidates = df_race[~df_race["horse"].isin(fav_names)].sort_values(
        by="hole_score", ascending=False
    )

    hole_horse = (
        hole_candidates.iloc[0] if len(hole_candidates) > 0 else df_race.iloc[0]
    )

    c_p1, c_p2, c_p3 = st.columns([1, 1, 2])
    with c_p1:
      st.metric("予想ペース", pace_type)
      drain_multi = {
          "良": "1.0x (標準)",
          "稍重": "1.15x (ややタフ)",
          "重": "1.30x (タフ)",
          "不良": "1.45x (極限消耗)",
      }[going]
      st.metric("馬場負荷", drain_multi)
    with c_p2:
      st.metric(
          "🎯 穴馬推奨枠",
          f"{hole_horse['num']}番 {hole_horse['horse']}",
          help="馬場状態・パワー・距離適性・展開から波乱を演出する隠れた好走期待馬",
      )
    with c_p3:
      st.write("**【展開・隊列・穴馬の狙い目】**")
      st.info(
          f"{pace_desc}\n\n💡 **穴馬推奨理由 ({hole_horse['horse']})**: "
          f"重馬場/パワー指標({hole_horse['heavy']})が高く、{dist}m適性・展開負荷に強い隠れた実力馬です。"
      )

    st.markdown("---")
    st.subheader("🏁 リアルコース再現 ＆ 100回展開シミュレーション")

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
            .sim-container {{ width: 100%; max-width: 900px; margin: 0 auto; padding: 4px; text-align: center; }}
            .btn-group {{ display: flex; gap: 8px; margin-bottom: 10px; }}
            .start-btn {{
                flex: 1;
                height: 48px;
                background: linear-gradient(135deg, #27ae60, #1e824c);
                color: white;
                border: none;
                border-radius: 24px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }}
            .sim100-btn {{
                flex: 1;
                height: 48px;
                background: linear-gradient(135deg, #2980b9, #8e44ad);
                color: white;
                border: none;
                border-radius: 24px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }}
            .status-box {{ font-size: 15px; font-weight: bold; color: #2ecc71; min-height: 28px; margin-bottom: 6px; }}
            .svg-wrapper {{ 
                width: 100%; 
                background: #05140e; 
                border-radius: 12px; 
                border: 2px solid #1e3d30; 
                padding: 10px;
                box-sizing: border-box;
                overflow: hidden;
            }}
            .results-box {{ 
                margin-top: 14px; 
                background: #161b22; 
                padding: 14px; 
                border-radius: 10px; 
                border: 1px solid #30363d; 
                text-align: left; 
                max-height: 420px; 
                overflow-y: auto;
            }}
            .results-table-wrapper {{
                width: 100%;
                overflow-x: auto;
            }}
            .results-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; min-width: 600px; }}
            .results-table th {{ 
                position: sticky;
                top: 0;
                background: #21262d; 
                padding: 8px; 
                font-size: 13px; 
                text-align: center; 
                color: #8b949e; 
                border-bottom: 2px solid #30363d; 
                z-index: 10;
            }}
            .results-table td {{ padding: 8px; font-size: 14px; text-align: center; border-bottom: 1px solid #21262d; }}
            .waku-tag {{ display: inline-block; width: 22px; height: 22px; line-height: 22px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 6px; }}
            .rank-badge {{ font-weight: bold; font-size: 15px; }}
            .rank-1 {{ color: #f1c40f; }}
            .rank-2 {{ color: #bdc3c7; }}
            .rank-3 {{ color: #e67e22; }}
            .rate-tag {{ font-weight: bold; color: #e74c3c; font-size: 16px; }}
        </style>
    </head>
    <body>
        <div class="sim-container">
            <div class="btn-group">
                <button id="startBtn" class="start-btn">▶ レース発走 (GATE OPEN)</button>
                <button id="sim100Btn" class="sim100-btn">
