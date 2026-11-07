import json
import numpy as np
import pandas as pd
import streamlit as st

# 1. ページ基本設定 ＆ デザイン
st.set_page_config(
    page_title="JRA 2026秋季重賞 4レース精密シミュレーター Pro",
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
    <h1 style="color: #f8fafc; margin: 0; font-size: 26px;">🏇 2026秋季重賞 4レース精密シミュレーター <span style="color: #38bdf8; font-size: 18px;">PRO</span></h1>
    <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 14px;">公式画像出馬表完全準拠版（京都JS・京王杯2歳S・みやこS・アルゼンチン共和国杯）</p>
</div>
""",
    unsafe_allow_html=True,
)


# ==========================================
# データベース定義（画像に基づく完全最新データ）
# ==========================================

# ① 京都ジャンプステークス（11/7・京都 障害3100m）
@st.cache_data
def get_kyoto_js_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "ロードリベラシオン",
          "jockey": "五十嵐雄",
          "style": "先行",
          "speed": 92,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 91,
          "odds": 12.0,
      },
      {
          "num": 2,
          "horse": "グラニットピーク",
          "jockey": "坂口智康",
          "style": "差し",
          "speed": 93,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 15.0,
      },
      {
          "num": 3,
          "horse": "トーアモルペウス",
          "jockey": "大江原圭",
          "style": "差し",
          "speed": 91,
          "stamina": 94,
          "power": 93,
          "heavy": 93,
          "burst": 91,
          "odds": 22.0,
      },
      {
          "num": 4,
          "horse": "メイショウアツイタ",
          "jockey": "難波剛健",
          "style": "先行",
          "speed": 94,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 94,
          "odds": 6.5,
      },
      {
          "num": 5,
          "horse": "ヴラディア",
          "jockey": "上野翔",
          "style": "差し",
          "speed": 92,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 92,
          "odds": 18.0,
      },
      {
          "num": 6,
          "horse": "シホノスペランツァ",
          "jockey": "森一馬",
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 96,
          "heavy": 96,
          "burst": 97,
          "odds": 2.8,
      },
      {
          "num": 7,
          "horse": "コンテナワールド",
          "jockey": "井上敏樹",
          "style": "追込",
          "speed": 90,
          "stamina": 94,
          "power": 93,
          "heavy": 93,
          "burst": 91,
          "odds": 30.0,
      },
      {
          "num": 8,
          "horse": "スマイルスルー",
          "jockey": "小牧加矢太",
          "style": "先行",
          "speed": 95,
          "stamina": 95,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 4.5,
      },
      {
          "num": 9,
          "horse": "ディナースタ",
          "jockey": "高田潤",
          "style": "差し",
          "speed": 94,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 5.0,
      },
  ])


# ② 京王杯2歳ステークス（11/7・東京 芝1400m）
@st.cache_data
def get_keio_2yo_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "アテナブレイブ",
          "jockey": "田辺裕信",
          "style": "差し",
          "speed": 92,
          "stamina": 91,
          "power": 92,
          "heavy": 91,
          "burst": 92,
          "odds": 25.0,
      },
      {
          "num": 2,
          "horse": "フレイコン",
          "jockey": "マーカン",
          "style": "差し",
          "speed": 91,
          "stamina": 91,
          "power": 91,
          "heavy": 91,
          "burst": 91,
          "odds": 40.0,
      },
      {
          "num": 3,
          "horse": "ニシノトラノスケ",
          "jockey": "大野拓弥",
          "style": "先行",
          "speed": 93,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 93,
          "odds": 18.0,
      },
      {
          "num": 4,
          "horse": "ノーセット",
          "jockey": "津村明秀",
          "style": "差し",
          "speed": 94,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 94,
          "odds": 12.0,
      },
      {
          "num": 5,
          "horse": "グルーヴェンス",
          "jockey": "横山武史",
          "style": "先行",
          "speed": 95,
          "stamina": 93,
          "power": 94,
          "heavy": 93,
          "burst": 95,
          "odds": 6.5,
      },
      {
          "num": 6,
          "horse": "インパルスドライブ",
          "jockey": "C.デムーロ",
          "style": "差し",
          "speed": 97,
          "stamina": 94,
          "power": 95,
          "heavy": 94,
          "burst": 97,
          "odds": 2.5,
      },
      {
          "num": 7,
          "horse": "シルバーノライダー",
          "jockey": "小林美駒",
          "style": "差し",
          "speed": 90,
          "stamina": 91,
          "power": 90,
          "heavy": 90,
          "burst": 91,
          "odds": 60.0,
      },
      {
          "num": 8,
          "horse": "ジオパークカツキ",
          "jockey": "ブーシャ",
          "style": "先行",
          "speed": 92,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 28.0,
      },
      {
          "num": 9,
          "horse": "ブルージェイ",
          "jockey": "C.ルメール",
          "style": "差し",
          "speed": 96,
          "stamina": 93,
          "power": 94,
          "heavy": 93,
          "burst": 96,
          "odds": 3.8,
      },
      {
          "num": 10,
          "horse": "ロンドンガーズ",
          "jockey": "三浦皇成",
          "style": "先行",
          "speed": 94,
          "stamina": 92,
          "power": 93,
          "heavy": 92,
          "burst": 94,
          "odds": 9.0,
      },
  ])


# ③ みやこステークス（11/8・京都 ダート1800m）
@st.cache_data
def get_miyako_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "トリポリタニア",
          "jockey": "C.デムーロ",
          "style": "差し",
          "speed": 95,
          "stamina": 94,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 8.0,
      },
      {
          "num": 2,
          "horse": "バスタードサフラン",
          "jockey": "酒井学",
          "style": "差し",
          "speed": 91,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 91,
          "odds": 45.0,
      },
      {
          "num": 3,
          "horse": "パシアンジャン",
          "jockey": "田口貫太",
          "style": "差し",
          "speed": 92,
          "stamina": 93,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 35.0,
      },
      {
          "num": 4,
          "horse": "ビービークローサー",
          "jockey": "坂井瑠星",
          "style": "先行",
          "speed": 96,
          "stamina": 95,
          "power": 96,
          "heavy": 96,
          "burst": 96,
          "odds": 6.0,
      },
      {
          "num": 5,
          "horse": "ヴァルツァーシャル",
          "jockey": "斎藤新",
          "style": "差し",
          "speed": 94,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 94,
          "odds": 18.0,
      },
      {
          "num": 6,
          "horse": "シゲルショウグン",
          "jockey": "太宰啓介",
          "style": "逃げ",
          "speed": 93,
          "stamina": 93,
          "power": 94,
          "heavy": 94,
          "burst": 92,
          "odds": 50.0,
      },
      {
          "num": 7,
          "horse": "マイノワール",
          "jockey": "武豊",
          "style": "差し",
          "speed": 96,
          "stamina": 95,
          "power": 96,
          "heavy": 96,
          "burst": 96,
          "odds": 7.5,
      },
      {
          "num": 8,
          "horse": "テスティモーネ",
          "jockey": "幸英明",
          "style": "先行",
          "speed": 93,
          "stamina": 93,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 22.0,
      },
      {
          "num": 9,
          "horse": "ラムジェット",
          "jockey": "三浦皇成",
          "style": "差し",
          "speed": 98,
          "stamina": 97,
          "power": 98,
          "heavy": 98,
          "burst": 99,
          "odds": 2.2,
      },
      {
          "num": 10,
          "horse": "ムルソー",
          "jockey": "松山弘平",
          "style": "先行",
          "speed": 96,
          "stamina": 95,
          "power": 97,
          "heavy": 97,
          "burst": 96,
          "odds": 5.0,
      },
      {
          "num": 11,
          "horse": "ロードクロンヌ",
          "jockey": "横山和生",
          "style": "差し",
          "speed": 93,
          "stamina": 94,
          "power": 93,
          "heavy": 93,
          "burst": 93,
          "odds": 25.0,
      },
      {
          "num": 12,
          "horse": "サイモンザナドゥ",
          "jockey": "富田暁",
          "style": "差し",
          "speed": 92,
          "stamina": 92,
          "power": 92,
          "heavy": 92,
          "burst": 92,
          "odds": 60.0,
      },
      {
          "num": 13,
          "horse": "レヴォントゥレット",
          "jockey": "鮫島克駿",
          "style": "差し",
          "speed": 94,
          "stamina": 94,
          "power": 94,
          "heavy": 94,
          "burst": 94,
          "odds": 16.0,
      },
      {
          "num": 14,
          "horse": "ルシュヴァルドール",
          "jockey": "北村友一",
          "style": "先行",
          "speed": 95,
          "stamina": 94,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 12.0,
      },
      {
          "num": 15,
          "horse": "ショウナンバンライ",
          "jockey": "池添謙一",
          "style": "差し",
          "speed": 94,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 94,
          "odds": 20.0,
      },
      {
          "num": 16,
          "horse": "シリウスコルト",
          "jockey": "浜中俊",
          "style": "先行",
          "speed": 95,
          "stamina": 95,
          "power": 96,
          "heavy": 96,
          "burst": 96,
          "odds": 9.5,
      },
  ])


# ④ アルゼンチン共和国杯（11/8・東京 芝2500m）
@st.cache_data
def get_arq_db():
  return pd.DataFrame([
      {
          "num": 1,
          "horse": "ジューティーダーリン",
          "jockey": "大野拓弥",
          "style": "先行",
          "speed": 93,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 20.0,
      },
      {
          "num": 2,
          "horse": "ビザンチンドリーム",
          "jockey": "国分優作",
          "style": "追込",
          "speed": 94,
          "stamina": 96,
          "power": 94,
          "heavy": 94,
          "burst": 96,
          "odds": 15.0,
      },
      {
          "num": 3,
          "horse": "マイネルエンペラー",
          "jockey": "吉村誠之",
          "style": "先行",
          "speed": 92,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 92,
          "odds": 35.0,
      },
      {
          "num": 4,
          "horse": "ミラージュナイト",
          "jockey": "西村淳也",
          "style": "差し",
          "speed": 94,
          "stamina": 96,
          "power": 94,
          "heavy": 94,
          "burst": 94,
          "odds": 18.0,
      },
      {
          "num": 5,
          "horse": "ドゥラドーレス",
          "jockey": "C.ルメール",
          "style": "差し",
          "speed": 98,
          "stamina": 98,
          "power": 96,
          "heavy": 96,
          "burst": 99,
          "odds": 2.2,
      },
      {
          "num": 6,
          "horse": "ファミリータイム",
          "jockey": "菅原明良",
          "style": "差し",
          "speed": 93,
          "stamina": 95,
          "power": 93,
          "heavy": 93,
          "burst": 93,
          "odds": 40.0,
      },
      {
          "num": 7,
          "horse": "ファイアンクランツ",
          "jockey": "岩田望来",
          "style": "先行",
          "speed": 96,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 96,
          "odds": 5.0,
      },
      {
          "num": 8,
          "horse": "ジョイボーイ",
          "jockey": "横山武史",
          "style": "先行",
          "speed": 95,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 8.0,
      },
      {
          "num": 9,
          "horse": "レッドバンデ",
          "jockey": "佐々木大",
          "style": "差し",
          "speed": 92,
          "stamina": 94,
          "power": 93,
          "heavy": 93,
          "burst": 92,
          "odds": 50.0,
      },
      {
          "num": 10,
          "horse": "ボーンディスウェイ",
          "jockey": "マーカン",
          "style": "先行",
          "speed": 93,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 30.0,
      },
      {
          "num": 11,
          "horse": "ウエストナウ",
          "jockey": "横山典弘",
          "style": "差し",
          "speed": 95,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 96,
          "odds": 9.5,
      },
      {
          "num": 12,
          "horse": "メイショウゲキリン",
          "jockey": "田辺裕信",
          "style": "逃げ",
          "speed": 93,
          "stamina": 94,
          "power": 94,
          "heavy": 94,
          "burst": 92,
          "odds": 45.0,
      },
      {
          "num": 13,
          "horse": "マイネルカンバーナ",
          "jockey": "津村明秀",
          "style": "差し",
          "speed": 93,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 93,
          "odds": 25.0,
      },
      {
          "num": 14,
          "horse": "ミクニインスパイア",
          "jockey": "岩田康誠",
          "style": "先行",
          "speed": 94,
          "stamina": 95,
          "power": 94,
          "heavy": 94,
          "burst": 94,
          "odds": 22.0,
      },
      {
          "num": 15,
          "horse": "ホーエリート",
          "jockey": "戸崎圭太",
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 95,
          "heavy": 95,
          "burst": 97,
          "odds": 6.0,
      },
      {
          "num": 16,
          "horse": "キングズパレス",
          "jockey": "松岡正海",
          "style": "差し",
          "speed": 96,
          "stamina": 97,
          "power": 96,
          "heavy": 96,
          "burst": 97,
          "odds": 7.0,
      },
      {
          "num": 17,
          "horse": "キングスコール",
          "jockey": "吉田豊",
          "style": "先行",
          "speed": 95,
          "stamina": 96,
          "power": 95,
          "heavy": 95,
          "burst": 95,
          "odds": 12.0,
      },
      {
          "num": 18,
          "horse": "ミステリーウェイ",
          "jockey": "松本大輝",
          "style": "逃げ",
          "speed": 92,
          "stamina": 93,
          "power": 93,
          "heavy": 93,
          "burst": 91,
          "odds": 80.0,
      },
  ])


# ==========================================
# SVGアニメーション ＆ モンテカルロシミュレーターHTMLジェネレータ
# ==========================================
def get_sim_html(horses_data, race_config):
  html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; touch-action: manipulation; }
        body { margin: 0; padding: 0; font-family: -apple-system, sans-serif; background-color: #080c14; color: white; }
        .sim-container { width: 100%; max-width: 900px; margin: 0 auto; padding: 4px; text-align: center; }
        .btn-group { display: flex; gap: 10px; margin-bottom: 12px; }
        .start-btn {
            flex: 1; height: 50px; background: linear-gradient(135deg, #059669, #047857); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(5,150,105,0.3);
        }
        .sim100-btn {
            flex: 1; height: 50px; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,0.3);
        }
        .status-box { font-size: 15px; font-weight: bold; color: #34d399; min-height: 28px; margin-bottom: 8px; }
        .svg-wrapper { 
            width: 100%; background: #06120d; border-radius: 14px; border: 2px solid #1e3a2f; padding: 10px; box-sizing: border-box; overflow: hidden;
        }
        .results-box { 
            margin-top: 14px; background: #111827; padding: 16px; border-radius: 12px; border: 1px solid #374151; text-align: left; max-height: 450px; overflow-y: auto;
        }
        .results-table-wrapper { width: 100%; overflow-x: auto; }
        .results-table { width: 100%; border-collapse: collapse; margin-top: 8px; min-width: 550px; }
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
            <button id="sim100Btn" class="sim100-btn">⚡ 100回モンテカルロ予想 ＆ 買い目</button>
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

        const spec = { dir: -1, startP: 0.20, goalP: 1.20 };

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
            resultsContent.innerHTML = '<div style="padding:10px; color:#94a3b8;">⏱ ゲートが開きました！決戦スタート！</div>';

            const runners = horsesData.map((h, i) => {
                const laneOffset = (i - (horsesData.length - 1) / 2) * 1.8;
                const wakuStyle = getWakuStyle(h.num, horsesData.length);
                const effectiveDrain = Math.max(0.65, raceConfig.drain);
                const conditionMod = 0.93 + Math.random() * 0.14;

                return {
                    ...h, laneOffset, wakuStyle,
                    progress: spec.startP, targetProgress: spec.goalP,
                    effectiveDrain, conditionMod,
                    staminaRem: h.stamina * 10 / effectiveDrain,
                    spurtPoint: spec.startP + (0.58 + Math.random() * 0.08),
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
                        if (h.jockey_bonus > 1.2) baseSpeed *= 1.02;
                        if (h.pace_effect > 0) baseSpeed *= 1.05;

                        if (h.progress >= h.spurtPoint) {
                            baseSpeed *= (h.style === "差し" || h.style === "追込") ? (1.28 + h.burst * 0.0022) : 1.08;
                        }

                        h.staminaRem -= 0.038 * h.effectiveDrain;
                        if (h.staminaRem <= 0) baseSpeed *= 0.58;
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
                        <text x="0" y="3.5" font-size="9" font-weight="bold" fill="${h.wakuStyle.text}" text-anchor="middle">${h.num}</text>
                        <text x="11" y="3.5" font-size="10" font-weight="bold" fill="#ffffff">${h.horse} (${h.jockey})</text>
                    `;
                    group.appendChild(g);
                });

                if (finishedCount === 0) {
                    status.innerText = `🏁 熱戦中！`;
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
                        html += `<tr><td class="rank-badge ${rankClass}">${h.rank}着</td><td><span class="waku-tag" style="background:${h.wakuStyle.bg}; color:${h.wakuStyle.text};">${h.num}</span></td><td style="text-align:left;"><strong>${h.horse}</strong></td><td>${h.jockey}</td><td>${h.style}</td></tr>`;
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

            status.innerText = "⚡ 100回モンテカルロシミュレーション実行中...";
            resultsTitle.innerText = "📊 100回試行シミュレーション総合結果 ＆ 推奨買い目";

            const stats = {};
            horsesData.forEach(h => {
                stats[h.horse] = {
                    num: h.num, name: h.horse, jockey: h.jockey, style: h.style,
                    wakuStyle: getWakuStyle(h.num, horsesData.length),
                    first: 0, second: 0, third: 0, totalRank: 0
                };
            });

            const SIM_COUNT = 100;
            for (let sim = 0; sim < SIM_COUNT; sim++) {
                let raceRes = horsesData.map(h => {
                    const effectiveDrain = Math.max(0.65, raceConfig.drain);
                    const burstScore = h.burst / effectiveDrain;
                    const randomMod = (Math.random() - 0.5) * 5.8;
                    const score = (burstScore * 0.36) + (h.speed * 0.30) + (h.stamina * 0.18) + (h.power * 0.16) + h.jockey_bonus + h.gate_bonus + h.pace_effect + randomMod;
                    return { name: h.horse, score: score };
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
                <strong>🎯 AI自動構築買い目</strong><br>
                ・ <strong>本命・馬連 (流し)</strong>: ${t1} - (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連複 (軸1頭流し)</strong>: 軸 ${t1} － 相手 (${t2}, ${t3}, ${t4})<br>
                ・ <strong>3連単 (フォーメーション)</strong>: 1着 ${t1}, ${t2} → 2着 ${t1}, ${t2}, ${t3} → 3着 ${t1}, ${t2}, ${t3}, ${t4}
            </div>`;

            resultsContent.innerHTML = html;
            status.innerText = "✅ 100回シミュレーション＆買い目構築完了";
        }
    </script>
</body>
</html>"""

  return (
      html_template.replace("__HORSES_JSON__", json.dumps(horses_data))
      .replace("__RACE_CONFIG_JSON__", json.dumps(race_config))
  )


# ==========================================
# メイン画面：4つの重賞タブ構成（開催競馬場準拠）
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🍁 11/7 京都JS (京都障害)",
    "🌸 11/7 京王杯2歳S (東京芝)",
    "⚡ 11/8 みやこS (京都ダート)",
    "👑 11/8 アルゼンチン共和国杯 (東京芝)",
])

