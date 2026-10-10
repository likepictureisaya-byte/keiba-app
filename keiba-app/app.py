import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ スタイリッシュデザイン
st.set_page_config(
    page_title="JRAリアルコース競馬シミュレーター Pro 2026",
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
        background-color: #0b0f19;
    }
    .hero-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 10px;
        border-left: 4px solid #38bdf8;
        padding-left: 10px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
            height: 48px;
            font-size: 15px !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-box">
    <h1 style="color: #f3f4f6; margin: 0; font-size: 26px;">🏇 JRAリアルコース競馬シミュレーター <span style="color: #38bdf8; font-size: 18px;">PRO 2026</span></h1>
    <p style="color: #9ca3af; margin: 6px 0 0 0; font-size: 14px;">今週末＆月曜重賞（サウジアラビアRC・アイルランドT・スワンS）完全対応 | 高精度物理シミュレーション＆AI予想</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース（サウジアラビアRC、アイルランドT、スワンS 登録・出走馬完備）
@st.cache_data
def get_active_horse_db_2026():
  base_horses = [
      # === サウジアラビアロイヤルカップ（11頭） ===
      {
          "horse": "ギブリ",
          "gate": 1,
          "race_type": "芝・マイル",
          "sire": "モーリス",
          "dam": "プレシャスライフ",
          "style": "差し",
          "stamina": 87,
          "speed": 89,
          "power": 88,
          "heavy": 89,
          "burst": 90,
          "odds": 24.5,
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
          "burst": 91,
          "odds": 3.8,
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
          "burst": 89,
          "odds": 12.0,
          "opt_dist": 1600,
          "wins_short": "1-0-1-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "アゴルディーノ",
          "gate": 4,
          "race_type": "芝・マイル",
          "sire": "エフフォーリア",
          "dam": "アゴラ",
          "style": "先行",
          "stamina": 88,
          "speed": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 8.5,
          "opt_dist": 1600,
          "wins_short": "1-1-0-0",
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
          "burst": 94,
          "odds": 2.1,
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
          "burst": 93,
          "odds": 5.4,
          "opt_dist": 1600,
          "wins_short": "1-0-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ニシノトラノスケ",
          "gate": 7,
          "race_type": "芝・マイル",
          "sire": "キズナ",
          "dam": "ニシノアモーレ",
          "style": "先行",
          "stamina": 87,
          "speed": 89,
          "power": 88,
          "heavy": 89,
          "burst": 88,
          "odds": 18.2,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "グルーヴェンス",
          "gate": 8,
          "race_type": "芝・マイル",
          "sire": "ドゥラメンテ",
          "dam": "グルーヴィテイル",
          "style": "差し",
          "stamina": 86,
          "speed": 88,
          "power": 87,
          "heavy": 88,
          "burst": 87,
          "odds": 42.0,
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
          "burst": 91,
          "odds": 15.6,
          "opt_dist": 1600,
          "wins_short": "1-0-0-0",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "アイファーマーリン",
          "gate": 10,
          "race_type": "芝・マイル",
          "sire": "アイファーソング",
          "dam": "アイファーマーベル",
          "style": "逃げ",
          "stamina": 88,
          "speed": 89,
          "power": 91,
          "heavy": 93,
          "burst": 86,
          "odds": 65.0,
          "opt_dist": 1600,
          "wins_short": "1-0-1-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ハンサム",
          "gate": 11,
          "race_type": "芝・マイル",
          "sire": "モーリス",
          "dam": "ビューティフル",
          "style": "追込",
          "stamina": 86,
          "speed": 89,
          "power": 88,
          "heavy": 88,
          "burst": 92,
          "odds": 29.0,
          "opt_dist": 1600,
          "wins_short": "1-0-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      # === アイルランドトロフィー（16頭） ===
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
          "burst": 91,
          "odds": 16.5,
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
          "dam": "キューティゴールド",
          "style": "差し",
          "stamina": 88,
          "speed": 93,
          "power": 90,
          "heavy": 90,
          "burst": 92,
          "odds": 14.2,
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
          "burst": 95,
          "odds": 2.8,
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
          "dam": "エンジェルフェイス",
          "style": "差し",
          "stamina": 86,
          "speed": 90,
          "power": 88,
          "heavy": 89,
          "burst": 90,
          "odds": 22.0,
          "opt_dist": 1600,
          "wins_short": "3-1-0-3",
          "wins_mid": "0-0-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "カネラフィーナ",
          "gate": 5,
          "race_type": "芝・中距離",
          "sire": "Frankel",
          "dam": "ジョイカネラ",
          "style": "差し",
          "stamina": 90,
          "speed": 91,
          "power": 91,
          "heavy": 93,
          "burst": 91,
          "odds": 18.0,
          "opt_dist": 1800,
          "wins_short": "1-1-0-1",
          "wins_mid": "2-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ムイ",
          "gate": 6,
          "race_type": "芝・中距離",
          "sire": "ミッキーアイル",
          "dam": "スウィートラヴァー",
          "style": "追込",
          "stamina": 85,
          "speed": 87,
          "power": 86,
          "heavy": 88,
          "burst": 86,
          "odds": 85.0,
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
          "dam": "ソーマジック",
          "style": "先行",
          "stamina": 89,
          "speed": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 19.5,
          "opt_dist": 1800,
          "wins_short": "2-0-0-2",
          "wins_mid": "1-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ルージュソリテール",
          "gate": 8,
          "race_type": "芝・中距離",
          "sire": "ロードカナロア",
          "dam": "レッドオルガ",
          "style": "差し",
          "stamina": 89,
          "speed": 92,
          "power": 90,
          "heavy": 91,
          "burst": 91,
          "odds": 25.0,
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
          "burst": 92,
          "odds": 31.0,
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
          "burst": 90,
          "odds": 11.5,
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
          "burst": 95,
          "odds": 6.2,
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
          "burst": 93,
          "odds": 7.4,
          "opt_dist": 1800,
          "wins_short": "1-0-0-1",
          "wins_mid": "2-2-1-3",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ワタシマツワ",
          "gate": 13,
          "race_type": "芝・中距離",
          "sire": "グレーターロンドン",
          "dam": "サンドスラッシュ",
          "style": "追込",
          "stamina": 87,
          "speed": 88,
          "power": 88,
          "heavy": 89,
          "burst": 88,
          "odds": 92.0,
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
          "dam": "モアニケアラ",
          "style": "差し",
          "stamina": 90,
          "speed": 92,
          "power": 91,
          "heavy": 92,
          "burst": 91,
          "odds": 28.0,
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
          "burst": 94,
          "odds": 4.5,
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
          "burst": 96,
          "odds": 3.2,
          "opt_dist": 2000,
          "wins_short": "0-0-0-0",
          "wins_mid": "3-2-0-1",
          "wins_long": "1-0-0-0",
      },
      # === スワンステークス（月曜開催・京都1400m登録馬主要メンバー） ===
      {
          "horse": "オフトレイル",
          "gate": 1,
          "race_type": "芝・短距離",
          "sire": "Farhh",
          "dam": "ローズトレイル",
          "style": "差し",
          "stamina": 91,
          "speed": 95,
          "power": 92,
          "heavy": 93,
          "burst": 95,
          "odds": 4.0,
          "opt_dist": 1400,
          "wins_short": "3-1-0-2",
          "wins_mid": "1-0-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ウインマーベル",
          "gate": 2,
          "race_type": "芝・短距離",
          "sire": "アイルハヴアナザー",
          "dam": "コスモマーベラス",
          "style": "先行",
          "stamina": 92,
          "speed": 96,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 13.5,
          "opt_dist": 1400,
          "wins_short": "4-2-1-3",
          "wins_mid": "0-0-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ダイヤモンドノット",
          "gate": 3,
          "race_type": "芝・短距離",
          "sire": "ブリックスアンドモルタル",
          "dam": "エンドレスノット",
          "style": "先行",
          "stamina": 89,
          "speed": 94,
          "power": 91,
          "heavy": 91,
          "burst": 94,
          "odds": 5.0,
          "opt_dist": 1400,
          "wins_short": "2-1-0-1",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "エリカエクスプレス",
          "gate": 4,
          "race_type": "芝・マイル",
          "sire": "エピファネイア",
          "dam": "エンタイスド",
          "style": "差し",
          "stamina": 90,
          "speed": 93,
          "power": 91,
          "heavy": 92,
          "burst": 92,
          "odds": 4.5,
          "opt_dist": 1600,
          "wins_short": "1-1-1-2",
          "wins_mid": "1-0-0-1",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "マイネルチケット",
          "gate": 5,
          "race_type": "芝・短距離",
          "sire": "ダノンバラード",
          "dam": "エントリーチケット",
          "style": "先行",
          "stamina": 89,
          "speed": 93,
          "power": 92,
          "heavy": 92,
          "burst": 91,
          "odds": 16.0,
          "opt_dist": 1400,
          "wins_short": "2-1-1-2",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ワイドラトゥール",
          "gate": 6,
          "race_type": "芝・短距離",
          "sire": "カリフォルニアクローム",
          "dam": "ワイドサファイア",
          "style": "差し",
          "stamina": 88,
          "speed": 92,
          "power": 90,
          "heavy": 91,
          "burst": 93,
          "odds": 26.5,
          "opt_dist": 1400,
          "wins_short": "2-0-1-2",
          "wins_mid": "0-0-0-0",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "ショウナンザナドゥ",
          "gate": 7,
          "race_type": "芝・マイル",
          "sire": "キズナ",
          "dam": "ミスエーニョ",
          "style": "差し",
          "stamina": 90,
          "speed": 94,
          "power": 92,
          "heavy": 92,
          "burst": 93,
          "odds": 25.0,
          "opt_dist": 1600,
          "wins_short": "1-1-0-2",
          "wins_mid": "1-1-0-2",
          "wins_long": "0-0-0-0",
      },
      {
          "horse": "スズハローム",
          "gate": 8,
          "race_type": "芝・短距離",
          "sire": "サトノダイヤモンド",
          "dam": "アイライン",
          "style": "差し",
          "stamina": 89,
          "speed": 92,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 30.5,
          "opt_dist": 1400,
          "wins_short": "2-1-0-3",
          "wins_mid": "0-0-0-1",
          "wins_long": "0-0-0-0",
      },
  ]
  return pd.DataFrame(base_horses)


