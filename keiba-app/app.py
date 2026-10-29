import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="第174回 天皇賞（秋） 究極精密シミュレーター Pro 2026",
    page_icon="🍁",
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
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">🍁 第174回 天皇賞（秋）（GI） <span style="color: #38bdf8; font-size: 18px;">PRO SIMULATOR 2026</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">東京芝2000m（左回り） 確定枠順・出走馬完全対応 | 東京実績＆瞬発力物理演算ロジック</p>
</div>
""",
    unsafe_allow_html=True,
)


# 2. データベース：天皇賞（秋） 確定出走馬（枠順・騎手・詳細パラメータ）
@st.cache_data
def get_tennosho_horse_db_2026():
  tennosho_horses = [
      {
          "race": "天皇賞（秋）",
          "horse": "タスティエーラ",
          "jockey": "松山弘平",
          "gate": 1,
          "venue": "東京",
          "dist": 2000,
          "style": "先行",
          "speed": 95,
          "stamina": 96,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 8.5,
          "opt_dist": 2000,
          "sire": "サトノクラウン",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "リバティアイランド",
          "jockey": "川田将雅",
          "gate": 2,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 98,
          "stamina": 97,
          "power": 96,
          "heavy": 95,
          "burst": 99,
          "odds": 2.2,
          "opt_dist": 2000,
          "sire": "ドゥラメンテ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ドウデュース",
          "jockey": "武豊",
          "gate": 3,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 99,
          "stamina": 97,
          "power": 97,
          "heavy": 96,
          "burst": 98,
          "odds": 3.0,
          "opt_dist": 2000,
          "sire": "ハーツクライ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ソールオリエンス",
          "jockey": "横山武史",
          "gate": 4,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 94,
          "stamina": 95,
          "power": 96,
          "heavy": 97,
          "burst": 95,
          "odds": 12.0,
          "opt_dist": 2000,
          "sire": "キタサンブラック",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ジャスティンパレス",
          "jockey": "C.ルメール",
          "gate": 5,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 95,
          "heavy": 94,
          "burst": 96,
          "odds": 6.8,
          "opt_dist": 2000,
          "sire": "ディープインパクト",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ベラジオオペラ",
          "jockey": "横山和生",
          "gate": 6,
          "venue": "東京",
          "dist": 2000,
          "style": "先行",
          "speed": 95,
          "stamina": 94,
          "power": 94,
          "heavy": 93,
          "burst": 94,
          "odds": 14.5,
          "opt_dist": 2000,
          "sire": "ロードカナロア",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ホウオウビスケッツ",
          "jockey": "岩田康誠",
          "gate": 7,
          "venue": "東京",
          "dist": 2000,
          "style": "逃げ",
          "speed": 93,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 91,
          "odds": 28.0,
          "opt_dist": 2000,
          "sire": "マインドユアビスケッツ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ノースブリッジ",
          "jockey": "岩田望来",
          "gate": 8,
          "venue": "東京",
          "dist": 2000,
          "style": "先行",
          "speed": 94,
          "stamina": 94,
          "power": 95,
          "heavy": 95,
          "burst": 93,
          "odds": 35.0,
          "opt_dist": 2000,
          "sire": "モーリス",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "キングズパレス",
          "jockey": "松岡正海",
          "gate": 9,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 93,
          "odds": 42.0,
          "opt_dist": 2000,
          "sire": "キングカメハメハ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "シックスペンス",
          "jockey": "戸崎圭太",
          "gate": 10,
          "venue": "東京",
          "dist": 2000,
          "style": "先行",
          "speed": 95,
          "stamina": 94,
          "power": 94,
          "heavy": 93,
          "burst": 96,
          "odds": 15.0,
          "opt_dist": 1800,
          "sire": "キズナ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ステラヴェローチェ",
          "jockey": "酒井学",
          "gate": 11,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 93,
          "heavy": 94,
          "burst": 91,
          "odds": 65.0,
          "opt_dist": 2000,
          "sire": "バゴ",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "ニシノスーベニア",
          "jockey": "大野拓弥",
          "gate": 12,
          "venue": "東京",
          "dist": 2000,
          "style": "差し",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 90,
          "odds": 95.0,
          "opt_dist": 1800,
          "sire": "ハービンジャー",
      },
      {
          "race": "天皇賞（秋）",
          "horse": "マテンロウスカイ",
          "jockey": "横山典弘",
          "gate": 13,
          "venue": "東京",
          "dist": 2000,
          "style": "先行",
          "speed": 92,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 55.0,
          "opt_dist": 2000,
          "sire": "モーリス",
      },
  ]
  return pd.DataFrame(tennosho_horses)


df_all = get_tennosho_horse_db_2026()

if "selected_horses" not in st.session_state:
  st.session_state.selected_horses = df_all["horse"].tolist()
if "going" not in st.session_state:
  st.session_state.going = "良"
if "pace_mode" not in st.session_state:
  st.session_state.pace_mode = "ミドルペース (M)"


def set_preset_tennosho():
  st.session_state.selected_horses = df_all["horse"].tolist()


tab_sim, tab_analysis, tab_db = st.tabs([
    "🍁 天皇賞（秋） シミュレーション＆予想",
    "📈 東京2000m適性・AI能力レーダー",
    f"📊 出走馬データベース（全{len(df_all)}頭）",
])

with tab_sim:
  st.markdown(
      '<div class="section-title">⚡ 第174回 天皇賞（秋） 確定枠順・全頭一括ロード</div>',
      unsafe_allow_html=True,
  )
  st.button(
      "🍁 天皇賞（秋） (東京・芝2000m) 全出走馬一括セット",
      on_click=set_preset_tennosho,
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
        '<div class="section-title">🔍 東京芝2000m コース物理演算 ＆ 瞬発力アナライザー</div>',
        unsafe_allow_html=True,
    )

    course_desc = (
        "【東京芝2000m特徴】2コーナー奥のポケット発走。最初の1コーナーまでの距離が約300mと短く、枠順の有利不利や序盤のポジション取りが勝敗に直結します。"
        "最後の直線（525.9m）での強烈な末脚と、東京巧者としての適性が問われる王道GIコースです。"
    )

    drain_multi = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[going]

    # 天皇賞（秋）実績・トップジョッキー補正
    top_tennosho_jockeys = [
        "武豊",
        "C.ルメール",
        "川田将雅",
        "横山武史",
        "戸崎圭太",
    ]
    df_race["jockey_bonus"] = df_race["jockey"].apply(
        lambda x: 5.0 if x in top_tennosho_jockeys else 1.2
    )

    # 東京2000mの枠順補正（極端な外枠はロス大、内〜中枠の経済コースが圧倒的有利）
    df_race["gate_bonus"] = df_race["num"].apply(
        lambda n: 3.0 if n <= 6 else (-2.5 if n >= 11 else 1.0)
    )

    if pace_mode == "ハイペース (H)":
      pace_comment = "前が激しく競り合う消耗戦。直線で強烈な末脚を発揮する差し・追込馬に展開の利が最大化。"
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.0 if s in ["差し", "追込"] else -5.0
      )
    elif pace_mode == "スローペース (S)":
      pace_comment = "スローの上り勝負。好位でスムーズに折り合える先行・自在馬が非常に有利。"
      df_race["pace_effect"] = df_race["style"].apply(
          lambda s: 5.0 if s in ["先行", "自在"] else -4.0
      )
    else:
      pace_comment = "平均ペース。各馬の純粋な地力と東京コース適性がダイレクトに結果へ直結。"
      df_race["pace_effect"] = 0.0

    df_race["going_effect"] = (
        (df_race["heavy"] - 90) * (drain_multi - 1.0) * 2.0
        + (df_race["power"] - 90) * (drain_multi - 1.0) * 1.5
    )

    df_race["tennosho_score"] = (
        (df_race["speed"] * 0.35)
        + (df_race["burst"] * 0.25)
        + (df_race["stamina"] * 0.20)
        + (df_race["power"] * 0.10)
        + df_race["jockey_bonus"]
        + df_race["gate_bonus"]
        + df_race["pace_effect"]
        + df_race["going_effect"]
    )

    best_horse = df_race.sort_values(
        by="tennosho_score", ascending=False
    ).iloc[0]

    c_p1, c_p2, c_p3 = st.columns([1, 1, 2])
    with c_p1:
      st.metric("レース条件", "東京 芝2000m (GI)")
      st.metric("馬場・ペース", f"{going} / {pace_mode}")
    with c_p2:
      st.metric(
          "🍁 天皇賞（秋） 本命推奨",
          f"{best_horse['num']}番 {best_horse['horse']}({best_horse['jockey']})",
          help="東京適性・瞬発力・枠順・騎手手腕を網羅した最高期待値馬",
      )
    with c_p3:
      st.write("**【天皇賞（秋） 徹底アナライズ】**")
      st.info(
          f"{course_desc}\n\n{pace_comment}\n\n💡 **最有力判定**: 東京2000mの瞬発力勝負と馬場【{going}】、さらに絶好の枠順を味方につけ、**{best_horse['horse']} ({best_horse['jockey']})** が最も高い勝率期待値を示しています。"
      )

    st.markdown("---")
    st.markdown(
        '<div class="section-title">🏁 東京芝2000m リアルタイムアニメーション ＆ 100回モンテカルロ予想</div>',
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
          "tennosho_score": float(r["tennosho_score"]),
      })

    race_config_js = {
        "venue": "東京",
        "dist": 2000,
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

        const totalLapsProgress = 1.0;
        const spec = { dir: -1, startP: 0.20, goalP: 1.20, slopeP: [0.03, 0.14] };

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
            resultsTitle.innerText = "🏆 天皇賞（秋） リアルタイム着順結果";
            resultsContent.innerHTML = '<div style="padding:10px; color:#94a3b8;">⏱ ゲートが開きました！東京2000mの決戦スタート！</div>';

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
                    spurtPoint: spec.startP + (totalLapsProgress * (0.60 + Math.random() * 0.08)),
                    finished: false, rank: 0
                };
            });

            let finishedCount = 0;
            const totalHorses = runners.length;

            function animate() {
                group.innerHTML = '';
                runners.forEach((h) => {
                    if (!h.finished) {
                        let baseSpeed = h.speed * h.conditionMod * 0.000035;
                        
                        if (h.jockey_bonus > 1.0) baseSpeed *= 1.02;
                        if (h.pace_effect > 0) baseSpeed *= 1.06;

                        if (h.progress >= h.spurtPoint) {
                            baseSpeed *= (h.style === "差し" || h.style === "追込") ? (1.25 + h.burst * 0.0025) : 1.12;
                        }

                        const pNorm = (h.progress % 1.0);
                        if (pNorm >= spec.slopeP[0] && pNorm <= spec.slopeP[1]) {
                            const powerFactor = (h.power - 90) * 0.006;
                            baseSpeed *= Math.max(0.7, 0.88 + powerFactor);
                        }

                        h.staminaRem -= 0.04 * h.effectiveDrain;
                        if (h.staminaRem <= 0) baseSpeed *= 0.6;

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
                    status.innerText = `🍁 東京2000m 天皇賞（秋） (${raceConfig.going} / ${raceConfig.pace}) 熱戦中！`;
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

            status.innerText = "⚡ 瞬発力・東京適性・枠順を反映して100回モンテカルロシミュレーション中...";
            resultsTitle.innerText = "📊 100回シミュレーション総合結果 ＆ 天皇賞（秋）推奨買い目";

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
                    const burstScore = h.burst / effectiveDrain;
                    const randomMod = (Math.random() - 0.5) * 6.0;

                    const score = (burstScore * 0.35) + (h.speed * 0.30) + (h.stamina * 0.20) + (h.power * 0.15) + h.jockey_bonus + h.gate_bonus + h.pace_effect + randomMod;
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
                <strong>🎯 天皇賞（秋） AI自動構築買い目 (${raceConfig.going} / ${raceConfig.pace})</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${t1} - (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${t1} － 相手 (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${t1}, ${t2} → 2着 ${t1}, ${t2}, ${t3} → 3着 ${t1}, ${t2}, ${t3}, ${t4}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ 天皇賞（秋）シミュレーション＆買い目構築完了";
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
      '<div class="section-title">📈 天皇賞（秋）出走馬 東京適性・AIレーダー</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "東京芝2000mに必要な瞬発力、スピード、枠順ロス・騎手補正を網羅した総合期待値の比較一覧です。"
  )

  df_ana = df_all[df_all["horse"].isin(selected_horses)].copy()
  if not df_ana.empty:
    df_ana["期待値スコア"] = (
        df_ana["odds"] * (df_ana["burst"] + df_ana["speed"]) / 200.0
    ).round(2)
    st.dataframe(
        df_ana[[
            "gate",
            "horse",
            "jockey",
            "odds",
            "burst",
            "speed",
            "stamina",
            "power",
            "heavy",
            "期待値スコア",
        ]].rename(columns={
            "gate": "枠番",
            "horse": "馬名",
            "jockey": "騎手",
            "odds": "想定オッズ",
            "burst": "瞬発力",
            "speed": "スピード",
            "stamina": "スタミナ",
            "power": "パワー",
            "heavy": "重馬場適性",
        }),
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.info("出走馬が選択されていません。")

with tab_db:
  st.markdown(
      f'<div class="section-title">📊 天皇賞（秋） 総合データベース（全{len(df_all)}頭）</div>',
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
          "burst",
          "speed",
          "stamina",
          "sire",
      ]].rename(columns={
          "gate": "確定枠番",
          "horse": "馬名",
          "jockey": "騎手",
          "style": "脚質",
          "odds": "想定オッズ",
          "burst": "瞬発力",
          "speed": "スピード",
          "stamina": "スタミナ",
          "sire": "父",
      }),
      use_container_width=True,
      hide_index=True,
  )
