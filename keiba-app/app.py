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
    "2026年10月4日 毎日王冠（17頭）＆ 京都大賞典（18頭）確定メンバー統合モデル"
)


# 2. データベース（2026年10月4日 確定出走全頭：35頭保持）
@st.cache_data
def get_active_horse_db_2026():
  base_horses = [
      # === 2026 毎日王冠（17頭） ===
      {
          "horse": "セイウンハーデス",
          "race_type": "芝・中距離",
          "sire": "シルバーステート",
          "dam": "ハイランドダンス",
          "style": "逃げ",
          "stamina": 90,
          "speed": 92,
          "power": 93,
          "heavy": 94,
          "opt_dist": 1800,
          "wins_short": "0-0-0-0",
          "wins_mid": "4-2-1-6",
          "wins_long": "0-0-0-1",
      },
      {
          "horse": "リアライズシリウス",
          "race_type": "芝・マイル・中距離",
          "sire": "ポエティックフレア",
          "dam": "シリアス",
          "style": "先行",
          "stamina": 88,
          "speed": 95,
          "power": 91,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "2-0-0-0",
          "wins_mid": "1-1-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "レディネス",
          "race_type": "芝・中距離",
          "sire": "リアルスティール",
          "dam": "スマートレイピア",
          "style": "先行",
          "stamina": 87,
          "speed": 91,
          "power": 90,
          "heavy": 89,
          "opt_dist": 1800,
          "wins_short": "1-0-0-1",
          "wins_mid": "3-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "サトノシャイニング",
          "race_type": "芝・中距離",
          "sire": "キズナ",
          "dam": "スワンドリーム",
          "style": "先行",
          "stamina": 91,
          "speed": 94,
          "power": 92,
          "heavy": 92,
          "opt_dist": 2000,
          "wins_short": "0-1-0-0",
          "wins_mid": "3-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "クルゼイロドスル",
          "race_type": "芝・マイル",
          "sire": "ファインニードル",
          "dam": "スタファニア",
          "style": "差し",
          "stamina": 85,
          "speed": 92,
          "power": 89,
          "heavy": 88,
          "opt_dist": 1600,
          "wins_short": "4-1-1-6",
          "wins_mid": "0-0-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ライヒスアドラー",
          "race_type": "芝・中距離",
          "sire": "シスキン",
          "dam": "アドラーイエガー",
          "style": "差し",
          "stamina": 89,
          "speed": 93,
          "power": 90,
          "heavy": 91,
          "opt_dist": 1800,
          "wins_short": "1-1-0-0",
          "wins_mid": "2-0-1-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ロングラン",
          "race_type": "芝・中距離",
          "sire": "ヴィクトワールピサ",
          "dam": "アレーグレ",
          "style": "追込",
          "stamina": 88,
          "speed": 90,
          "power": 91,
          "heavy": 92,
          "opt_dist": 1800,
          "wins_short": "1-0-0-2",
          "wins_mid": "4-2-1-12",
          "wins_long": "0-0-0-1",
      },
      {
          "horse": "ビーアストニッシド",
          "race_type": "芝・中距離",
          "sire": "アメリカンペイリオット",
          "dam": "マウレア",
          "style": "逃げ",
          "stamina": 86,
          "speed": 89,
          "power": 90,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "0-1-0-3",
          "wins_mid": "2-2-1-15",
          "wins_long": "0-0-0-1",
      },
      {
          "horse": "ドラゴンブースト",
          "race_type": "芝・マイル・中距離",
          "sire": "ディーマジェスティ",
          "dam": "プレシャスゴールド",
          "style": "差し",
          "stamina": 87,
          "speed": 91,
          "power": 89,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "2-1-0-3",
          "wins_mid": "1-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "エルトンバローズ",
          "race_type": "芝・マイル・中距離",
          "sire": "ディープブリランテ",
          "dam": "ショウナンカラット",
          "style": "先行",
          "stamina": 89,
          "speed": 94,
          "power": 91,
          "heavy": 91,
          "opt_dist": 1800,
          "wins_short": "2-1-0-3",
          "wins_mid": "3-2-1-4",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ランスオブカオス",
          "race_type": "芝・中距離",
          "sire": "シルバーステート",
          "dam": "ランスオブプランドル",
          "style": "差し",
          "stamina": 88,
          "speed": 91,
          "power": 90,
          "heavy": 89,
          "opt_dist": 1800,
          "wins_short": "1-0-0-1",
          "wins_mid": "3-1-1-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "レガーロデルシエロ",
          "race_type": "芝・マイル・中距離",
          "sire": "ロードカナロア",
          "dam": "デアレガーロ",
          "style": "先行",
          "stamina": 86,
          "speed": 92,
          "power": 91,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "2-2-0-2",
          "wins_mid": "1-2-1-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ホウオウビスケッツ",
          "race_type": "芝・中距離",
          "sire": "マインドユアビスケッツ",
          "dam": "ホウオウサブリナ",
          "style": "逃げ",
          "stamina": 91,
          "speed": 94,
          "power": 93,
          "heavy": 93,
          "opt_dist": 1800,
          "wins_short": "0-0-0-0",
          "wins_mid": "5-3-1-5",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "レイニング",
          "race_type": "芝・マイル・中距離",
          "sire": "サートゥルナーリア",
          "dam": "クルミナル",
          "style": "差し",
          "stamina": 88,
          "speed": 95,
          "power": 92,
          "heavy": 91,
          "opt_dist": 1800,
          "wins_short": "1-0-0-0",
          "wins_mid": "3-1-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "シャンパンカラー",
          "race_type": "芝・マイル",
          "sire": "ドゥラメンテ",
          "dam": "メモリアルライフ",
          "style": "追込",
          "stamina": 86,
          "speed": 94,
          "power": 92,
          "heavy": 93,
          "opt_dist": 1600,
          "wins_short": "3-0-1-5",
          "wins_mid": "0-0-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "アドマイヤクワッズ",
          "race_type": "芝・マイル",
          "sire": "リアルスティール",
          "dam": "アドマイヤローザ",
          "style": "差し",
          "stamina": 86,
          "speed": 94,
          "power": 89,
          "heavy": 89,
          "opt_dist": 1600,
          "wins_short": "2-1-0-1",
          "wins_mid": "1-0-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ダノンエアズロック",
          "race_type": "芝・中距離",
          "sire": "モーリス",
          "dam": "モシーン",
          "style": "先行",
          "stamina": 90,
          "speed": 93,
          "power": 92,
          "heavy": 90,
          "opt_dist": 1800,
          "wins_short": "1-0-0-0",
          "wins_mid": "3-0-0-3",
          "wins_long": "0-0-0-1",
      },
      # === 2026 京都大賞典（18頭・確定メンバー） ===
      {
          "horse": "ウエストナウ",
          "race_type": "芝・中長距離",
          "sire": "キズナ",
          "dam": "エムズクリフ",
          "style": "先行",
          "stamina": 92,
          "speed": 92,
          "power": 91,
          "heavy": 91,
          "opt_dist": 2200,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-0-2",
          "wins_long": "1-1-0-1",
      },
      {
          "horse": "ヴェルテンベルク",
          "race_type": "芝・中長距離",
          "sire": "キッカケ",
          "dam": "ワイオラ",
          "style": "差し",
          "stamina": 91,
          "speed": 89,
          "power": 90,
          "heavy": 92,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-2-5",
          "wins_long": "1-1-1-4",
      },
      {
          "horse": "ディープモンスター",
          "race_type": "芝・中長距離",
          "sire": "ディープインパクト",
          "dam": "シスタルノ",
          "style": "差し",
          "stamina": 93,
          "speed": 91,
          "power": 92,
          "heavy": 93,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "3-4-2-6",
          "wins_long": "2-1-0-5",
      },
      {
          "horse": "ヘデントール",
          "race_type": "芝・長距離",
          "sire": "ルーラーシップ",
          "dam": "コルコバード",
          "style": "差し",
          "stamina": 97,
          "speed": 93,
          "power": 94,
          "heavy": 95,
          "opt_dist": 2500,
          "wins_short": "0-0-0-0",
          "wins_mid": "1-1-0-1",
          "wins_long": "4-1-0-1",
      },
      {
          "horse": "ヴェルミセル",
          "race_type": "芝・長距離",
          "sire": "ゴールドシップ",
          "dam": "トップコメット",
          "style": "追込",
          "stamina": 94,
          "speed": 88,
          "power": 90,
          "heavy": 93,
          "opt_dist": 2600,
          "wins_short": "0-0-0-0",
          "wins_mid": "1-0-1-3",
          "wins_long": "2-2-0-4",
      },
      {
          "horse": "アクアヴァーナル",
          "race_type": "芝・中長距離",
          "sire": "キタサンブラック",
          "dam": "アクアリベリス",
          "style": "差し",
          "stamina": 93,
          "speed": 92,
          "power": 91,
          "heavy": 92,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-1-2",
          "wins_long": "2-1-0-1",
      },
      {
          "horse": "リビアングラス",
          "race_type": "芝・中長距離",
          "sire": "キズナ",
          "dam": "ディルガ",
          "style": "先行",
          "stamina": 93,
          "speed": 90,
          "power": 92,
          "heavy": 91,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-1-3",
          "wins_long": "1-1-1-3",
      },
      {
          "horse": "ミクニインスパイア",
          "race_type": "芝・中長距離",
          "sire": "サトノダイヤモンド",
          "dam": "ミクニ",
          "style": "差し",
          "stamina": 91,
          "speed": 90,
          "power": 89,
          "heavy": 90,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-0-2",
          "wins_long": "1-1-1-2",
      },
      {
          "horse": "ミステリーウェイ",
          "race_type": "芝・長距離",
          "sire": "ジャスタウェイ",
          "dam": "ミステリートレイン",
          "style": "先行",
          "stamina": 94,
          "speed": 87,
          "power": 91,
          "heavy": 93,
          "opt_dist": 2600,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-2-1-8",
          "wins_long": "2-1-1-5",
      },
      {
          "horse": "マイネルエンペラー",
          "race_type": "芝・中長距離",
          "sire": "ゴールドシップ",
          "dam": "マイネテレジア",
          "style": "差し",
          "stamina": 94,
          "speed": 89,
          "power": 92,
          "heavy": 94,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-1-2-4",
          "wins_long": "1-2-0-3",
      },
      {
          "horse": "ファミリータイム",
          "race_type": "芝・中長距離",
          "sire": "リアルスティール",
          "dam": "タイムトラベラー",
          "style": "差し",
          "stamina": 91,
          "speed": 90,
          "power": 89,
          "heavy": 90,
          "opt_dist": 2200,
          "wins_short": "0-0-0-0",
          "wins_mid": "3-1-0-3",
          "wins_long": "0-1-1-2",
      },
      {
          "horse": "エコロディノス",
          "race_type": "芝・中長距離",
          "sire": "キタサンブラック",
          "dam": "エコロプライド",
          "style": "先行",
          "stamina": 92,
          "speed": 91,
          "power": 90,
          "heavy": 91,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-2-0-1",
          "wins_long": "1-1-0-1",
      },
      {
          "horse": "サフィラ",
          "race_type": "芝・中長距離",
          "sire": "ハーツクライ",
          "dam": "サロミナ",
          "style": "差し",
          "stamina": 91,
          "speed": 92,
          "power": 90,
          "heavy": 90,
          "opt_dist": 2200,
          "wins_short": "1-1-1-2",
          "wins_mid": "1-1-0-3",
          "wins_long": "1-0-0-1",
      },
      {
          "horse": "サヴォーナ",
          "race_type": "芝・中長距離",
          "sire": "キズナ",
          "dam": "テイラーバートン",
          "style": "先行",
          "stamina": 94,
          "speed": 90,
          "power": 93,
          "heavy": 93,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "1-2-1-4",
          "wins_long": "2-2-0-5",
      },
      {
          "horse": "メイショウブレゲ",
          "race_type": "芝・長距離",
          "sire": "ゴールドシップ",
          "dam": "メイショウツバクロ",
          "style": "追込",
          "stamina": 96,
          "speed": 88,
          "power": 91,
          "heavy": 94,
          "opt_dist": 2600,
          "wins_short": "0-0-0-0",
          "wins_mid": "1-0-1-6",
          "wins_long": "3-1-1-8",
      },
      {
          "horse": "ショウナンラプンタ",
          "race_type": "芝・中長距離",
          "sire": "キズナ",
          "dam": "フリアアステカ",
          "style": "差し",
          "stamina": 94,
          "speed": 93,
          "power": 92,
          "heavy": 93,
          "opt_dist": 2400,
          "wins_short": "0-0-0-0",
          "wins_mid": "2-2-0-2",
          "wins_long": "1-1-1-2",
      },
      {
          "horse": "キングスコール",
          "race_type": "芝・中長距離",
          "sire": "ドゥラメンテ",
          "dam": "レインボーダリア",
          "style": "先行",
          "stamina": 91,
          "speed": 93,
          "power": 91,
          "heavy": 90,
          "opt_dist": 2200,
          "wins_short": "1-0-0-0",
          "wins_mid": "2-0-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ダノンシーマ",
          "race_type": "芝・中長距離",
          "sire": "キタサンブラック",
          "dam": "インクルードベティ",
          "style": "先行",
          "stamina": 92,
          "speed": 93,
          "power": 92,
          "heavy": 91,
          "opt_dist": 2200,
          "wins_short": "0-0-0-0",
          "wins_mid": "3-1-0-1",
          "wins_long": "1-0-1-0",
      },
  ]
  return pd.DataFrame(base_horses)


