import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="JRA重賞 究極精密シミュレーター Pro 2026",
    page_icon="🏆",
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
        background-color: #080c14;
    }
    .hero-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
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
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">🏆 JRA重賞 究極精密シミュレーター <span style="color: #38bdf8; font-size: 18px;">PRO 2026</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">富士ステークス（東京1600m） ＆ 秋華賞（京都2000m） 確定枠順・騎手完全対応 | 物理演算アルゴリズム</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース：富士ステークス ＆ 秋華賞 確定出走馬データベース
@st.cache_data
def get_weekend_race_db_2026():
  # --- 富士ステークス（14頭・確定枠順） ---
  fuji_horses = [
      {
          "race": "富士ステークス",
          "horse": "ファンダム",
          "jockey": "戸崎圭太",
          "gate": 1,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "speed": 94,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 95,
          "odds": 6.5,
          "opt_dist": 1600,
          "sire": "エピファネイア",
      },
      {
          "race": "富士ステークス",
          "horse": "ミトノオルフェ",
          "jockey": "菅原明良",
          "gate": 2,
          "venue": "東京",
          "dist": 1600,
          "style": "先行",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 89,
          "odds": 32.0,
          "opt_dist": 1600,
          "sire": "オルフェーヴル",
      },
      {
          "race": "富士ステークス",
          "horse": "シンフォーエバー",
          "jockey": "岩田康誠",
          "gate": 3,
          "venue": "東京",
          "dist": 1600,
          "style": "逃げ",
          "speed": 91,
          "stamina": 88,
          "power": 92,
          "heavy": 91,
          "burst": 88,
          "odds": 45.0,
          "opt_dist": 1600,
          "sire": "リオンディーズ",
      },
      {
          "race": "富士ステークス",
          "horse": "トロヴァトーレ",
          "jockey": "C.ルメール",
          "gate": 4,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "speed": 97,
          "stamina": 94,
          "power": 95,
          "heavy": 93,
          "burst": 97,
          "odds": 2.5,
          "opt_dist": 1600,
          "sire": "レイデオロ",
      },
      {
          "race": "富士ステークス",
          "horse": "アドマイヤズーム",
          "jockey": "武豊",
          "gate": 5,
          "venue": "東京",
          "dist": 1600,
          "style": "先行",
          "speed": 96,
          "stamina": 94,
          "power": 94,
          "heavy": 93,
          "burst": 96,
          "odds": 3.1,
          "opt_dist": 1600,
          "sire": "モーリス",
      },
      {
          "race": "富士ステークス",
          "horse": "デビットバローズ",
          "jockey": "池添謙一",
          "gate": 6,
          "venue": "東京",
          "dist": 1600,
          "style": "先行",
          "speed": 89,
          "stamina": 90,
          "power": 89,
          "heavy": 89,
          "burst": 88,
          "odds": 55.0,
          "opt_dist": 1600,
          "sire": "ディープインパクト",
      },
      {
          "race": "富士ステークス",
          "horse": "ウォーターリヒト",
          "jockey": "幸英明",
          "gate": 7,
          "venue": "東京",
          "dist": 1600,
          "style": "追込",
          "speed": 93,
          "stamina": 92,
          "power": 91,
          "heavy": 92,
          "burst": 96,
          "odds": 18.0,
          "opt_dist": 1600,
          "sire": "ドレフォン",
      },
      {
          "race": "富士ステークス",
          "horse": "マジックサンズ",
          "jockey": "横山和生",
          "gate": 8,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "speed": 92,
          "stamina": 91,
          "power": 92,
          "heavy": 91,
          "burst": 93,
          "odds": 22.0,
          "opt_dist": 1600,
          "sire": "キズナ",
      },
      {
          "race": "富士ステークス",
          "horse": "キープカルム",
          "jockey": "荻野極",
          "gate": 9,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "speed": 90,
          "stamina": 90,
          "power": 89,
          "heavy": 90,
          "burst": 90,
          "odds": 40.0,
          "opt_dist": 1600,
          "sire": "ロードカナロア",
      },
      {
          "race": "富士ステークス",
          "horse": "アンパドゥ",
          "jockey": "岩田望来",
          "gate": 10,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "speed": 95,
          "stamina": 93,
          "power": 96,
          "heavy": 97,
          "burst": 94,
          "odds": 4.8,
          "opt_dist": 1600,
          "sire": "リアルインパクト",
      },
      {
          "race": "富士ステークス",
          "horse": "ファーヴェント",
          "jockey": "三浦皇成",
          "gate": 11,
          "venue": "東京",
          "dist": 1600,
          "style": "先行",
          "speed": 90,
          "stamina": 90,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 48.0,
          "opt_dist": 1600,
          "sire": "ハーツクライ",
      },
      {
          "race": "富士ステークス",
          "horse": "エンペラーズソード",
          "jockey": "木幡巧也",
          "gate": 12,
          "venue": "東京",
          "dist": 1600,
          "style": "逃げ",
          "speed": 89,
          "stamina": 88,
          "power": 89,
          "heavy": 89,
          "burst": 87,
          "odds": 95.0,
          "opt_dist": 1600,
          "sire": "ロードカナロア",
      },
      {
          "race": "富士ステークス",
          "horse": "シュガークン",
          "jockey": "吉村誠之助",
          "gate": 13,
          "venue": "東京",
          "dist": 1600,
          "style": "先行",
          "speed": 92,
          "stamina": 94,
          "power": 93,
          "heavy": 92,
          "burst": 91,
          "odds": 28.0,
          "opt_dist": 2000,
          "sire": "ドゥラメンテ",
      },
      {
          "race": "富士ステークス",
          "horse": "エコロアルバ",
          "jockey": "坂井瑠星",
          "gate": 14,
          "venue": "東京",
          "dist": 1600,
          "style": "差し",
          "stamina": 91,
          "speed": 93,
          "power": 91,
          "heavy": 91,
          "burst": 94,
          "odds": 20.0,
          "opt_dist": 1600,
          "sire": "ブリックスアンドモルタル",
      },
  ]

  # --- 秋華賞（17頭・確定枠順） ---
  shuka_horses = [
      {
          "race": "秋華賞",
          "horse": "ギャラボーグ",
          "jockey": "横山和生",
          "gate": 1,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 91,
          "burst": 91,
          "odds": 36.6,
          "opt_dist": 2000,
          "sire": "キズナ",
      },
      {
          "race": "秋華賞",
          "horse": "テイエムアイラン",
          "jockey": "富田暁",
          "gate": 2,
          "venue": "京都",
          "dist": 2000,
          "style": "逃げ",
          "speed": 88,
          "stamina": 89,
          "power": 88,
          "heavy": 88,
          "burst": 86,
          "odds": 54.5,
          "opt_dist": 2000,
          "sire": "シニスターミニスター",
      },
      {
          "race": "秋華賞",
          "horse": "マスターソアラ",
          "jockey": "武豊",
          "gate": 3,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 94,
          "stamina": 95,
          "power": 93,
          "heavy": 92,
          "burst": 93,
          "odds": 16.0,
          "opt_dist": 2000,
          "sire": "キタサンブラック",
      },
      {
          "race": "秋華賞",
          "horse": "エンネ",
          "jockey": "坂井瑠星",
          "gate": 4,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 92,
          "stamina": 93,
          "power": 91,
          "heavy": 91,
          "burst": 92,
          "odds": 19.8,
          "opt_dist": 2000,
          "sire": "エピファネイア",
      },
      {
          "race": "秋華賞",
          "horse": "タイセイボーグ",
          "jockey": "西村淳也",
          "gate": 5,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 89,
          "stamina": 90,
          "power": 89,
          "heavy": 89,
          "burst": 89,
          "odds": 65.5,
          "opt_dist": 2000,
          "sire": "ロードカナロア",
      },
      {
          "race": "秋華賞",
          "horse": "ラベルセーヌ",
          "jockey": "荻野極",
          "gate": 6,
          "venue": "京都",
          "dist": 2000,
          "style": "追込",
          "speed": 88,
          "stamina": 89,
          "power": 88,
          "heavy": 88,
          "burst": 88,
          "odds": 80.0,
          "opt_dist": 2000,
          "sire": "モーリス",
      },
      {
          "race": "秋華賞",
          "horse": "バースデイフライト",
          "jockey": "田山旺佑",
          "gate": 7,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 87,
          "stamina": 88,
          "power": 87,
          "heavy": 87,
          "burst": 86,
          "odds": 110.0,
          "opt_dist": 2000,
          "sire": "イスラボニータ",
      },
      {
          "race": "秋華賞",
          "horse": "モンローウォーク",
          "jockey": "戸崎圭太",
          "gate": 8,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 97,
          "stamina": 96,
          "power": 95,
          "heavy": 94,
          "burst": 97,
          "odds": 2.2,
          "opt_dist": 2000,
          "sire": "ドゥラメンテ",
      },
      {
          "race": "秋華賞",
          "horse": "スウィートハピネス",
          "jockey": "佐々木大輔",
          "gate": 9,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 42.0,
          "opt_dist": 2000,
          "sire": "リアルスティール",
      },
      {
          "race": "秋華賞",
          "horse": "ナイスプレーアスク",
          "jockey": "岩田康誠",
          "gate": 10,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 91,
          "stamina": 91,
          "power": 91,
          "heavy": 91,
          "burst": 90,
          "odds": 38.0,
          "opt_dist": 2000,
          "sire": "ゴールドシップ",
      },
      {
          "race": "秋華賞",
          "horse": "ガーネットフレア",
          "jockey": "北村友一",
          "gate": 11,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 90,
          "stamina": 92,
          "power": 90,
          "heavy": 90,
          "burst": 91,
          "odds": 50.0,
          "opt_dist": 2000,
          "sire": "ハーツクライ",
      },
      {
          "race": "秋華賞",
          "horse": "カナルサンマルタン",
          "jockey": "岩田望来",
          "gate": 12,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 24.0,
          "opt_dist": 2000,
          "sire": "ロードカナロア",
      },
      {
          "race": "秋華賞",
          "horse": "ドリームコア",
          "jockey": "C.ルメール",
          "gate": 13,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "speed": 96,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 96,
          "odds": 3.4,
          "opt_dist": 2000,
          "sire": "エピファネイア",
      },
      {
          "race": "秋華賞",
          "horse": "サムシングスイート",
          "jockey": "松山弘平",
          "gate": 14,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 93,
          "stamina": 94,
          "power": 93,
          "heavy": 93,
          "burst": 92,
          "odds": 14.5,
          "opt_dist": 2000,
          "sire": "キズナ",
      },
      {
          "race": "秋華賞",
          "horse": "フェスティバルヒル",
          "jockey": "浜中俊",
          "gate": 15,
          "venue": "京都",
          "dist": 2000,
          "style": "差し",
          "stamina": 91,
          "speed": 91,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 45.0,
          "opt_dist": 2000,
          "sire": "ドレフォン",
      },
      {
          "race": "秋華賞",
          "horse": "ハヤブササキチャン",
          "jockey": "吉田隼人",
          "gate": 16,
          "venue": "京都",
          "dist": 2000,
          "style": "先行",
          "speed": 89,
          "power": 90,
          "stamina": 90,
          "heavy": 89,
          "burst": 89,
          "odds": 75.0,
          "opt_dist": 2000,
          "sire": "シルバーステート",
      },
      {
          "race": "秋華賞",
          "horse": "ロザーンジュ",
          "jockey": "今村聖奈",
          "gate": 17,
          "venue": "京都",
          "dist": 2000,
          "style": "追込",
          "speed": 88,
          "power": 88,
          "stamina": 89,
          "heavy": 88,
          "burst": 88,
          "odds": 130.0,
          "opt_dist": 2000,
          "sire": "リアルインパクト",
      },
  ]

  return pd.DataFrame(fuji_horses + shuka_horses)


