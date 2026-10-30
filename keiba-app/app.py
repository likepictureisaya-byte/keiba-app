import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="JRA 週末重賞 究極精密シミュレーター Pro 2026",
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
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">🏇 JRA週末重賞 究極精密シミュレーター <span style="color: #38bdf8; font-size: 18px;">PRO 2026</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">土曜：ファンタジーS ＆ 日曜：天皇賞（秋） 確定枠順・全出走馬完全対応版</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース：ファンタジーS（土曜・京都芝1400m外・全11頭）
@st.cache_data
def get_fantasy_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "レニュアージュ",
          "jockey": "西村淳也",
          "style": "逃げ",
          "speed": 93,
          "stamina": 90,
          "power": 91,
          "heavy": 91,
          "burst": 92,
          "odds": 12.0,
          "sire": "コントレイル",
      },
      {
          "num": 2,
          "horse": "セイウンマイラヴ",
          "jockey": "田山旺佑",
          "style": "逃げ",
          "speed": 92,
          "stamina": 89,
          "power": 90,
          "heavy": 90,
          "burst": 91,
          "odds": 25.0,
          "sire": "カラヴァッジオ",
      },
      {
          "num": 3,
          "horse": "ビスケットサンド",
          "jockey": "北村友一",
          "style": "差し",
          "speed": 94,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 94,
          "odds": 6.5,
          "sire": "モーリス",
      },
      {
          "num": 4,
          "horse": "ニクスルーナ",
          "jockey": "岩田望来",
          "style": "差し",
          "speed": 91,
          "stamina": 91,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 35.0,
          "sire": "キズナ",
      },
      {
          "num": 5,
          "horse": "バタフライ",
          "jockey": "原田和真",
          "style": "差し",
          "speed": 90,
          "stamina": 92,
          "power": 93,
          "heavy": 94,
          "burst": 90,
          "odds": 45.0,
          "sire": "ロードカナロア",
      },
      {
          "num": 6,
          "horse": "イモージェン",
          "jockey": "C.デムーロ",
          "style": "差し",
          "speed": 95,
          "stamina": 93,
          "power": 93,
          "heavy": 93,
          "burst": 96,
          "odds": 4.0,
          "sire": "サリオス",
      },
      {
          "num": 7,
          "horse": "シャンデヴァーグ",
          "jockey": "鮫島克駿",
          "style": "差し",
          "speed": 92,
          "stamina": 92,
          "power": 91,
          "heavy": 91,
          "burst": 93,
          "odds": 18.0,
          "sire": "ロードカナロア",
      },
      {
          "num": 8,
          "horse": "ブライトスクリプト",
          "jockey": "池添謙一",
          "style": "差し",
          "speed": 96,
          "stamina": 94,
          "power": 93,
          "heavy": 92,
          "burst": 97,
          "odds": 3.0,
          "sire": "サートゥルナーリア",
      },
      {
          "num": 9,
          "horse": "ベニバナ",
          "jockey": "幸英明",
          "style": "差し",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 80.0,
          "sire": "キタサンブラック",
      },
      {
          "num": 10,
          "horse": "フェリチタ",
          "jockey": "松山弘平",
          "style": "先行",
          "speed": 95,
          "stamina": 93,
          "power": 94,
          "heavy": 95,
          "burst": 95,
          "odds": 5.5,
          "sire": "タワーオブロンドン",
      },
      {
          "num": 11,
          "horse": "ツキミ",
          "jockey": "川田将雅",
          "style": "先行",
          "speed": 93,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 94,
          "odds": 8.0,
          "sire": "ビッグアーサー",
      },
  ])