df_all = get_active_horse_db_2026()

# 2026年10月4日 確定出走メンバー
MAINICHI_MEMBERS_2026 = [
    "セイウンハーデス",
    "リアライズシリウス",
    "レディネス",
    "サトノシャイニング",
    "クルゼイロドスル",
    "ライヒスアドラー",
    "ロングラン",
    "ビーアストニッシド",
    "ドラゴンブースト",
    "エルトンバローズ",
    "ランスオブカオス",
    "レガーロデルシエロ",
    "ホウオウビスケッツ",
    "レイニング",
    "シャンパンカラー",
    "アドマイヤクワッズ",
    "ダノンエアズロック",
]

KYOTO_MEMBERS_2026 = [
    "ウエストナウ",
    "ヴェルテンベルク",
    "ディープモンスター",
    "ヘデントール",
    "ヴェルミセル",
    "アクアヴァーナル",
    "リビアングラス",
    "ミクニインスパイア",
    "ミステリーウェイ",
    "マイネルエンペラー",
    "ファミリータイム",
    "エコロディノス",
    "サフィラ",
    "サヴォーナ",
    "メイショウブレゲ",
    "ショウナンラプンタ",
    "キングスコール",
    "ダノンシーマ",
]

# セッション状態初期化
if "selected_horses" not in st.session_state:
  st.session_state.selected_horses = MAINICHI_MEMBERS_2026