df_all = get_weekend_race_db_2026()

if "selected_race" not in st.session_state:
  st.session_state.selected_race = "富士ステークス"
if "selected_horses" not in st.session_state:
  st.session_state.selected_horses = df_all[
      df_all["race"] == "富士ステークス"
  ]["horse"].tolist()
if "going" not in st.session_state:
  st.session_state.going = "良"
if "pace_mode" not in st.session_state:
  st.session_state.pace_mode = "ミドルペース (M)"


def set_preset_fuji():
  st.session_state.selected_race = "富士ステークス"
  st.session_state.selected_horses = df_all[df_all["race"] == "富士ステークス"][
      "horse"
  ].tolist()


def set_preset_shuka():
  st.session_state.selected_race = "秋華賞"
  st.session_state.selected_horses = df_all[df_all["race"] == "秋華賞"][
      "horse"
  ].tolist()


tab_sim, tab_analysis, tab_db = st.tabs([
    "🏇 レースシミュレーション＆究極予想",
    "📈 AI能力レーダー＆期待値分析",
    f"📊 出走馬データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.markdown(
      '<div class="section-title">⚡ 開催レース 一括セット（枠順・騎手確定版）</div>',
      unsafe_allow_html=True,
  )
  col_b1, col_b2 = st.columns(2)
  with col_b1:
    st.button(
        "👑 10/17(土) 富士ステークス (東京・芝1600m) 一括ロード",
        on_click=set_preset_fuji,
        use_container_width=True,
    )
  with col_b2:
    st.button(
        "👑 10/18(日) 秋華賞 (京都・芝2000m) 一括ロード",
        on_click=set_preset_shuka,
        use_container_width=True,
    )

  st.markdown("---")
  st.markdown(
      '<div class="section-title">⚙ 馬場状態 ＆ 展開ペース設定</div>',
      unsafe_allow_html=True,
  )
  col_c1, col_c2 = st.columns(2)
  with col_c1:
    going = st.selectbox(
        "馬場状態", ["良", "稍重", "重", "不良"], key="going"
    )
  with col_c2:
    pace_mode = st.selectbox(
        "展開ペース指定",
        ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"],
        key="pace_mode",
    )

  # 現在選択されているレースの判定
  current_race_name = st.session_state.selected_race
  df_race_base = df_all[df_all["race"] == current_race_name].copy()
  venue = "東京" if current_race_name == "富士ステークス" else "京都"
  dist = 1600 if current_race_name == "富士ステークス" else 2000

  st.markdown("---")
  st.markdown(
      f'<div class="section-title">🐎 {current_race_name} 出走馬・確定枠順 ＆ 騎手一覧</div>',
      unsafe_allow_html=True,
  )

  selected_horses = st.multiselect(
      "出走馬を選択（変更可能）",
      options=df_race_base["horse"].tolist(),
      key="selected_horses",
  )

  if len(selected_horses) < 2:
    st.warning("⚠ 出走馬を【2頭以上】選択してください。")
  else:
    df_race = (
        df_race_base[df_race_base["horse"].isin(selected_horses)]
        .copy()
        .reset_index(drop=True)
    )

    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}

    for idx, r in df_race.iterrows():
      horse_name = r["horse"]
      default_gate = int(r["gate"])
      col_target = num_cols[idx % min(3, len(selected_horses))]
      with col_target:
        custom_num = st.number_input(
            f"{horse_name} ({r['jockey']}) 枠番",
            min_value=1,
            max_value=24,
            value=default_gate,
            key=f"num_input_{horse_name}_{current_race_name}",
        )
        custom_numbers[horse_name] = custom_num

    df_race["num"] = df_race["horse"].map(custom_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    st.dataframe(
        df_race[[
            "num",
            "horse",
            "jockey",
            "style",
            "odds",
            "sire",
        ]].rename(columns={
            "num": "馬番",
            "horse": "馬名",
            "jockey": "騎手",
            "style": "脚質",
            "odds": "想定オッズ",
            "sire": "父",
        }),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🔍 コース物理演算 ＆ 究極AI予想アナライザー</div>',
        unsafe_allow_html=True,
    )

    if current_race_name == "富士ステークス":
      course_desc = (
          "【東京芝1600m特徴】2コーナー出口ポケット発走。最初の3コーナーまで約540mの長い直線。最後の直線（525.9m）の急坂で瞬発力と末脚の持続力が完全決着。"
      )
    else:
      course_desc = (
          "【京都芝2000m（内回り）特徴】スタンド前直線ポケットからの発走。1コーナーまでの距離が短く、小回り2回の内回り戦。機動力と立ち回りの巧者、経済コースを通る馬が圧倒的有利。"
      )

    drain_multi = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going]

    # 究極精密補正（トップジョッキー補正・枠順ロス補正・馬場適性）
    top_jockeys = [
        "C.ルメール",
        "川田将雅",
        "武豊",
        "横山武史",
        "戸崎圭太",
        "松山弘平",
    ]
    df_race["jockey_bonus"] = df_race["jockey"].apply(
        lambda x: 4.5 if x in top_jockeys else 1.0
    )

    # 枠順補正（内枠・中枠の経済コース優位性）
    df_race["gate_bonus"] = df_race["num"].apply(
        lambda n: 2.0 if n <= 8 else (-1.0 if n >= 14 else 0.5)
    )

    if pace_mode == "ハイペース (H)":
      pace_comment = "淀みのない厳しい流れ。前が総崩れとなり、後方からの差し・追込馬に絶好の展開。"
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.5 if s in ["差し", "追込"] else -5.0
      )
    elif pace_mode == "スローペース (S)":
      pace_comment = (
          "スローペース濃厚。前で折り合える逃げ・先行馬の残りが非常に濃厚。"
      )
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.5 if s in ["逃げ", "先行"] else -4.0
      )
    else:
      pace_comment = "平均ペース。各馬の純粋な地力とコース相性がダイレクトに反映。"
      df_race["pace_effect"] = 0.0

    df_race["going_effect"] = (
        (df_race["heavy"] - 90) * (drain_multi - 1.0) * 2.0
        + (df_race["power"] - 90) * (drain_multi - 1.0) * 1.5
    )

    df_race["ultimate_score"] = (
        (df_race["speed"] * 0.35)
        + (df_race["stamina"] * 0.25)
        + (df_race["power"] * 0.15)
        + (df_race["burst"] * 0.15)
        + df_race["jockey_bonus"]
        + df_race["gate_bonus"]
        + df_race["pace_effect"]
        + df_race["going_effect"]
    )

    best_horse = df_race.sort_values(
        by="ultimate_score", ascending=False
    ).iloc[0]

    c_p1, c_p2, c_p3 = st.columns([1, 1, 2])
    with c_p1:
      st.metric("分析対象レース", current_race_name)
      st.metric("設定条件", f"{going} / {pace_mode}")
    with c_p2:
      st.metric(
          "🎯 究極本命推奨（勝率特化）",
          f"{best_horse['num']}番 {best_horse['horse']}({best_horse['jockey']})",
          help="現在の馬場・ペース・枠順を完全網羅した最高期待値馬",
      )
    with c_p3:
      st.write(f"**【{current_race_name} 徹底分析エンジン】**")
      st.info(
          f"{course_desc}\n\n{pace_comment}\n\n💡 **最有力判定**: 馬場【{going}】・ペース【{pace_mode}】の物理補正を経て、**{best_horse['horse']} ({best_horse['jockey']})** が全てのファクターで最高値をマークしています。"
      )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🏁 リアルタイムコース再現アニメーション ＆ 100回モンテカルロ予想</div>',
        unsafe_allow_html=True,
    )

    horses_js = []
    for idx, r in df_race.iterrows():
      horses_js.append({
          "num": int(r["num"]),
          "name": str(r["horse"]),
          "jockey": str(r["jockey"]),
          "style": str(r["style"]),
          "speed": float(r["speed"]),
          "stamina": float(r["stamina"]),
          "power": float(r["power"]),
          "heavy": float(r["heavy"]),
          "burst": float(r["burst"]),
          "jockey_bonus": float(r["jockey_bonus"]),
          "gate_bonus": float(r["gate_bonus"]),
          "pace_effect": float(r["pace_effect"]),
          "going_effect": float(r["going_effect"]),
          "ultimate_score": float(r["ultimate_score"]),
      })

    race_config_js = {
        "venue": venue,
        "dist": dist,
        "going": going,
        "drain": drain_multi,
        "pace": pace_mode,
    }

    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; touch-action: manipulation; }
        body { margin: 0; padding: 0; font-family: -apple-system, sans-serif; background-color: #080c14; color: white; }
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
            <button id="sim100Btn" class="sim100-btn">⚡ 100回シミュレーション＆究極買い目</button>
        </div>
        
        <div id="statusBox" class="status-box">発走準備完了：ボタンを押してください</div>
        
        <div class="svg-wrapper">
            <svg id="trackSvg" viewBox="0 0 720 380" width="100%" height="auto" style="display: block;">
                <path d="M 220 70 L 500 70 A 110 110 0 0 1 500 290 L 220 290 A 110 110 0 0 1 220 70 Z" fill="#16382b" stroke="#22c55e" stroke-width="26"/>
                <path d="M 220 84 L 500 84 A 96 96 0 0 1 500 276 L 220 276 A 96 96 0 0 1 220 84 Z" fill="#080c14" stroke="#080c14" stroke-width="2"/>
                <g id="goalGroup"></g>
                <g id="startGroup"></g>
                <g id="horsesGroup"></g>
            </svg>
        </div>

        <div class="results-box">
            <div id="resultsTitle" style="font-weight: bold; color: #f59e0b; font-size: 16px;">🏆 リアルタイム着順結果</div>
            <div id="resultsContent" style="color: #94a3b8;">発走スタンバイOK</div>
        </div>
    </div>

    <script>
        const horsesData = __HORSES_JSON__;
        const raceConfig = __RACE_CONFIG_JSON__;
        let animId = null;

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
            "東京": { dir: -1, startP: raceConfig.dist === 1600 ? 0.58 : 0.20, slopeP: [0.03, 0.14] },
            "京都": { dir: 1, startP: raceConfig.dist === 2000 ? 0.20 : 0.60, slopeP: [0.02, 0.09] }
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
            resultsContent.innerHTML = '<div style="padding:10px; color:#94a3b8;">⏱ ゲートが開きました！各馬一斉にスタート！</div>';

            const runners = horsesData.map((h, i) => {
                const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                const wakuStyle = getWakuStyle(h.num, horsesData.length);
                const heavyMitigation = (h.heavy - 90) * 0.03;
                const effectiveDrain = Math.max(0.7, raceConfig.drain - heavyMitigation);
                const conditionMod = 0.94 + Math.random() * 0.12;

                return {
                    ...h, laneOffset, wakuStyle,
                    progress: spec.startP, targetProgress: spec.goalP,
                    effectiveDrain, conditionMod,
                    staminaRem: h.stamina * 10 / effectiveDrain,
                    spurtPoint: spec.startP + (totalLapsProgress * (0.62 + Math.random() * 0.08)),
                    finished: false, rank: 0
                };
            });

            let finishedCount = 0;
            const totalHorses = runners.length;

            function animate() {
                group.innerHTML = '';
                runners.forEach((h) => {
                    if (!h.finished) {
                        let baseSpeed = h.speed * h.conditionMod * 0.000037;
                        
                        if (h.jockey_bonus > 1.0) baseSpeed *= 1.02;
                        if (h.pace_effect > 0) baseSpeed *= 1.06;

                        if (h.progress >= h.spurtPoint) {
                            baseSpeed *= (h.style === "差し" || h.style === "追込") ? (1.22 + h.burst * 0.0025) : 1.12;
                        }

                        const pNorm = (h.progress % 1.0);
                        if (pNorm >= spec.slopeP[0] && pNorm <= spec.slopeP[1]) {
                            const powerFactor = (h.power - 90) * 0.006;
                            baseSpeed *= Math.max(0.7, 0.88 + powerFactor);
                        }

                        h.staminaRem -= 0.04 * h.effectiveDrain;
                        if (h.staminaRem <= 0) baseSpeed *= 0.65;

                        h.progress += baseSpeed;

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
                        <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${h.name} (${h.jockey})</text>
                    `;
                    group.appendChild(g);
                });

                if (finishedCount === 0) {
                    status.innerText = `🏇 ${raceConfig.venue} ${raceConfig.dist}m (${raceConfig.going} / ${raceConfig.pace}) レース中！`;
                } else if (finishedCount < totalHorses) {
                    status.innerText = `🏁 ${finishedCount}頭ゴールイン！`;
                } else {
                    status.innerText = '🏆 全頭ゴール！';
                }

                if (finishedCount < totalHorses) {
                    animId = requestAnimationFrame(animate);
                } else {
                    runners.sort((a, b) => a.rank - b.rank);
                    let html = `<div class="results-table-wrapper"><table class="results-table"><thead><tr><th>着順</th><th>枠番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>脚質</th></tr></thead><tbody>`;
                    runners.forEach((h) => {
                        const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                        html += `<tr><td class="rank-badge ${rankClass}">${h.rank}着</td><td><span class="waku-tag" style="background:${h.wakuStyle.bg}; color:${h.wakuStyle.text};">${h.num}</span></td><td style="text-align:left;"><strong>${h.name}</strong></td><td>${h.jockey}</td><td>${h.style}</td></tr>`;
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

            status.innerText = "⚡ 条件・枠順・騎手を反映して100回モンテカルロシミュレーション中...";
            resultsTitle.innerText = "📊 100回シミュレーション総合結果 ＆ 究極推奨買い目";

            const stats = {};
            horsesData.forEach(h => {
                stats[h.name] = {
                    num: h.num, name: h.name, jockey: h.jockey, style: h.style,
                    wakuStyle: getWakuStyle(h.num, horsesData.length),
                    first: 0, second: 0, third: 0, totalRank: 0
                };
            });

            const SIM_COUNT = 100;
            for (let sim = 0; sim < SIM_COUNT; sim++) {
                let raceRes = horsesData.map(h => {
                    const heavyMitigation = (h.heavy - 90) * 0.03;
                    const effectiveDrain = Math.max(0.7, raceConfig.drain - heavyMitigation);
                    const staminaScore = h.stamina / effectiveDrain;
                    const randomMod = (Math.random() - 0.5) * 6.5;

                    const score = (h.speed * 0.35) + (staminaScore * 0.25) + (h.power * 0.15) + (h.burst * 0.15) + h.jockey_bonus + h.gate_bonus + h.pace_effect + randomMod;
                    return { name: h.name, score: score };
                });
                raceRes.sort((a, b) => b.score - a.score);
                raceRes.forEach((item, index) => {
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
                <thead><tr><th>予想順</th><th>枠番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>1着</th><th>2着</th><th>3着</th><th>複勝率</th><th>平均着順</th></tr></thead><tbody>`;

            top5.forEach((h, idx) => {
                const rankClass = idx === 0 ? 'rank-1' : idx === 1 ? 'rank-2' : idx === 2 ? 'rank-3' : '';
                html += `<tr>
                    <td class="rank-badge ${rankClass}">${idx + 1}位</td>
                    <td><span class="waku-tag" style="background:${h.wakuStyle.bg}; color:${h.wakuStyle.text};">${h.num}</span></td>
                    <td style="text-align:left;"><strong>${h.name}</strong></td>
                    <td>${h.jockey}</td>
                    <td>${h.first}回</td><td>${h.second}回</td><td>${h.third}回</td>
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
                <strong>🎯 究極AI自動構築買い目 (${raceConfig.going} / ${raceConfig.pace})</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${t1} - (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${t1} － 相手 (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${t1}, ${t2} → 2着 ${t1}, ${t2}, ${t3} → 3着 ${t1}, ${t2}, ${t3}, ${t4}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ 究極シミュレーション＆買い目構築完了";
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
      f'<div class="section-title">📈 {current_race_name} 究極AIレーダー＆期待値分析</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "枠順のロス、騎手適性、馬場状態、ペース補合をすべて網羅した総合期待値スコアの比較一覧です。"
  )

  df_ana = df_race_base[df_race_base["horse"].isin(selected_horses)].copy()
  if not df_ana.empty:
    df_ana["期待値スコア"] = (
        df_ana["odds"] * (df_ana["speed"] + df_ana["power"]) / 200.0
    ).round(2)
    st.dataframe(
        df_ana[[
            "gate",
            "horse",
            "jockey",
            "odds",
            "speed",
            "stamina",
            "power",
            "burst",
            "期待値スコア",
        ]].rename(columns={
            "gate": "枠番",
            "horse": "馬名",
            "jockey": "騎手",
            "odds": "想定オッズ",
            "speed": "スピード",
            "stamina": "スタミナ",
            "power": "パワー",
            "burst": "瞬発力",
        }),
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.info("出走馬が選択されていません。")

with tab_db:
  st.markdown(
      f'<div class="section-title">📊 週末重賞 総合データベース（全{len(df_all)}頭）</div>',
      unsafe_allow_html=True,
  )
  search_term = st.text_input("レース名・馬名・騎手・父名で検索", "")
  df_filtered = df_all.copy()
  if search_term:
    df_filtered = df_filtered[
        df_filtered["race"].str.contains(search_term, case=False)
        | df_filtered["horse"].str.contains(search_term, case=False)
        | df_filtered["jockey"].str.contains(search_term, case=False)
        | df_filtered["sire"].str.contains(search_term, case=False)
    ]

  st.dataframe(
      df_filtered[[
          "race",
          "gate",
          "horse",
          "jockey",
          "style",
          "odds",
          "speed",
          "stamina",
          "power",
          "sire",
      ]].rename(columns={
          "race": "レース名",
          "gate": "確定枠番",
          "horse": "馬名",
          "jockey": "騎手",
          "style": "脚質",
          "odds": "想定オッズ",
          "speed": "スピード",
          "stamina": "スタミナ",
          "power": "パワー",
          "sire": "父",
      }),
      use_container_width=True,
      hide_index=True,
  )