# ------------------------------------------
# ① 京都ジャンプステークス
# ------------------------------------------
with tab1:
  df_1 = get_kyoto_js_db()
  st.markdown(
      '<div class="section-title">📅 11月7日(土) 京都ジャンプステークス (京都競馬場・障害3100m)</div>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    g1 = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"], key="g_kjs")
  with col2:
    p1 = st.selectbox(
        "展開ペース", ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"], key="p_kjs"
    )

  sel_1 = st.multiselect(
      "出走馬選択",
      options=df_1["horse"].tolist(),
      default=df_1["horse"].tolist(),
      key="ms_kjs",
  )

  if len(sel_1) >= 2:
    df_r = df_1[df_1["horse"].isin(sel_1)].copy().reset_index(drop=True)
    drain = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[g1]
    top_j = ["シホノスペランツァ", "スマイルスルー", "ディナースタ"]
    df_r["jockey_bonus"] = df_r["jockey"].apply(
        lambda x: 4.5 if x in ["森一馬", "高田潤"] else 1.2
    )
    df_r["gate_bonus"] = df_r["num"].apply(lambda n: 1.5 if n <= 4 else 1.0)
    df_r["pace_effect"] = 0.0

    horses_js = df_r.to_dict(orient="records")
    st.components.v1.html(
        get_sim_html(horses_js, {"drain": drain, "going": g1, "pace": p1}),
        height=850,
    )

# ------------------------------------------
# ② 京王杯2歳ステークス
# ------------------------------------------
with tab2:
  df_2 = get_keio_2yo_db()
  st.markdown(
      '<div class="section-title">📅 11月7日(土) 京王杯2歳ステークス (東京競馬場・芝1400m)</div>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    g2 = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"], key="g_k2yo")
  with col2:
    p2 = st.selectbox(
        "展開ペース", ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"], key="p_k2yo"
    )

  sel_2 = st.multiselect(
      "出走馬選択",
      options=df_2["horse"].tolist(),
      default=df_2["horse"].tolist(),
      key="ms_k2yo",
  )

  if len(sel_2) >= 2:
    df_r = df_2[df_2["horse"].isin(sel_2)].copy().reset_index(drop=True)
    drain = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[g2]
    top_j = ["C.ルメール", "C.デムーロ", "横山武史"]
    df_r["jockey_bonus"] = df_r["jockey"].apply(
        lambda x: 5.0 if x in top_j else 1.2
    )
    df_r["gate_bonus"] = df_r["num"].apply(lambda n: 2.0 if n <= 3 else 1.0)
    df_r["pace_effect"] = (
        df_r["style"].apply(lambda s: 5.0 if s in ["差し", "追込"] else -4.0)
        if "ハイペース" in p2
        else 0.0
    )

    horses_js = df_r.to_dict(orient="records")
    st.components.v1.html(
        get_sim_html(horses_js, {"drain": drain, "going": g2, "pace": p2}),
        height=850,
    )

# ------------------------------------------
# ③ みやこステークス
# ------------------------------------------
with tab3:
  df_3 = get_miyako_db()
  st.markdown(
      '<div class="section-title">📅 11月8日(日) みやこステークス (京都競馬場・ダート1800m)</div>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    g3 = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"], key="g_miyako")
  with col2:
    p3 = st.selectbox(
        "展開ペース", ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"], key="p_miyako"
    )

  sel_3 = st.multiselect(
      "出走馬選択",
      options=df_3["horse"].tolist(),
      default=df_3["horse"].tolist(),
      key="ms_miyako",
  )

  if len(sel_3) >= 2:
    df_r = df_3[df_3["horse"].isin(sel_3)].copy().reset_index(drop=True)
    drain = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[g3]
    top_j = ["三浦皇成", "坂井瑠星", "松山弘平", "武豊"]
    df_r["jockey_bonus"] = df_r["jockey"].apply(
        lambda x: 5.0 if x in top_j else 1.2
    )
    df_r["gate_bonus"] = df_r["num"].apply(lambda n: 2.0 if n <= 4 else 1.0)
    df_r["pace_effect"] = (
        df_r["style"].apply(lambda s: 5.0 if s in ["先行", "逃げ"] else -3.0)
        if "スロー" in p3
        else 0.0
    )

    horses_js = df_r.to_dict(orient="records")
    st.components.v1.html(
        get_sim_html(horses_js, {"drain": drain, "going": g3, "pace": p3}),
        height=850,
    )

# ------------------------------------------
# ④ アルゼンチン共和国杯
# ------------------------------------------
with tab4:
  df_4 = get_arq_db()
  st.markdown(
      '<div class="section-title">📅 11月8日(日) アルゼンチン共和国杯 (東京競馬場・芝2500m)</div>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    g4 = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"], key="g_arq")
  with col2:
    p4 = st.selectbox(
        "展開ペース", ["ハイペース (H)", "ミドルペース (M)", "スローペース (S)"], key="p_arq"
    )

  sel_4 = st.multiselect(
      "出走馬選択",
      options=df_4["horse"].tolist(),
      default=df_4["horse"].tolist(),
      key="ms_arq",
  )

  if len(sel_4) >= 2:
    df_r = df_4[df_4["horse"].isin(sel_4)].copy().reset_index(drop=True)
    drain = {"良": 1.0, "稍重": 1.15, "重": 1.35, "不良": 1.55}[g4]
    top_j = ["C.ルメール", "戸崎圭太", "横山武史"]
    df_r["jockey_bonus"] = df_r["jockey"].apply(
        lambda x: 5.0 if x in top_j else 1.2
    )
    df_r["gate_bonus"] = df_r["num"].apply(lambda n: 2.0 if n <= 3 else 1.0)
    df_r["pace_effect"] = (
        df_r["style"].apply(lambda s: 5.0 if s in ["差し", "追込"] else -4.0)
        if "ハイペース" in p4
        else 0.0
    )

    horses_js = df_r.to_dict(orient="records")
    st.components.v1.html(
        get_sim_html(horses_js, {"drain": drain, "going": g4, "pace": p4}),
        height=850,
    )