if "venue" not in st.session_state:
  st.session_state.venue = "東京"
if "dist" not in st.session_state:
  st.session_state.dist = 1800


def set_preset_mainichi():
  st.session_state.selected_horses = MAINICHI_MEMBERS_2026
  st.session_state.venue = "東京"
  st.session_state.dist = 1800


def set_preset_kyoto():
  st.session_state.selected_horses = KYOTO_MEMBERS_2026
  st.session_state.venue = "京都"
  st.session_state.dist = 2400


# タブ構成
tab_sim, tab_db = st.tabs([
    "🏇 レースシミュレーション",
    f"📊 2026最新データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.subheader("⚡ 2026年重賞メンバー 一括セット")
  col_btn1, col_btn2 = st.columns(2)
  with col_btn1:
    st.button(
        f"👑 2026 毎日王冠（東京・芝1800m）全{len(MAINICHI_MEMBERS_2026)}頭を一括セット",
        on_click=set_preset_mainichi,
        use_container_width=True,
    )
  with col_btn2:
    st.button(
        f"👑 2026 京都大賞典（京都・芝2400m）全{len(KYOTO_MEMBERS_2026)}頭を一括セット",
        on_click=set_preset_kyoto,
        use_container_width=True,
    )

  st.markdown("---")
  st.subheader("⚙ レース条件設定")
  col_c1, col_c2, col_c3 = st.columns(3)
  with col_c1:
    venue = st.selectbox(
        "開催競馬場", ["東京", "京都", "中山", "阪神"], key="venue"
    )
  with col_c2:
    dist = st.selectbox(
        "距離(m)", [1800, 2400, 1600, 2000, 3000], key="dist"
    )
  with col_c3:
    going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

  st.markdown("---")
  st.subheader("🐎 出走馬選択 & 枠順設定")

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

    st.markdown("##### 🔢 出走馬の馬番設定")

    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}

    for idx, horse_name in enumerate(selected_horses):
      col_target = num_cols[idx % min(3, len(selected_horses))]
      with col_target:
        custom_num = st.number_input(
            f"{horse_name}",
            min_value=1,
            max_value=18,
            value=idx + 1,
            key=f"num_input_{horse_name}",
        )
        custom_numbers[horse_name] = custom_num

    df_race = (
        df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
    )
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
            "num": "馬番",
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
    st.subheader("🔍 精確な展開予想アナライザー")

    escape_count = len(df_race[df_race["style"] == "逃げ"])
    leader_count = len(df_race[df_race["style"] == "先行"])

    if escape_count >= 2 or (escape_count == 1 and leader_count >= 4):
      pace_type = "ハイペース (H)"
      pace_desc = "同型（逃げ・先行馬）が多く前半からポジション争いが激化します。ハイペース化しやすく、タフなスタミナと直線での差し・追込馬が台頭しやすい展開です。"
    elif escape_count == 1:
      pace_type = "ミドルペース (M)"
      pace_desc = (
          "単騎逃げの形になり引き締まった平均ペースで流れます。"
          "各馬の実力と距離適性がストレートに反映されやすい展開です。"
      )
    else:
      pace_type = "スローペース (S)"
      pace_desc = (
          "明確な逃げ馬が不在で押し出される形のスローペースが予想されます。"
          "前残りの展開や、最後の直線での一瞬の切れ味（上がり勝負）が決め手となります。"
      )

    if going in ["重", "不良"]:
      pace_desc += (
          f" なお、馬場状態が【{going}】のため全体的にスタミナ消費が激しくなります。"
          "重馬場適性（パワー）が低い馬は直線で急激に失速する危険があります。"
      )

    c_p1, c_p2 = st.columns([1, 2])
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
      st.write("**【展開・隊列分析】**")
      st.info(pace_desc)

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
            /* スクロール可能な結果コンテナを追加 */
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
                <button id="sim100Btn" class="sim100-btn">⚡ 100回展開シミュレーション (上位5頭分析)</button>
            </div>
            
            <div id="statusBox" class="status-box">ボタンを押してシミュレーションを開始してください</div>
            
            <div class="svg-wrapper">
                <svg id="trackSvg" viewBox="0 0 720 380" width="100%" height="auto" style="display: block;">
                    <path id="outerTrack" d="M 220 70 L 500 70 A 110 110 0 0 1 500 290 L 220 290 A 110 110 0 0 1 220 70 Z" fill="#1b4d3e" stroke="#2e8b57" stroke-width="26"/>
                    <path id="innerTrack" d="M 220 84 L 500 84 A 96 96 0 0 1 500 276 L 220 276 A 96 96 0 0 1 220 84 Z" fill="#0e1117" stroke="#0e1117" stroke-width="2"/>

                    <g id="goalGroup"></g>
                    <g id="startGroup"></g>
                    <g id="horsesGroup"></g>
                </svg>
            </div>

            <div class="results-box">
                <div id="resultsTitle" style="font-weight: bold; color: #f1c40f; font-size: 16px;">🏆 結果表示領域</div>
                <div id="resultsContent">発走準備完了</div>
            </div>
        </div>

        <script>
            const horsesData = {json.dumps(horses_js)};
            const raceConfig = {json.dumps(race_config_js)};
            let animId = null;

            const GOING_DRAIN_MAP = {{ "良": 1.0, "稍重": 1.15, "重": 1.30, "不良": 1.45 }};
            const goingDrain = GOING_DRAIN_MAP[raceConfig.going] || 1.0;

            function getWakuStyle(num, total) {{
                let waku = Math.ceil((num / total) * 8);
                if (total <= 8) waku = num;
                const colors = [
                    {{ bg: '#ffffff', text: '#000000' }},
                    {{ bg: '#222222', text: '#ffffff' }},
                    {{ bg: '#e74c3c', text: '#ffffff' }},
                    {{ bg: '#3498db', text: '#ffffff' }},
                    {{ bg: '#f1c40f', text: '#000000' }},
                    {{ bg: '#2ecc71', text: '#ffffff' }},
                    {{ bg: '#e67e22', text: '#ffffff' }},
                    {{ bg: '#9b59b6', text: '#ffffff' }}
                ];
                return colors[Math.min(Math.max(waku - 1, 0), 7)];
            }}

            const totalLapsProgress = (raceConfig.dist / 2000.0);

            const COURSE_SPECS = {{
                "東京": {{ dir: -1, startP: raceConfig.dist === 1800 ? 0.68 : (raceConfig.dist === 1600 ? 0.58 : 0.20), slopeP: [0.02, 0.12] }},
                "中山": {{ dir: 1, startP: raceConfig.dist === 2000 ? 0.02 : (raceConfig.dist === 1600 ? 0.55 : 0.30), slopeP: [0.02, 0.08] }},
                "京都": {{ dir: 1, startP: raceConfig.dist === 2400 ? 0.10 : 0.60, slopeP: [0.40, 0.60] }},
                "阪神": {{ dir: 1, startP: raceConfig.dist === 2000 ? 0.20 : 0.55, slopeP: [0.02, 0.08] }}
            }};

            const spec = COURSE_SPECS[raceConfig.venue] || COURSE_SPECS["京都"];
            spec.goalP = spec.startP + totalLapsProgress;

            function getTrackPoint(p, laneOffset = 0) {{
                p = (p % 1.0 + 1.0) % 1.0;
                const r = 110 + laneOffset;
                const lenStr = 280;
                const circumference = 2 * Math.PI * r + 2 * lenStr;
                const distOnTrack = p * circumference;

                let x, y, angle;

                if (distOnTrack <= lenStr) {{
                    x = 500 - distOnTrack; y = 290 + laneOffset; angle = Math.PI;
                }} else if (distOnTrack <= lenStr + Math.PI * r) {{
                    const arcLen = distOnTrack - lenStr;
                    const theta = Math.PI / 2 + (arcLen / r);
                    x = 220 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
                }} else if (distOnTrack <= 2 * lenStr + Math.PI * r) {{
                    const strLen2 = distOnTrack - (lenStr + Math.PI * r);
                    x = 220 + strLen2; y = 70 - laneOffset; angle = 0;
                }} else {{
                    const arcLen2 = distOnTrack - (2 * lenStr + Math.PI * r);
                    const theta = -Math.PI / 2 + (arcLen2 / r);
                    x = 500 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
                }}

                if (spec.dir === -1) {{ x = 720 - x; angle = Math.PI - angle; }}
                return {{ x, y, angle }};
            }}

            function drawCourse() {{
                const goalPt = getTrackPoint(spec.goalP);
                document.getElementById('goalGroup').innerHTML = `
                    <line x1="${{goalPt.x}}" y1="${{goalPt.y - 20}}" x2="${{goalPt.x}}" y2="${{goalPt.y + 20}}" stroke="#ff3333" stroke-width="4"/>
                    <text x="${{goalPt.x}}" y="${{goalPt.y + 36}}" fill="#ff3333" font-size="13" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
                `;

                const startPt = getTrackPoint(spec.startP);
                document.getElementById('startGroup').innerHTML = `
                    <line x1="${{startPt.x}}" y1="${{startPt.y - 16}}" x2="${{startPt.x}}" y2="${{startPt.y + 16}}" stroke="#2ecc71" stroke-width="3"/>
                    <text x="${{startPt.x}}" y="${{startPt.y - 20}}" fill="#2ecc71" font-size="12" font-weight="bold" text-anchor="middle">START</text>
                `;
            }}
            drawCourse();

            document.getElementById('startBtn').addEventListener('click', startSimulation);
            document.getElementById('sim100Btn').addEventListener('click', run100Simulations);

            function startSimulation() {{
                if (animId) cancelAnimationFrame(animId);

                const group = document.getElementById('horsesGroup');
                const status = document.getElementById('statusBox');
                const resultsTitle = document.getElementById('resultsTitle');
                const resultsContent = document.getElementById('resultsContent');
                
                group.innerHTML = '';
                resultsTitle.innerText = "🏆 リアルタイム着順結果";
                resultsContent.innerHTML = '<div style="padding:10px; color:#8b949e;">⏱ ゲートが開きました！各馬一斉にスタート！</div>';

                const runners = horsesData.map((h, i) => {{
                    const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                    const wakuStyle = getWakuStyle(h.num, horsesData.length);
                    
                    const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                    const distPenalty = Math.max(0, (distDiff - 200) * 0.05);

                    const heavyMitigation = (h.heavy - 90) * 0.02;
                    const effectiveDrain = Math.max(0.8, goingDrain - heavyMitigation);

                    return {{
                        ...h,
                        laneOffset: laneOffset,
                        wakuStyle: wakuStyle,
                        progress: spec.startP,
                        targetProgress: spec.goalP,
                        staminaRem: (h.stamina - distPenalty) * 12,
                        effectiveDrain: effectiveDrain,
                        conditionMod: 0.94 + Math.random() * 0.12,
                        spurtPoint: spec.startP + (totalLapsProgress * (0.65 + Math.random() * 0.15)),
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
                            let curSpeed = h.speed * h.conditionMod * 0.000038;

                            if (h.progress >= h.spurtPoint) {{
                                if (h.style === "差し" || h.style === "追込") curSpeed *= 1.28;
                                else curSpeed *= 1.12;
                            }}

                            const pNorm = (h.progress % 1.0);
                            if (pNorm >= spec.slopeP[0] && pNorm <= spec.slopeP[1]) {{
                                curSpeed *= 0.88;
                            }}

                            h.staminaRem -= 0.04 * h.effectiveDrain;
                            if (h.staminaRem <= 0) curSpeed *= 0.65;

                            h.progress += curSpeed;

                            if (h.progress >= h.targetProgress) {{
                                h.progress = h.targetProgress;
                                h.finished = true;
                                finishedCount++;
                                h.rank = finishedCount;
                            }}
                        }}

                        const pt = getTrackPoint(h.progress, h.laneOffset);

                        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                        g.setAttribute('transform', `translate(${{pt.x}}, ${{pt.y}})`);
                        g.innerHTML = `
                            <circle cx="0" cy="0" r="8" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                            <text x="0" y="3" font-size="10" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                            <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${{h.name}}</text>
                        `;
                        group.appendChild(g);
                    }});

                    if (finishedCount === 0) {{
                        status.innerText = '🏇 ' + raceConfig.venue + ' ' + raceConfig.dist + 'm (' + raceConfig.going + ') 発走しました！';
                    }} else if (finishedCount < totalHorses) {{
                        status.innerText = '🏁 ' + finishedCount + '頭ゴール！激しい叩き合い！';
                    }} else {{
                        status.innerText = '🏆 全頭ゴールイン！確定着順を表示します';
                    }}

                    if (finishedCount < totalHorses) {{
                        animId = requestAnimationFrame(animate);
                    }} else {{
                        runners.sort((a, b) => a.rank - b.rank);
                        let html = `<div class="results-table-wrapper"><table class="results-table"><thead><tr><th>着順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>脚質</th><th>適性距離</th></tr></thead><tbody>`;
                        runners.forEach((h) => {{
                            const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                            html += `<tr><td class="rank-badge ${{rankClass}}">${{h.rank}}着</td><td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td><td style="text-align:left;"><strong>${{h.name}}</strong></td><td>${{h.style}}</td><td>${{h.opt_dist}}m</td></tr>`;
                        }});
                        html += '</tbody></table></div>';
                        resultsContent.innerHTML = html;
                    }}
                }}

                animId = requestAnimationFrame(animate);
            }}

            function run100Simulations() {{
                if (animId) cancelAnimationFrame(animId);

                const status = document.getElementById('statusBox');
                const resultsTitle = document.getElementById('resultsTitle');
                const resultsContent = document.getElementById('resultsContent');

                status.innerText = "⚡ 100回展開シミュレーションを計算中...";
                resultsTitle.innerText = "📊 100回シミュレーション総合推計（上位5頭分析）";

                const stats = {{}};
                horsesData.forEach(h => {{
                    stats[h.name] = {{
                        num: h.num,
                        name: h.name,
                        style: h.style,
                        wakuStyle: getWakuStyle(h.num, horsesData.length),
                        first: 0,
                        second: 0,
                        third: 0,
                        totalRank: 0,
                        totalScore: 0
                    }};
                }});

                const SIM_COUNT = 100;

                for (let sim = 0; sim < SIM_COUNT; sim++) {{
                    let raceRes = horsesData.map(h => {{
                        const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                        const distPenalty = Math.max(0, (distDiff - 200) * 0.05);
                        
                        const heavyMitigation = (h.heavy - 90) * 0.02;
                        const effectiveDrain = Math.max(0.8, goingDrain - heavyMitigation);
                        const stamina = (h.stamina - distPenalty) / effectiveDrain;

                        const randomMod = (Math.random() - 0.5) * 6;
                        let styleBonus = 0;
                        if (h.style === "逃げ") styleBonus = 1.5;
                        else if (h.style === "先行") styleBonus = 1.0;
                        else if (h.style === "差し") styleBonus = 2.0;
                        else if (h.style === "追込") styleBonus = 2.5;

                        const performanceScore = (h.speed * 0.45) + (stamina * 0.35) + (h.power * 0.2) + styleBonus + randomMod;
                        return {{ name: h.name, score: performanceScore }};
                    }});

                    raceRes.sort((a, b) => b.score - a.score);

                    raceRes.forEach((item, index) => {{
                        stats[item.name].totalScore += item.score;
                        stats[item.name].totalRank += (index + 1);
                        if (index === 0) stats[item.name].first++;
                        if (index === 1) stats[item.name].second++;
                        if (index === 2) stats[item.name].third++;
                    }});
                }}

                const rankedList = Object.values(stats).map(s => {{
                    const inTop3 = s.first + s.second + s.third;
                    const inTop3Rate = (inTop3 / SIM_COUNT) * 100;
                    const avgRank = (s.totalRank / SIM_COUNT).toFixed(2);
                    return {{ ...s, inTop3, inTop3Rate, avgRank }};
                }}).sort((a, b) => {{
                    if (b.inTop3Rate !== a.inTop3Rate) return b.inTop3Rate - a.inTop3Rate;
                    if (b.first !== a.first) return b.first - a.first;
                    return b.totalScore - a.totalScore;
                }});

                const top5 = rankedList.slice(0, 5);

                let html = `<div class="results-table-wrapper"><table class="results-table">
                    <thead>
                        <tr>
                            <th>予想順</th>
                            <th>馬番</th>
                            <th style="text-align:left;">馬名</th>
                            <th>脚質</th>
                            <th>1着</th>
                            <th>2着</th>
                            <th>3着</th>
                            <th>複勝率 (1~3着)</th>
                            <th>平均着順</th>
                        </tr>
                    </thead>
                    <tbody>`;

                top5.forEach((h, idx) => {{
                    const rankClass = idx === 0 ? 'rank-1' : idx === 1 ? 'rank-2' : idx === 2 ? 'rank-3' : '';
                    html += `<tr>
                        <td class="rank-badge ${{rankClass}}">${{idx + 1}}位</td>
                        <td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td>
                        <td style="text-align:left;"><strong>${{h.name}}</strong></td>
                        <td>${{h.style}}</td>
                        <td>${{h.first}}回</td>
                        <td>${{h.second}}回</td>
                        <td>${{h.third}}回</td>
                        <td><span class="rate-tag">${{h.inTop3Rate.toFixed(0)}}%</span></td>
                        <td><strong>${{h.avgRank}}着</strong></td>
                    </tr>`;
                }});

                html += '</tbody></table></div>';
                resultsContent.innerHTML = html;
                status.innerText = "✅ 100回展開シミュレーション完了（上位5頭）";
            }}
        </script>
    </body>
    </html>
    """
    # スクロールが見切れないようコンポーネントの高さを850pxに拡張
    st.components.v1.html(html_code, height=850, scrolling=True)

with tab_db:
  st.subheader(f"📊 2026最新データベース（全{len(df_all)}頭）")

  search_term = st.text_input("馬名・父名・母名・タイプで検索", "")
  df_filtered = df_all.copy()
  if search_term:
    df_filtered = df_filtered[
        df_filtered["horse"].str.contains(search_term, case=False)
        | df_filtered["sire"].str.contains(search_term, case=False)
        | df_filtered["dam"].str.contains(search_term, case=False)
        | df_filtered["race_type"].str.contains(search_term, case=False)
    ]

  st.dataframe(
      df_filtered[[
          "horse",
          "race_type",
          "style",
          "opt_dist",
          "wins_short",
          "wins_mid",
          "wins_long",
          "speed",
          "stamina",
          "power",
          "sire",
          "dam",
      ]].rename(columns={
          "horse": "馬名",
          "race_type": "タイプ",
          "style": "脚質",
          "opt_dist": "適性距離",
          "wins_short": "短距離(〜1600m)",
          "wins_mid": "中距離(1800〜2000m)",
          "wins_long": "長距離(2200m〜)",
          "speed": "スピード",
          "stamina": "スタミナ",
          "power": "パワー",
          "sire": "父",
          "dam": "母",
      }),
      use_container_width=True,
      hide_index=True,
  )