# 3. データベース：天皇賞（秋）（日曜・東京芝2000m・全17頭）
@st.cache_data
def get_tennosho_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "クロワデュノール",
          "jockey": "C.デムーロ",
          "style": "先行",
          "speed": 98,
          "stamina": 97,
          "power": 96,
          "heavy": 95,
          "burst": 98,
          "odds": 2.5,
          "sire": "キタサンブラック",
      },
      {
          "num": 2,
          "horse": "エルトンバローズ",
          "jockey": "松若風馬",
          "style": "先行",
          "speed": 92,
          "stamina": 92,
          "power": 91,
          "heavy": 90,
          "burst": 91,
          "odds": 65.0,
          "sire": "ディープブリランテ",
      },
      {
          "num": 3,
          "horse": "レガレイラ",
          "jockey": "戸崎圭太",
          "style": "差し",
          "speed": 97,
          "stamina": 98,
          "power": 95,
          "heavy": 96,
          "burst": 99,
          "odds": 4.2,
          "sire": "スワーヴリチャード",
      },
      {
          "num": 4,
          "horse": "レディネス",
          "jockey": "横山典弘",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 92,
          "heavy": 91,
          "burst": 92,
          "odds": 80.0,
          "sire": "ドゥラメンテ",
      },
      {
          "num": 5,
          "horse": "シャンパンカラー",
          "jockey": "内田博幸",
          "style": "差し",
          "speed": 93,
          "stamina": 92,
          "power": 93,
          "heavy": 94,
          "burst": 92,
          "odds": 90.0,
          "sire": "Reckless",
      },
      {
          "num": 6,
          "horse": "セイウンハーデス",
          "jockey": "幸英明",
          "style": "逃げ",
          "speed": 93,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 91,
          "odds": 50.0,
          "sire": "マンハッタンカフェ",
      },
      {
          "num": 7,
          "horse": "マスカレードボール",
          "jockey": "C.ルメール",
          "style": "差し",
          "speed": 97,
          "stamina": 96,
          "power": 95,
          "heavy": 94,
          "burst": 97,
          "odds": 5.0,
          "sire": "ドゥラメンテ",
      },
      {
          "num": 8,
          "horse": "ジュブロッサム",
          "jockey": "杉原誠人",
          "style": "先行",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 120.0,
          "sire": "クロフネ",
      },
      {
          "num": 9,
          "horse": "ホウオウビスケッツ",
          "jockey": "岩田康誠",
          "style": "逃げ",
          "speed": 94,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 91,
          "odds": 28.0,
          "sire": "マインドユアビスケッツ",
      },
      {
          "num": 10,
          "horse": "ネブラディスク",
          "jockey": "川田将雅",
          "style": "差し",
          "speed": 95,
          "stamina": 95,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 16.0,
          "sire": "American Post",
      },
      {
          "num": 11,
          "horse": "シェイクユアハート",
          "jockey": "吉村智洋",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 85.0,
          "sire": "Sri Pekan",
      },
      {
          "num": 12,
          "horse": "コスモキュランダ",
          "jockey": "M.デムーロ",
          "style": "差し",
          "speed": 94,
          "stamina": 95,
          "power": 95,
          "heavy": 96,
          "burst": 94,
          "odds": 22.0,
          "sire": "アルアイン",
      },
      {
          "num": 13,
          "horse": "リアライズシリウス",
          "jockey": "丹内祐次",
          "style": "先行",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 70.0,
          "sire": "Southern Image",
      },
      {
          "num": 14,
          "horse": "タガノデュード",
          "jockey": "津村明秀",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 95.0,
          "sire": "ステイゴールド",
      },
      {
          "num": 15,
          "horse": "サクラファレル",
          "jockey": "佐々木大輔",
          "style": "差し",
          "speed": 92,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 60.0,
          "sire": "ハーツクライ",
      },
      {
          "num": 16,
          "horse": "ジョバンニ",
          "jockey": "松山弘平",
          "style": "先行",
          "speed": 95,
          "stamina": 95,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 18.0,
          "sire": "エピファネイア",
      },
      {
          "num": 17,
          "horse": "ダノンデサイル",
          "jockey": "戸崎圭太",
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 96,
          "heavy": 95,
          "burst": 96,
          "odds": 8.0,
          "sire": "エピファネイア",
      },
  ])


# メインのレース選択タブ
main_tab1, main_tab2 = st.tabs(
    ["🌸 土曜：ファンタジーS (GIII)", "🍁 日曜：天皇賞（秋） (GI)"]
  )

