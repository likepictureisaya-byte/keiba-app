import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="第87回 菊花賞 究極精密シミュレーター Pro 2026",
    page_icon="⚜️",
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
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">⚜️ 第87回 菊花賞（GI） <span style="color: #38bdf8; font-size: 18px;">PRO SIMULATOR 2026</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">京都芝3000m（外回り） 確定枠順・全18頭完全対応 | 長距離物理演算＆過去傾向ロジック</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース：菊花賞 確定出走馬（全18頭・枠順・騎手・詳細パラメータ）
@st.cache_data
def get_kikuka_horse_db_2026():
  kikuka_horses = [
      {
          "race": "菊花賞",
          "horse": "エムズビギン",
          "jockey": "岩田望来",
          "gate": 1,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 92,
          "stamina": 94,
          "power": 92,
          "heavy": 91,
          "burst": 92,
          "odds": 27.9,
          "opt_dist": 3000,
          "sire": "コントレイル",
      },
      {
          "race": "菊花賞",
          "horse": "コンジェスタス",
          "jockey": "西村淳也",
          "gate": 2,
          "venue": "京都",
          "dist": 3000,
          "style": "先行",
          "speed": 91,
          "stamina": 93,
          "power": 91,
          "heavy": 90,
          "burst": 90,
          "odds": 16.3,
          "opt_dist": 3000,
          "sire": "キタサンブラック",
      },
      {
          "race": "菊花賞",
          "horse": "アウダーシア",
          "jockey": "津村明秀",
          "gate": 3,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 92,
          "stamina": 94,
          "power": 92,
          "heavy": 92,
          "burst": 91,
          "odds": 20.2,
          "opt_dist": 3000,
          "sire": "キズナ",
      },
      {
          "race": "菊花賞",
          "horse": "ショウナンガルフ",
          "jockey": "田山旺佑",
          "gate": 4,
          "venue": "京都",
          "dist": 3000,
          "style": "追込",
          "speed": 85,
          "stamina": 87,
          "power": 86,
          "heavy": 86,
          "burst": 85,
          "odds": 160.0,
          "opt_dist": 3000,
          "sire": "ドゥラメンテ",
      },
      {
          "race": "菊花賞",
          "horse": "ジャスティンシカゴ",
          "jockey": "原優介",
          "gate": 5,
          "venue": "京都",
          "dist": 3000,
          "style": "先行",
          "speed": 94,
          "stamina": 95,
          "power": 93,
          "heavy": 92,
          "burst": 93,
          "odds": 38.6,
          "opt_dist": 3000,
          "sire": "スワーヴリチャード",
      },
      {
          "race": "菊花賞",
          "horse": "バステール",
          "jockey": "川田将雅",
          "gate": 6,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 95,
          "stamina": 96,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 32.4,
          "opt_dist": 3000,
          "sire": "キタサンブラック",
      },
      {
          "race": "菊花賞",
          "horse": "ラージアンサンブル",
          "jockey": "坂井瑠星",
          "gate": 7,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 89,
          "stamina": 90,
          "power": 89,
          "heavy": 89,
          "burst": 89,
          "odds": 85.2,
          "opt_dist": 3000,
          "sire": "モーリス",
      },
      {
          "race": "菊花賞",
          "horse": "ロブチェン",
          "jockey": "松山弘平",
          "gate": 8,
          "venue": "京都",
          "dist": 3000,
          "style": "自在",
          "speed": 98,
          "stamina": 99,
          "power": 97,
          "heavy": 96,
          "burst": 98,
          "odds": 1.7,
          "opt_dist": 3000,
          "sire": "ワールドプレミア",
      },
      {
          "race": "菊花賞",
          "horse": "ゴーイントゥスカイ",
          "jockey": "武豊",
          "gate": 9,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 93,
          "stamina": 95,
          "power": 93,
          "heavy": 92,
          "burst": 94,
          "odds": 11.8,
          "opt_dist": 3000,
          "sire": "コントレイル",
      },
      {
          "race": "菊花賞",
          "horse": "ダノンヒストリー",
          "jockey": "C.ルメール",
          "gate": 10,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 97,
          "stamina": 98,
          "power": 95,
          "heavy": 94,
          "burst": 97,
          "odds": 3.1,
          "opt_dist": 3000,
          "sire": "エピファネイア",
      },
      {
          "race": "菊花賞",
          "horse": "アスクエジンバラ",
          "jockey": "岩田康誠",
          "gate": 11,
          "venue": "京都",
          "dist": 3000,
          "style": "自在",
          "speed": 93,
          "stamina": 94,
          "power": 93,
          "heavy": 92,
          "burst": 92,
          "odds": 48.7,
          "opt_dist": 3000,
          "sire": "リオンディーズ",
      },
      {
          "race": "菊花賞",
          "horse": "サノノグレーター",
          "jockey": "田辺裕信",
          "gate": 12,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 89,
          "stamina": 90,
          "power": 89,
          "heavy": 89,
          "burst": 88,
          "odds": 91.3,
          "opt_dist": 3000,
          "sire": "グレーターロンドン",
      },
      {
          "race": "菊花賞",
          "horse": "キンググローリー",
          "jockey": "丹内祐次",
          "gate": 13,
          "venue": "京都",
          "dist": 3000,
          "style": "逃げ",
          "speed": 88,
          "stamina": 89,
          "power": 88,
          "heavy": 88,
          "burst": 86,
          "odds": 120.0,
          "opt_dist": 3000,
          "sire": "モーリス",
      },
      {
          "race": "菊花賞",
          "horse": "マジョレルブルー",
          "jockey": "戸崎圭太",
          "gate": 14,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 64.8,
          "opt_dist": 3000,
          "sire": "ロードカナロア",
      },
      {
          "race": "菊花賞",
          "horse": "シートゥサミット",
          "jockey": "酒井学",
          "gate": 15,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 76.2,
          "opt_dist": 3000,
          "sire": "モーリス",
      },
      {
          "race": "菊花賞",
          "horse": "ショウナンハヤナミ",
          "jockey": "池添謙一",
          "gate": 16,
          "venue": "京都",
          "dist": 3000,
          "style": "追込",
          "speed": 87,
          "stamina": 89,
          "power": 87,
          "heavy": 87,
          "burst": 87,
          "odds": 180.0,
          "opt_dist": 3000,
          "sire": "ドレフォン",
      },
      {
          "race": "菊花賞",
          "horse": "チャリングクロス",
          "jockey": "石川裕紀人",
          "gate": 17,
          "venue": "京都",
          "dist": 3000,
          "style": "差し",
          "speed": 89,
          "stamina": 90,
          "power": 89,
          "heavy": 89,
          "burst": 89,
          "odds": 102.0,
          "opt_dist": 3000,
          "sire": "ロードカナロア",
      },
      {
          "race": "菊花賞",
          "horse": "ナリタエスペランサ",
          "jockey": "北村友一",
          "gate": 18,
          "venue": "京都",
          "dist": 3000,
          "style": "逃げ",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 88,
          "odds": 200.0,
          "opt_dist": 2600,
          "sire": "エピファネイア",
      },
  ]
  return pd.DataFrame(kikuka_horses)