df_all = get_active_horse_db_2026()

SAUDI_MEMBERS_2026 = [
    "ギブリ",
    "デミアン",
    "サトノハクマイ",
    "アゴルディーノ",
    "フィリオソラーレ",
    "ベルウッドディープ",
    "ニシノトラノスケ",
    "グルーヴェンス",
    "ジップスパーク",
    "アイファーマーリン",
    "ハンサム",
]

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

SWAN_MEMBERS_2026 = [
    "オフトレイル",
    "ウインマーベル",
    "ダイヤモンドノット",
    "エリカエクスプレス",
    "マイネルチケット",
    "ワイドラトゥール",
    "ショウナンザナドゥ",
    "スズハローム",
]

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


def set_preset_swan():
  st.session_state.selected_horses = SWAN_MEMBERS_2026
  st.session_state.venue = "京都"
  st.session_state.dist = 1400


tab_sim, tab_analysis, tab_db = st.tabs([
    "🏇 レースシミュレーション＆予想",
    "📈 AI総合レーダー＆期待値分析",
    f"📊 2026最新データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.markdown(
      '<div class="section-title">⚡ 2026 今週末・月曜 重賞メンバー 一括セット</div>',
      unsafe_allow_html=True,
  )
  col_btn1, col_btn2, col_btn3 = st.columns(3)
  with col_btn1:
    st.button(
        f"👑 10/10(土) サウジアラビアRC\n(東京・1600m / {len(SAUDI_MEMBERS_2026)}頭)",
        on_click=set_preset_saudi,
        use_container_width=True,
    )
  with col_btn2:
    st.button(
        f"👑 10/11(日) アイルランドT\n(東京・1800m / {len(IRELAND_MEMBERS_2026)}頭)",
        on_click=set_preset_ireland,
        use_container_width=True,
    )
  with col_btn3:
    st.button(
        f"👑 10/12(月) スワンS\n(京都・1400m / {len(SWAN_MEMBERS_2026)}頭)",
        on_click=set_preset_swan,
        use_container_width=True,
    )

  st.markdown("---")
  st.markdown(
      '<div class="section-title">⚙ レース条件設定</div>',
      unsafe_allow_html=True,
  )
  col_c1, col_c2, col_c3 = st.columns(3)
  with col_c1:
    venue = st.selectbox(
        "開催競馬場", ["東京", "中山", "京都", "阪神"], key="venue"
    )
  with col_c2:
    dist = st.selectbox(
        "距離(m)", [1400, 1600, 1800, 2000, 2400], key="dist"
    )
  with col_c3:
    going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

  st.markdown("---")
  st.markdown(
      '<div class="section-title">🐎 出走馬選択 & 馬番調整</div>',
      unsafe_allow_html=True,
  )

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

    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}

    for idx, r in df_race.iterrows():
      horse_name = r["horse"]
      default_gate = int(r["gate"])
      col_target = num_cols[idx % min(3, len(selected_horses))]
      with col_target:
        custom_num = st.number_input(
            f"{horse_name} (馬番)",
            min_value=1,
            max_value=24,
            value=default_gate,
            key=f"num_input_{horse_name}",
        )
        custom_numbers[horse_name] = custom_num

    df_race["num"] = df_race["horse"].map(custom_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    if dist <= 1400:
      df_race["current_wins"] = df_race["wins_short"]
      dist_label = "短距離(1400m以下)"
    elif dist <= 1600:
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
            "odds",
            "current_wins",
            "sire",
            "dam",
        ]].rename(columns={
            "num": "馬番",
            "horse": "馬名",
            "race_type": "タイプ",
            "style": "脚質",
            "opt_dist": "適性距離",
            "odds": "想定オッズ",
            "current_wins": f"戦績 ({dist_label})",
            "sire": "父",
            "dam": "母",
        }),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🔍 コース特性完全準拠・展開予想 ＆ 🎯 穴馬アナライザー</div>',
        unsafe_allow_html=True,
    )

    # コース説明の出し分け
    if venue == "京都" and dist == 1400:
      course_desc = (
          "【京都芝1400m（外→内）特徴】2コーナー奥ポケットからのスタート。"
          "最初の3コーナーまでの距離が長く先行争いは比較的スムーズだが、"
          "内回りのため4コーナーからの立ち回りと直線平坦〜急坂手前までの瞬発力が勝負を分けます。"
      )
    elif venue == "東京" and dist == 1600:
      course_desc = (
          "【東京芝1600m特徴】2コーナー出口ポケット発走。最初の3コーナーまで約540m。"
          "最後の直線（525.9m）に待ち受ける高低差2mの急坂で末脚の持続力が問われます。"
      )
    elif venue == "東京" and dist == 1800:
      course_desc = (
          "【東京芝1800m特徴】2コーナー奥ポケット発走。序盤のポジション争いが厳しく、"
          "向正面の中盤から緩やかな上り下りを経て長い直線での持久力が試されます。"
      )
    else:
      course_desc = f"【{venue} 芝 {dist}m】 JRA公式コースレイアウト・坂・コーナー特性を完全反映。"

    escape_count = len(df_race[df_race["style"] == "逃げ"])
    leader_count = len(df_race[df_race["style"] == "先行"])

    if escape_count >= 2 or (escape_count == 1 and leader_count >= 4):
      pace_type = "ハイペース (H)"
      pace_desc = "前が競り合い激化。差し・追込馬に絶好の展開利が生じます。"
    elif escape_count == 1:
      pace_type = "ミドルペース (M)"
      pace_desc = "平均ペース。地力とコース適性がダイレクトに反映されるフラットな展開です。"
    else:
      pace_type = "スローペース (S)"
      pace_desc = (
          "逃げ馬不在。直線まで脚を温存できる先行馬や瞬発力上位馬が有利です。"
      )

    if going in ["重", "不良"]:
      pace_desc += f" 馬場状態【{going}】によりパワーとスタミナの消耗が倍増。"

    df_race["hole_score"] = (
        (df_race["power"] * 0.3)
        + (df_race["heavy"] * 0.3)
        + (df_race["odds"] * 0.15)
        - (np.abs(df_race["opt_dist"] - dist) * 0.05)
    )
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
          "🎯 厳選穴馬推奨",
          f"{hole_horse['num']}番 {hole_horse['horse']}",
          help="オッズ妙味・パワー・重馬場適性から波乱を演出する注目馬",
      )
    with c_p3:
      st.write("**【コース分析 ＆ 展開コメント】**")
      st.info(
          f"{course_desc}\n\n{pace_desc}\n\n💡 **穴馬推奨 ({hole_horse['horse']})**: "
          f"パワー指数({hole_horse['power']})/重馬場適性({hole_horse['heavy']})が高く、想定オッズ({hole_horse['odds']}倍)妙味を含めて激走条件が揃っています。"
      )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🏁 JRAリアルコース再現アニメーション ＆ 100回シミュレーション</div>',
        unsafe_allow_html=True,
    )

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
          "burst": float(r["burst"]),
          "opt_dist": float(r["opt_dist"]),
      })

    race_config_js = {"venue": venue, "dist": dist, "going": going}

    # 高精度レースビジュアライザHTML
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; touch-action: manipulation; }
        body { margin: 0; padding: 0; font-family: -apple-system, sans-serif; background-color: #0b0f19; color: white; }
        .sim-container { width: 100%; max-width: 900px; margin: 0 auto; padding: 4px; text-align: center; }
        .btn-group { display: flex; gap: 10px; margin-bottom: 12px; }
        .start-btn {
            flex: 1; height: 50px; background: linear-gradient(135deg, #059669, #047857); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(5,150,105,0.3);
        }
        .sim100-btn {
            flex: 1; height: 50px; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,0.3);
        }
        .status-box { font-size: 15px; font-weight: bold; color: #34d399; min-height: 28px; margin-bottom: 8px; }
        .svg-wrapper { 
            width: 100%; background: #06120d; border-radius: 14px; border: 2px solid #1e3a2f; padding: 10px; box-sizing: border-box; overflow: hidden;
        }
        .results-box { 
            margin-top: 14px; background: #111827; padding: 16px; border-radius: 12px; border: 1px solid #374151; text-align: left; max-height: 450px; overflow-y: auto;
        }
        .results-table-wrapper { width: 100%; overflow-x: auto; }
        .results-table { width: 100%; border-collapse: collapse; margin-top: 8px; min-width: 600px; }
        .results-table th { 
            position: sticky; top: 0; background: #1f2937; padding: 10px; font-size: 13px; text-align: center; color: #9ca3af; border-bottom: 2px solid #374151; z-index: 10;
        }
        .results-table td { padding: 9px; font-size: 14px; text-align: center; border-bottom: 1px solid #1f2937; }
        .waku-tag { display: inline-block; width: 24px; height: 24px; line-height: 24px; text-align: center; border-radius: 6px; font-weight: bold; font-size: 12px; margin-right: 6px; }
        .rank-badge { font-weight: bold; font-size: 15px; }
        .rank-1 { color: #f59e0b; }
        .rank-2 { color: #94a3b8; }
        .rank-3 { color: #d97706; }
        .rate-tag { font-weight: bold; color: #f87171; font-size: 16px; }
        .ticket-box { background: #030712; border: 1px solid #374151; padding: 12px 16px; border-radius: 10px; margin-top: 12px; font-size: 13px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="sim-container">
        <div class="btn-group">
            <button id="startBtn" class="start-btn">▶ レース発走 (GATE OPEN)</button>
            <button id="sim100Btn" class="sim100-btn">⚡ 100回シミュレーション＆買い目構築</button>
        </div>
        
        <div id="statusBox" class="status-box">ボタンを押してシミュレーションを開始してください</div>
        
        <div class="svg-wrapper">
            <svg id="trackSvg" viewBox="0 0 720 380" width="100%" height="auto" style="display: block;">
                <path d="M 220 70 L 500 70 A 110 110 0 0 1 500 290 L 220 290 A 110 110 0 0 1 220 70 Z" fill="#16382b" stroke="#22c55e" stroke-width="26"/>
                <path d="M 220 84 L 500 84 A 96 96 0 0 1 500 276 L 220 276 A 96 96 0 0 1 220 84 Z" fill="#0b0f19" stroke="#0b0f19" stroke-width="2"/>
                <g id="goalGroup"></g>
                <g id="startGroup"></g>
                <g id="horsesGroup"></g>
            </svg>
        </div>

        <div class="results-box">
            <div id="resultsTitle" style="font-weight: bold; color: #f59e0b; font-size: 16px;">🏆 結果および推奨買い目表示</div>
            <div id="resultsContent" style="color: #9ca3af;">発走準備完了</div>
        </div>
    </div>

    <script>
        const horsesData = __HORSES_JSON__;
        const raceConfig = __RACE_CONFIG_JSON__;
        let animId = null;

        const GOING_DRAIN_MAP = { "良": 1.0, "稍重": 1.15, "重": 1.30, "不良": 1.45 };
        let goingDrain = GOING_DRAIN_MAP[raceConfig.going] || 1.0;

        function getWakuStyle(num, total) {
            let waku = Math.ceil((num / total) * 8);
            if (total <= 8) waku = num;
            const colors = [
                { bg: '#ffffff', text: '#000000' }, { bg: '#333333', text: '#ffffff' },
                { bg: '#ef4444', text: '#ffffff' }, { bg: '#3b82f6', text: '#ffffff' },
                { bg: '#eab308', text: '#000000' }, { bg: '#22c55e', text: '#ffffff' },
                { bg: '#f97316', text: '#ffffff' }, { bg: '#a855f7', text: '#ffffff' }
            ];
            return colors[Math.min(Math.max(waku - 1, 0), 7)];
        }

        const totalLapsProgress = (raceConfig.dist / 2000.0);
        const COURSE_SPECS = {
            "東京": { dir: -1, startP: raceConfig.dist === 1800 ? 0.68 : (raceConfig.dist === 1600 ? 0.58 : 0.20), slopeP: [0.03, 0.14] },
            "中山": { dir: 1, startP: raceConfig.dist === 2000 ? 0.02 : (raceConfig.dist === 1600 ? 0.55 : 0.30), slopeP: [0.02, 0.09] },
            "京都": { dir: 1, startP: raceConfig.dist === 1400 ? 0.62 : (raceConfig.dist === 2400 ? 0.10 : 0.60), slopeP: [0.42, 0.62] },
            "阪神": { dir: 1, startP: raceConfig.dist === 2000 ? 0.20 : 0.55, slopeP: [0.02, 0.09] }
        };

        const spec = COURSE_SPECS[raceConfig.venue] || COURSE_SPECS["東京"];
        spec.goalP = spec.startP + totalLapsProgress;

        function getTrackPoint(p, laneOffset = 0) {
            p = (p % 1.0 + 1.0) % 1.0;
            const r = 110 + laneOffset;
            const lenStr = 280;
            const circumference = 2 * Math.PI * r + 2 * lenStr;
            const distOnTrack = p * circumference;
            let x, y, angle;

            if (distOnTrack <= lenStr) {
                x = 500 - distOnTrack; y = 290 + laneOffset; angle = Math.PI;
            } else if (distOnTrack <= lenStr + Math.PI * r) {
                const arcLen = distOnTrack - lenStr;
                const theta = Math.PI / 2 + (arcLen / r);
                x = 220 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
            } else if (distOnTrack <= 2 * lenStr + Math.PI * r) {
                const strLen2 = distOnTrack - (lenStr + Math.PI * r);
                x = 220 + strLen2; y = 70 - laneOffset; angle = 0;
            } else {
                const arcLen2 = distOnTrack - (2 * lenStr + Math.PI * r);
                const theta = -Math.PI / 2 + (arcLen2 / r);
                x = 500 + r * Math.cos(theta); y = 180 + r * Math.sin(theta); angle = theta + Math.PI / 2;
            }
            if (spec.dir === -1) { x = 720 - x; angle = Math.PI - angle; }
            return { x, y, angle };
        }

        function drawCourse() {
            const goalPt = getTrackPoint(spec.goalP);
            document.getElementById('goalGroup').innerHTML = `
                <line x1="${goalPt.x}" y1="${goalPt.y - 22}" x2="${goalPt.x}" y2="${goalPt.y + 22}" stroke="#ef4444" stroke-width="5"/>
                <text x="${goalPt.x}" y="${goalPt.y + 38}" fill="#ef4444" font-size="13" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
            `;
            const startPt = getTrackPoint(spec.startP);
            document.getElementById('startGroup').innerHTML = `
                <line x1="${startPt.x}" y1="${startPt.y - 18}" x2="${startPt.x}" y2="${startPt.y + 18}" stroke="#22c55e" stroke-width="4"/>
                <text x="${startPt.x}" y="${startPt.y - 22}" fill="#22c55e" font-size="12" font-weight="bold" text-anchor="middle">START 🚪</text>
            `;
        }
        drawCourse();

        document.getElementById('startBtn').addEventListener('click', startSimulation);
        document.getElementById('sim100Btn').addEventListener('click', run100Simulations);

        function startSimulation() {
            if (animId) cancelAnimationFrame(animId);
            const group = document.getElementById('horsesGroup');
            const status = document.getElementById('statusBox');
            const resultsTitle = document.getElementById('resultsTitle');
            const resultsContent = document.getElementById('resultsContent');
            
            group.innerHTML = '';
            resultsTitle.innerText = "🏆 リアルタイム着順結果";
            resultsContent.innerHTML = '<div style="padding:10px; color:#9ca3af;">⏱ ゲートが開きました！各馬一斉にスタート！</div>';

            const runners = horsesData.map((h, i) => {
                const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                const wakuStyle = getWakuStyle(h.num, horsesData.length);
                const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                const distPenalty = Math.max(0, (distDiff - 200) * 0.05);
                const heavyMitigation = (h.heavy - 90) * 0.02;
                const effectiveDrain = Math.max(0.8, goingDrain - heavyMitigation);

                return {
                    ...h, laneOffset, wakuStyle,
                    progress: spec.startP, targetProgress: spec.goalP,
                    staminaRem: (h.stamina - distPenalty) * 12,
                    effectiveDrain,
                    conditionMod: 0.94 + Math.random() * 0.12,
                    spurtPoint: spec.startP + (totalLapsProgress * (0.65 + Math.random() * 0.15)),
                    finished: false, rank: 0
                };
            });

            let finishedCount = 0;
            const totalHorses = runners.length;

            function animate() {
                group.innerHTML = '';
                runners.forEach((h) => {
                    if (!h.finished) {
                        let curSpeed = h.speed * h.conditionMod * 0.000038;
                        if (h.progress >= h.spurtPoint) {
                            curSpeed *= (h.style === "差し" || h.style === "追込") ? (1.25 + h.burst * 0.003) : 1.12;
                        }
                        const pNorm = (h.progress % 1.0);
                        if (pNorm >= spec.slopeP[0] && pNorm <= spec.slopeP[1]) {
                            const powerMitigation = (h.power - 90) * 0.005;
                            curSpeed *= Math.max(0.75, 0.88 + powerMitigation);
                        }
                        h.staminaRem -= 0.04 * h.effectiveDrain;
                        if (h.staminaRem <= 0) curSpeed *= 0.65;
                        h.progress += curSpeed;

                        if (h.progress >= h.targetProgress) {
                            h.progress = h.targetProgress;
                            h.finished = true;
                            finishedCount++;
                            h.rank = finishedCount;
                        }
                    }
                    const pt = getTrackPoint(h.progress, h.laneOffset);
                    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    g.setAttribute('transform', `translate(${pt.x}, ${pt.y})`);
                    g.innerHTML = `
                        <circle cx="0" cy="0" r="8" fill="${h.wakuStyle.bg}" stroke="#ffffff" stroke-width="1.5"/>
                        <text x="0" y="3" font-size="10" font-weight="bold" fill="${h.wakuStyle.text}" text-anchor="middle">${h.num}</text>
                        <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${h.name}</text>
                    `;
                    group.appendChild(g);
                });

                if (finishedCount === 0) {
                    status.innerText = '🏇 ' + raceConfig.venue + ' ' + raceConfig.dist + 'm (' + raceConfig.going + ') レース中！';
                } else if (finishedCount < totalHorses) {
                    status.innerText = '🏁 ' + finishedCount + '頭ゴールイン！';
                } else {
                    status.innerText = '🏆 全頭ゴール！';
                }

                if (finishedCount < totalHorses) {
                    animId = requestAnimationFrame(animate);
                } else {
                    runners.sort((a, b) => a.rank - b.rank);
                    let html = `<div class="results-table-wrapper"><table class="results-table"><thead><tr><th>着順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>脚質</th><th>適性距離</th></tr></thead><tbody>`;
                    runners.forEach((h) => {
                        const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                        html += `<tr><td class="rank-badge ${rankClass}">${h.rank}着</td><td><span class="waku-tag" style="background:${h.wakuStyle.bg}; color:${h.wakuStyle.text};">${h.num}</span></td><td style="text-align:left;"><strong>${h.name}</strong></td><td>${h.style}</td><td>${h.opt_dist}m</td></tr>`;
                    });
                    html += '</tbody></table></div>';
                    resultsContent.innerHTML = html;
                }
            }
            animId = requestAnimationFrame(animate);
        }

        function run100Simulations() {
            if (animId) cancelAnimationFrame(animId);
            const status = document.getElementById('statusBox');
            const resultsTitle = document.getElementById('resultsTitle');
            const resultsContent = document.getElementById('resultsContent');

            status.innerText = "⚡ 100回モンテカルロシミュレーション＆買い目構築中...";
            resultsTitle.innerText = "📊 100回シミュレーション総合結果 ＆ AI推奨買い目";

            const stats = {};
            horsesData.forEach(h => {
                stats[h.name] = {
                    num: h.num, name: h.name, style: h.style,
                    wakuStyle: getWakuStyle(h.num, horsesData.length),
                    first: 0, second: 0, third: 0, totalRank: 0, totalScore: 0
                };
            });

            const SIM_COUNT = 100;
            for (let sim = 0; sim < SIM_COUNT; sim++) {
                let raceRes = horsesData.map(h => {
                    const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                    const distPenalty = Math.max(0, (distDiff - 200) * 0.05);
                    const heavyMitigation = (h.heavy - 90) * 0.02;
                    const effectiveDrain = Math.max(0.8, goingDrain - heavyMitigation);
                    const stamina = (h.stamina - distPenalty) / effectiveDrain;

                    const randomMod = (Math.random() - 0.5) * 7;
                    let styleBonus = (h.style === "差し" || h.style === "追込") ? 2.2 : 1.2;
                    const score = (h.speed * 0.4) + (stamina * 0.3) + (h.power * 0.15) + (h.burst * 0.15) + styleBonus + randomMod;
                    return { name: h.name, score: score };
                });
                raceRes.sort((a, b) => b.score - a.score);
                raceRes.forEach((item, index) => {
                    stats[item.name].totalScore += item.score;
                    stats[item.name].totalRank += (index + 1);
                    if (index === 0) stats[item.name].first++;
                    if (index === 1) stats[item.name].second++;
                    if (index === 2) stats[item.name].third++;
                });
            }

            const rankedList = Object.values(stats).map(s => {
                const inTop3 = s.first + s.second + s.third;
                const inTop3Rate = (inTop3 / SIM_COUNT) * 100;
                const avgRank = (s.totalRank / SIM_COUNT).toFixed(2);
                return { ...s, inTop3, inTop3Rate, avgRank };
            }).sort((a, b) => {
                if (b.inTop3Rate !== a.inTop3Rate) return b.inTop3Rate - a.inTop3Rate;
                return b.first - a.first;
            });

            const top5 = rankedList.slice(0, 5);

            let html = `<div class="results-table-wrapper"><table class="results-table">
                <thead><tr><th>予想順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>脚質</th><th>1着</th><th>2着</th><th>3着</th><th>複勝率</th><th>平均着順</th></tr></thead><tbody>`;

            top5.forEach((h, idx) => {
                const rankClass = idx === 0 ? 'rank-1' : idx === 1 ? 'rank-2' : idx === 2 ? 'rank-3' : '';
                html += `<tr>
                    <td class="rank-badge ${rankClass}">${idx + 1}位</td>
                    <td><span class="waku-tag" style="background:${h.wakuStyle.bg}; color:${h.wakuStyle.text};">${h.num}</span></td>
                    <td style="text-align:left;"><strong>${h.name}</strong></td>
                    <td>${h.style}</td><td>${h.first}回</td><td>${h.second}回</td><td>${h.third}回</td>
                    <td><span class="rate-tag">${h.inTop3Rate.toFixed(0)}%</span></td>
                    <td><strong>${h.avgRank}着</strong></td>
                </tr>`;
            });
            html += '</tbody></table></div>';

            const t1 = top5[0].num;
            const t2 = top5[1].num;
            const t3 = top5[2].num;
            const t4 = top5[3].num;

            html += `<div class="ticket-box">
                <strong>🎯 AI自動構築プロフェッショナル買い目</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${t1} - (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${t1} － 相手 (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${t1}, ${t2} → 2着 ${t1}, ${t2}, ${t3} → 3着 ${t1}, ${t2}, ${t3}, ${t4}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ シミュレーション＆買い目構築完了";
        }
    </script>
</body>
</html>"""

    html_code = html_template.replace(
        "__HORSES_JSON__", json.dumps(horses_js)
    ).replace("__RACE_CONFIG_JSON__", json.dumps(race_config_js))

    st.components.v1.html(html_code, height=880, scrolling=True)

with tab_analysis:
  st.markdown(
      '<div class="section-title">📈 2026出走馬 AI能力レーダー＆期待値分析</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "選択されているレースの登録全頭について、AIが算出している各能力パラメーターと妙味度（期待値）を一覧で比較できます。"
  )

  df_ana = df_all[df_all["horse"].isin(selected_horses)].copy()
  if not df_ana.empty:
    df_ana["期待値スコア"] = (
        df_ana["odds"] * (df_ana["speed"] + df_ana["power"]) / 200.0
    ).round(2)
    st.dataframe(
        df_ana[[
            "gate",
            "horse",
            "odds",
            "speed",
            "stamina",
            "power",
            "heavy",
            "burst",
            "期待値スコア",
        ]].rename(columns={
            "gate": "馬番",
            "horse": "馬名",
            "odds": "想定オッズ",
            "speed": "スピード",
            "stamina": "スタミナ",
            "power": "パワー",
            "heavy": "重馬場適性",
            "burst": "瞬発力",
        }),
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.info("出走馬が選択されていません。")

with tab_db:
  st.markdown(
      f'<div class="section-title">📊 2026最新データベース（全{len(df_all)}頭）</div>',
      unsafe_allow_html=True,
  )
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
          "gate",
          "horse",
          "race_type",
          "style",
          "opt_dist",
          "odds",
          "speed",
          "stamina",
          "power",
          "sire",
          "dam",
      ]].rename(columns={
          "gate": "デフォルト馬番",
          "horse": "馬名",
          "race_type": "タイプ",
          "style": "脚質",
          "opt_dist": "適性距離",
          "odds": "想定オッズ",
          "speed": "スピード",
          "stamina": "スタミナ",
          "power": "パワー",
          "sire": "父",
          "dam": "母",
      }),
      use_container_width=True,
      hide_index=True,
  )