# ==========================================
# 🌸 ファンタジーS タブ処理
# ==========================================
with main_tab1:
  df_all = get_fantasy_db()
  if "sel_fan" not in st.session_state:
    st.session_state.sel_fan = df_all["horse"].tolist()

  st.markdown(
      '<div class="section-title">⚡ ファンタジーS 最新全11頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  if st.button(
      "🌸 ファンタジーS (京都・芝1400m外) 全11頭一括セット",
      key="btn_fan",
      use_container_width=True,
  ):
    st.session_state.sel_fan = df_all["horse"].tolist()

  c1, c2 = st.columns(2)
  with c1:
    going_f = st.selectbox(
        "馬場状態 (ファンタジーS)", ["良", "稍重", "重", "不良"], key="g_fan"
    )
  with c2:
    pace_f = st.selectbox(
        "展開ペース (荒れ想定対応)",
        [
            "ハイペース (H - 荒れ想定)",
            "ミドルペース (M)",
            "スローペース (S)",
        ],
        key="p_fan",
    )

  selected_horses = st.multiselect(
      "出走馬選択 (ファンタジーS)",
      options=df_all["horse"].tolist(),
      default=st.session_state.sel_fan,
      key="ms_fan",
  )

  if len(selected_horses) >= 2:
    df_race = (
        df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
    )
    num_cols = st.columns(min(3, len(selected_horses)))
    custom_numbers = {}
    for idx, r in df_race.iterrows():
      with num_cols[idx % min(3, len(selected_horses))]:
        custom_numbers[r["horse"]] = st.number_input(
            f"{r['horse']} ({r['jockey']}) 馬番",
            1,
            24,
            int(r["num"]),
            key=f"num_f_{r['horse']}",
        )
    df_race["num"] = df_race["horse"].map(custom_numbers)
    df_race = df_race.sort_values(by="num").reset_index(drop=True)

    drain_f = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going_f]
    top_j = ["川田将雅", "C.デムーロ", "池添謙一", "松山弘平", "北村友一"]
    df_race["j_bonus"] = df_race["jockey"].apply(
        lambda x: 4.5 if x in top_j else 1.5
    )
    df_race["g_bonus"] = df_race["num"].apply(
        lambda n: 2.5 if n >= 8 else (2.0 if n <= 3 else 1.0)
    )
    df_race["p_effect"] = (
        df_race["style"].apply(lambda s: 6.0 if s in ["差し", "追込"] else -6.0)
        if "ハイペース" in pace_f
        else (
            df_race["style"].apply(
                lambda s: 5.0 if s in ["先行", "自在"] else -3.0
            )
            if "スローペース" in pace_f
            else 0.0
        )
    )
    df_race["score"] = (
        df_race["speed"] * 0.30
        + df_race["burst"] * 0.30
        + df_race["stamina"] * 0.20
        + df_race["power"] * 0.10
        + df_race["j_bonus"]
        + df_race["g_bonus"]
        + df_race["p_effect"]
    )
    best_f = df_race.sort_values(by="score", ascending=False).iloc[0]

    st.success(
        f"🌸 **ファンタジーS 荒れ想定本命**: {best_f['num']}番"
        f" {best_f['horse']} ({best_f['jockey']})"
    )

    # 簡易HTMLシミュレーター表示（ファンタジーS用）
    horses_js = df_race.to_dict(orient="records")
    race_cfg = {"drain": drain_f, "going": going_f, "pace": pace_f}

    # 共通HTMLビルダー
    html_sim = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ margin:0; background:#080c14; color:white; font-family:sans-serif; text-align:center; }}
        .btn {{ height:45px; background:linear-gradient(135deg,#059669,#047857); color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer; width:100%; margin-top:5px; }}
        .box {{ background:#111827; padding:12px; border-radius:10px; margin-top:10px; text-align:left; }}
        table {{ width:100%; border-collapse:collapse; margin-top:5px; }}
        th, td {{ padding:8px; font-size:13px; text-align:center; border-bottom:1px solid #1f2937; }}
        th {{ background:#1f2937; color:#9ca3af; }}
    </style>
</head>
<body>
    <button class="btn" onclick="runSim()">▶ リアルタイムレース発走</button>
    <div id="st" style="font-weight:bold; color:#34d399; margin:8px;">スタンバイOK</div>
    <div class="box" id="res">ボタンを押してレーススタート</div>
    <script>
        const hData = {json.dumps(horses_js)};
        function runSim() {{
            document.getElementById('st.id' || 'st').innerText = "🏁 レース熱戦中！";
            let resHtml = "<table><tr><th>着順</th><th>馬番</th><th>馬名</th><th>騎手</th></tr>";
            let sorted = [...hData].sort(() => Math.random() - 0.5);
            sorted.forEach((h, idx) => {{
                resHtml += `<tr><td><b>${{idx+1}}着</b></td><td>${{h.num}}</td><td><b>${{h.name}}</b></td><td>${{h.jockey}}</td></tr>`;
            }});
            resHtml += "</table>";
            document.getElementById('res').innerHTML = resHtml;
            document.getElementById('st').innerText = "🏆 ゴールイン！";
        }}
    </script>
</body>
</html>"""
    st.components.v1.html(html_sim, height=350)

# ==========================================
# 🍁 天皇賞（秋） タブ処理
# ==========================================
with main_tab2:
  df_all_t = get_tennosho_db()
  if "sel_ten" not in st.session_state:
    st.session_state.sel_ten = df_all_t["horse"].tolist()

  st.markdown(
      '<div class="section-title">⚡ 天皇賞（秋） 最新全17頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  if st.button(
      "🍁 天皇賞（秋） (東京・芝2000m) 全17頭一括セット",
      key="btn_ten",
      use_container_width=True,
  ):
    st.session_state.sel_ten = df_all_t["horse"].tolist()

  tc1, tc2 = st.columns(2)
  with tc1:
    going_t = st.selectbox(
        "馬場状態 (天皇賞秋)", ["良", "稍重", "重", "不良"], key="g_ten"
    )
  with tc2:
    pace_t = st.selectbox(
        "展開ペース指定 (天皇賞秋)",
        ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"],
        key="p_ten",
    )

  selected_horses_t = st.multiselect(
      "出走馬選択 (天皇賞秋)",
      options=df_all_t["horse"].tolist(),
      default=st.session_state.sel_ten,
      key="ms_ten",
  )

  if len(selected_horses_t) >= 2:
    df_race_t = (
        df_all_t[df_all_t["horse"].isin(selected_horses_t)]
        .copy()
        .reset_index(drop=True)
    )
    num_cols_t = st.columns(min(3, len(selected_horses_t)))
    custom_numbers_t = {}
    for idx, r in df_race_t.iterrows():
      with num_cols_t[idx % min(3, len(selected_horses_t))]:
        custom_numbers_t[r["horse"]] = st.number_input(
            f"{r['horse']} ({r['jockey']}) 馬番",
            1,
            24,
            int(r["num"]),
            key=f"num_t_{r['horse']}",
        )
    df_race_t["num"] = df_race_t["horse"].map(custom_numbers_t)
    df_race_t = df_race_t.sort_values(by="num").reset_index(drop=True)

    drain_t = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going_t]
    top_jt = ["C.ルメール", "C.デムーロ", "川田将雅", "戸崎圭太", "横山典弘"]
    df_race_t["j_bonus"] = df_race_t["jockey"].apply(
        lambda x: 5.0 if x in top_jt else 1.2
    )
    df_race_t["g_bonus"] = df_race_t["num"].apply(
        lambda n: 3.0 if n <= 6 else (-3.0 if n >= 14 else 1.0)
    )
    df_race_t["p_effect"] = (
        df_race_t["style"].apply(lambda s: 5.0 if s in ["差し", "追込"] else -5.0)
        if pace_t == "ハイペース (H)"
        else (
            df_race_t["style"].apply(
                lambda s: 5.0 if s in ["先行", "自在"] else -4.0
            )
            if pace_t == "スローペース (S)"
            else 0.0
        )
    )
    df_race_t["score"] = (
        df_race_t["speed"] * 0.35
        + df_race_t["burst"] * 0.25
        + df_race_t["stamina"] * 0.20
        + df_race_t["power"] * 0.10
        + df_race_t["j_bonus"]
        + df_race_t["g_bonus"]
        + df_race_t["p_effect"]
    )
    best_t = df_race_t.sort_values(by="score", ascending=False).iloc[0]

    st.warning(
        f"🍁 **天皇賞（秋） 本命推奨**: {best_t['num']}番"
        f" {best_t['horse']} ({best_t['jockey']})"
    )

    horses_js_t = df_race_t.to_dict(orient="records")
    st.components.v1.html(html_sim.replace("hData = ", f"hData = {json.dumps(horses_js_t)}; //"), height=350)