df_all = get_kikuka_horse_db_2026()

if "selected_horses" not in st.session_state:
  st.session_state.selected_horses = df_all["horse"].tolist()
if "going" not in st.session_state:
  st.session_state.going = "良"
if "pace_mode" not in st.session_state:
  st.session_state.pace_mode = "ミドルペース (M)"


def set_preset_kikuka():
  st.session_state.selected_horses = df_all["horse"].tolist()


tab_sim, tab_analysis, tab_db = st.tabs([
    "⚜️ 菊花賞 レースシミュレーション＆予想",
    "📈 長距離適性・AI能力レーダー",
    f"📊 菊花賞出走馬データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.markdown(
      '<div class="section-title">⚡ 第87回 菊花賞 確定枠順・全頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  st.button(
      "⚜️ 10/25(日) 菊花賞 (京都・芝3000m) 全18頭一括セット",
      on_click=set_preset_kikuka,
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

  st.markdown("---")
  st.markdown(
      '<div class="section-title">🐎 出走馬・確定枠順（馬番） ＆ 騎手一覧</div>',
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
            f"{horse_name} ({r['jockey']}) 馬番",
            min_value=1,
            max_value=24,
            value=default_gate,
            key=f"num_input_{horse_name}",
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
        '<div class="section-title">🔍 京都芝3000m コース物理演算 ＆ 長距離適性アナライザー</div>',
        unsafe_allow_html=True,
    )

    course_desc = (
        "【京都芝3000m（外回り3周）特徴】スタンド前発走で淀の坂を2回越える日本最長のクラシックディスタンス。"
        "前半の折り合いと、3〜4コーナーの下り坂からのロングスパート能力、そしてタフなスタミナが完全に求められます。"
    )

    drain_multi = {"良": 1.0, "稍重": 1.18, "重": 1.40, "不良": 1.65}[going]

    # 長距離実績・トップジョッキー補正（武豊、C.ルメール、川田将雅、松山弘平など）
    top_long_jockeys = [
        "武豊",
        "C.ルメール",
        "川田将雅",
        "松山弘平",
        "戸崎圭太",
    ]
    df_race["jockey_bonus"] = df_race["jockey"].apply(
        lambda x: 5.0 if x in top_long_jockeys else 1.2
    )

    # 枠順補正（3000mでは極端な外枠はロスが大きいが、中〜内枠はロスが少ない）
    df_race["gate_bonus"] = df_race["num"].apply(
        lambda n: 2.5 if 4 <= n <= 12 else (-2.0 if n >= 16 else 1.0)
    )

    if pace_mode == "ハイペース (H)":
      pace_comment = "淀みのない持久戦。前が潰れ、確実なスタミナと末脚を温存できた馬が浮上。"
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.0 if s in ["差し", "追込"] else -5.0
      )
    elif pace_mode == "スローペース (S)":
      pace_comment = (
          "スローの瞬発力勝負。器用に立ち回れる先行力・自在性が大きな武器に。"
      )
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.0 if s in ["先行", "自在"] else -4.0
      )
    else:
      pace_comment = "平均ペース。スタミナ・折り合い・地力がダイレクトに結果へ直結。"
      df_race["pace_effect"] = 0.0

    df_race["going_effect"] = (
        (df_race["heavy"] - 90) * (drain_multi - 1.0) * 2.5
        + (df_race["stamina"] - 90) * (drain_multi - 1.0) * 2.0
    )

    df_race["kikuka_score"] = (
        (df_race["stamina"] * 0.40)
        + (df_race["speed"] * 0.25)
        + (df_race["power"] * 0.15)
        + (df_race["burst"] * 0.10)
        + df_race["jockey_bonus"]
        + df_race["gate_bonus"]
        + df_race["pace_effect"]
        + df_race["going_effect"]
    )

    best_horse = df_race.sort_values(by="kikuka_score", ascending=False).iloc[0]

    c_p1, c_p2, c_p3 = st.columns([1, 1, 2])
    with c_p1:
      st.metric("レース条件", "京都 芝3000m (GI)")
      st.metric("馬場・ペース", f"{going} / {pace_mode}")
    with c_p2:
      st.metric(
          "👑 菊花賞 本命推奨",
          f"{best_horse['num']}番 {best_horse['horse']}({best_horse['jockey']})",
          help="長距離適性・スタミナ・騎手手腕を網羅した最高期待値馬",
      )
    with c_p3:
      st.write("**【菊花賞 徹底アナライズ】**")
      st.info(
          f"{course_desc}\n\n{pace_comment}\n\n💡 **最有力判定**: 長距離3000mのスタミナ負荷と馬場【{going}】をクリアし、**{best_horse['horse']} ({best_horse['jockey']})** が最も安定した走破確率を示しています。"
      )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🏁 京都芝3000m リアルタイムアニメーション ＆ 100回モンテカルロ予想</div>',
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
          "kikuka_score": float(r["kikuka_score"]),
      })

    race_config_js = {
        "venue": "京都",
        "dist": 3000,
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

        // 3000mは1.5周 (3000 / 2000)
        const totalLapsProgress = 1.5;
        const spec = { dir: 1, startP: 0.60, goalP: 0.60 + 1.5, slopeP: [0.02, 0.09] };

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
            resultsTitle.innerText = "🏆 菊花賞 リアルタイム着順結果";
            resultsContent.innerHTML = '<div style="padding:10px; color:#94a3b8;">⏱ ゲートが開きました！京都3000mの長丁場スタート！</div>';

            const runners = horsesData.map((h, i) => {
                const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                const wakuStyle = getWakuStyle(h.num, horsesData.length);
                const heavyMitigation = (h.heavy - 90) * 0.03;
                const effectiveDrain = Math.max(0.65, raceConfig.drain - heavyMitigation);
                const conditionMod = 0.94 + Math.random() * 0.12;

                return {
                    ...h, laneOffset, wakuStyle,
                    progress: spec.startP, targetProgress: spec.goalP,
                    effectiveDrain, conditionMod,
                    staminaRem: h.stamina * 15 / effectiveDrain,
                    spurtPoint: spec.startP + (totalLapsProgress * (0.75 + Math.random() * 0.05)),
                    finished: false, rank: 0
                };
            });

            let finishedCount = 0;
            const totalHorses = runners.length;

            function animate() {
                group.innerHTML = '';
                runners.forEach((h) => {
                    if (!h.finished) {
                        let baseSpeed = h.speed * h.conditionMod * 0.000032;
                        
                        if (h.jockey_bonus > 1.0) baseSpeed *= 1.018;
                        if (h.pace_effect > 0) baseSpeed *= 1.05;

                        if (h.progress >= h.spurtPoint) {
                            baseSpeed *= (h.style === "差し" || h.style === "追込") ? (1.20 + h.burst * 0.002) : 1.10;
                        }

                        // 長距離3000mはスタミナ切れが勝負を分ける
                        h.staminaRem -= 0.055 * h.effectiveDrain;
                        if (h.staminaRem <= 0) baseSpeed *= 0.5;

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
                    status.innerText = `⚜️ 京都3000m 菊花賞 (${raceConfig.going} / ${raceConfig.pace}) 熱戦中！`;
                } else if (finishedCount < totalHorses) {
                    status.innerText = `🏁 ${finishedCount}頭ゴールイン！`;
                } else {
                    status.innerText = '🏆 全頭ゴール！';
                }

                if (finishedCount < totalHorses) {
                    animId = requestAnimationFrame(animate);
                } else {
                    runners.sort((a, b) => a.rank - b.rank);
                    let html = `<div class="results-table-wrapper"><table class="results-table"><thead><tr><th>着順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>脚質</th></tr></thead><tbody>`;
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

            status.innerText = "⚡ スタミナ・長距離実績・枠順を反映して100回モンテカルロシミュレーション中...";
            resultsTitle.innerText = "📊 100回シミュレーション総合結果 ＆ 菊花賞推奨買い目";

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
                    const effectiveDrain = Math.max(0.65, raceConfig.drain - heavyMitigation);
                    const staminaScore = (h.stamina * 1.4) / effectiveDrain;
                    const randomMod = (Math.random() - 0.5) * 6.0;

                    const score = (staminaScore * 0.40) + (h.speed * 0.25) + (h.power * 0.15) + (h.burst * 0.10) + h.jockey_bonus + h.gate_bonus + h.pace_effect + randomMod;
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
                <thead><tr><th>予想順</th><th>馬番</th><th style="text-align:left;">馬名</th><th>騎手</th><th>1着</th><th>2着</th><th>3着</th><th>複勝率</th><th>平均着順</th></tr></thead><tbody>`;

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
                <strong>🎯 菊花賞 AI自動構築買い目 (${raceConfig.going} / ${raceConfig.pace})</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${t1} - (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${t1} － 相手 (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${t1}, ${t2} → 2着 ${t1}, ${t2}, ${t3} → 3着 ${t1}, ${t2}, ${t3}, ${t4}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ 菊花賞シミュレーション＆買い目構築完了";
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
      '<div class="section-title">📈 菊花賞出走馬 長距離適性AIレーダー</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "京都芝3000mのスタミナ負荷、長距離実績、騎手・枠順補正を網羅した総合期待値の比較一覧です。"
  )

  df_ana = df_all[df_all["horse"].isin(selected_horses)].copy()
  if not df_ana.empty:
    df_ana["期待値スコア"] = (
        df_ana["odds"] * (df_ana["stamina"] + df_ana["power"]) / 200.0
    ).round(2)
    st.dataframe(
        df_ana[[
            "gate",
            "horse",
            "jockey",
            "odds",
            "stamina",
            "speed",
            "power",
            "heavy",
            "burst",
            "期待値スコア",
        ]].rename(columns={
            "gate": "枠番",
            "horse": "馬名",
            "jockey": "騎手",
            "odds": "想定オッズ",
            "stamina": "スタミナ",
            "speed": "スピード",
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
      f'<div class="section-title">📊 菊花賞 総合データベース（全{len(df_all)}頭）</div>',
      unsafe_allow_html=True,
  )
  search_term = st.text_input("馬名・騎手・父名で検索", "")
  df_filtered = df_all.copy()
  if search_term:
    df_filtered = df_filtered[
        df_filtered["horse"].str.contains(search_term, case=False)
        | df_filtered["jockey"].str.contains(search_term, case=False)
        | df_filtered["sire"].str.contains(search_term, case=False)
    ]

  st.dataframe(
      df_filtered[[
          "gate",
          "horse",
          "jockey",
          "style",
          "odds",
          "stamina",
          "speed",
          "power",
          "sire",
      ]].rename(columns={
          "gate": "確定枠番",
          "horse": "馬名",
          "jockey": "騎手",
          "style": "脚質",
          "odds": "想定オッズ",
          "stamina": "スタミナ",
          "speed": "スピード",
          "power": "パワー",
          "sire": "父",
      }),
      use_container_width=True,
      hide_index=True,
  )
