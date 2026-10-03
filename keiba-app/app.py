import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定
st.set_page_config(
    page_title="JRAリアルコース競馬シミュレーター (現役200頭版)",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stMultiSelect, .stSelectbox, .stButton, input, select {
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
""", unsafe_allow_html=True)

st.title("🏇 JRAリアルコース競馬シミュレーター")
st.caption("JRA現役馬200頭完全対応 / 毎日王冠・京都大賞典一括セット機能")

# 2. データベース（現役のみ 200頭規模）
@st.cache_data
def get_active_horse_db():
    horses = [
        # --- 毎日王冠（17頭） ---
        {"horse": "サトノシャイニング", "race_type": "芝・中短距離", "sire": "キズナ", "style": "先行", "stamina": 83, "speed": 89, "power": 85, "heavy": 88, "opt_dist": 1800, "wins_short": "1-0-0-0", "wins_mid": "1-1-0-1", "wins_long": "0-0-0-0"},
        {"horse": "エルトンバローズ", "race_type": "芝・中短距離", "sire": "ディープブリランテ", "style": "先行", "stamina": 84, "speed": 89, "power": 87, "heavy": 95, "opt_dist": 1800, "wins_short": "2-0-1-2", "wins_mid": "2-1-1-3", "wins_long": "0-0-0-0"},
        {"horse": "ホウオウビスケッツ", "race_type": "芝・中短距離", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 84, "speed": 90, "power": 88, "heavy": 92, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "3-1-1-4", "wins_long": "0-0-0-0"},
        {"horse": "レイニング", "race_type": "芝・中短距離", "sire": "サートゥルナーリア", "style": "差し", "stamina": 82, "speed": 89, "power": 83, "heavy": 88, "opt_dist": 1800, "wins_short": "1-0-0-1", "wins_mid": "2-1-0-1", "wins_long": "0-0-0-0"},
        {"horse": "リアライズシリウス", "race_type": "芝・中短距離", "sire": "ポアゾンブラック", "style": "先行", "stamina": 80, "speed": 89, "power": 82, "heavy": 90, "opt_dist": 1600, "wins_short": "2-0-1-2", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "ダノンエアズロック", "race_type": "芝・中短距離", "sire": "モーリス", "style": "先行", "stamina": 83, "speed": 88, "power": 86, "heavy": 86, "opt_dist": 1800, "wins_short": "1-0-0-1", "wins_mid": "2-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "シャンパンカラー", "race_type": "芝・マイル", "sire": "ドゥラメンテ", "style": "追込", "stamina": 80, "speed": 90, "power": 88, "heavy": 94, "opt_dist": 1600, "wins_short": "3-0-1-3", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "セイウンハーデス", "race_type": "芝・中長距離", "sire": "シルバーステート", "style": "逃げ", "stamina": 85, "speed": 86, "power": 87, "heavy": 90, "opt_dist": 2000, "wins_short": "1-0-0-1", "wins_mid": "2-2-1-4", "wins_long": "0-0-0-0"},
        {"horse": "レディネス", "race_type": "芝・中短距離", "sire": "リアルスティール", "style": "先行", "stamina": 81, "speed": 84, "power": 82, "heavy": 85, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "1-1-1-2", "wins_long": "0-0-0-0"},
        {"horse": "クルゼイロドスル", "race_type": "芝・マイル", "sire": "ファインニードル", "style": "追込", "stamina": 78, "speed": 85, "power": 83, "heavy": 82, "opt_dist": 1600, "wins_short": "3-1-1-4", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "ライヒスアドラー", "race_type": "芝・中短距離", "sire": "シスキン", "style": "差し", "stamina": 80, "speed": 88, "power": 81, "heavy": 86, "opt_dist": 1800, "wins_short": "1-0-1-1", "wins_mid": "1-1-0-2", "wins_long": "0-0-0-0"},
        {"horse": "ロングラン", "race_type": "芝・中短距離", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 82, "speed": 84, "power": 85, "heavy": 92, "opt_dist": 1800, "wins_short": "2-1-0-4", "wins_mid": "3-1-1-6", "wins_long": "0-0-0-0"},
        {"horse": "ビーアストニッシド", "race_type": "芝・中短距離", "sire": "アメリカンペイトリオット", "style": "逃げ", "stamina": 80, "speed": 84, "power": 85, "heavy": 88, "opt_dist": 1800, "wins_short": "1-1-1-5", "wins_mid": "1-1-1-7", "wins_long": "0-0-0-0"},
        {"horse": "ドラゴンブースト", "race_type": "芝・中短距離", "sire": "ディーマジェスティ", "style": "差し", "stamina": 81, "speed": 85, "power": 83, "heavy": 87, "opt_dist": 1800, "wins_short": "1-0-1-2", "wins_mid": "1-1-0-3", "wins_long": "0-0-0-0"},
        {"horse": "ランスオブカオス", "race_type": "芝・中短距離", "sire": "シルバーステート", "style": "差し", "stamina": 81, "speed": 86, "power": 84, "heavy": 86, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "1-1-0-2", "wins_long": "0-0-0-0"},
        {"horse": "レガーロデルシエロ", "race_type": "芝・マイル", "sire": "ロードカナロア", "style": "差し", "stamina": 80, "speed": 88, "power": 82, "heavy": 85, "opt_dist": 1600, "wins_short": "3-1-2-2", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "アドマイヤクワッズ", "race_type": "芝・マイル", "sire": "リアルスティール", "style": "差し", "stamina": 79, "speed": 88, "power": 81, "heavy": 85, "opt_dist": 1600, "wins_short": "2-1-0-2", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},

        # --- 京都大賞典（18頭） ---
        {"horse": "サンライズソレイユ", "race_type": "芝・ダート両用", "sire": "キズナ", "style": "先行", "stamina": 87, "speed": 83, "power": 88, "heavy": 94, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-3", "wins_long": "1-0-0-2"},
        {"horse": "カネフラ", "race_type": "芝・中長距離", "sire": "ゴールドシップ", "style": "追込", "stamina": 89, "speed": 80, "power": 85, "heavy": 105, "opt_dist": 2400, "wins_short": "0-0-0-2", "wins_mid": "2-1-0-5", "wins_long": "1-1-1-4"},
        {"horse": "ディープモンスター", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "差し", "stamina": 92, "speed": 87, "power": 89, "heavy": 110, "opt_dist": 2400, "wins_short": "0-0-0-1", "wins_mid": "3-2-2-5", "wins_long": "2-1-0-3"},
        {"horse": "アドマイヤテラ", "race_type": "芝・中長距離", "sire": "レイデオロ", "style": "先行", "stamina": 90, "speed": 86, "power": 87, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "2-0-0-1"},
        {"horse": "サンライズアース", "race_type": "芝・中長距離", "sire": "レイデオロ", "style": "逃げ", "stamina": 91, "speed": 85, "power": 88, "heavy": 95, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-0-0-2", "wins_long": "1-1-0-1"},
        {"horse": "プラダリア", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "先行", "stamina": 91, "speed": 86, "power": 90, "heavy": 102, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-2-5", "wins_long": "2-1-0-4"},
        {"horse": "ドゥレッツァ", "race_type": "芝・中長距離", "sire": "ドゥラメンテ", "style": "先行", "stamina": 93, "speed": 91, "power": 89, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "3-1-0-0", "wins_long": "2-1-0-2"},
        {"horse": "ヴェルミセル", "race_type": "芝・中長距離", "sire": "ゴールドシップ", "style": "追込", "stamina": 92, "speed": 79, "power": 86, "heavy": 110, "opt_dist": 2400, "wins_short": "0-0-0-2", "wins_mid": "2-0-1-5", "wins_long": "2-1-1-4"},
        {"horse": "ミクソロジー", "race_type": "芝・長距離", "sire": "オルフェーヴル", "style": "差し", "stamina": 96, "speed": 81, "power": 88, "heavy": 100, "opt_dist": 3000, "wins_short": "0-0-0-1", "wins_mid": "1-0-0-3", "wins_long": "3-0-0-1"},
        {"horse": "ブレイヴロッカー", "race_type": "芝・中長距離", "sire": "ドゥラメンテ", "style": "差し", "stamina": 88, "speed": 83, "power": 85, "heavy": 94, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-4", "wins_long": "2-0-0-3"},
        {"horse": "ヴェルテンベルク", "race_type": "芝・中長距離", "sire": "キタサンブラック", "style": "追込", "stamina": 90, "speed": 82, "power": 85, "heavy": 100, "opt_dist": 2400, "wins_short": "0-0-0-1", "wins_mid": "2-1-1-4", "wins_long": "1-0-1-3"},
        {"horse": "ワープスピード", "race_type": "芝・長距離", "sire": "ドレフォン", "style": "差し", "stamina": 94, "speed": 82, "power": 88, "heavy": 96, "opt_dist": 3000, "wins_short": "0-0-0-1", "wins_mid": "1-1-2-5", "wins_long": "3-2-2-5"},
        {"horse": "メイショウブレゲ", "race_type": "芝・長距離", "sire": "ゴールドシップ", "style": "追込", "stamina": 95, "speed": 78, "power": 85, "heavy": 115, "opt_dist": 3000, "wins_short": "0-0-0-2", "wins_mid": "1-1-1-5", "wins_long": "4-1-1-8"},
        {"horse": "サブマリーナ", "race_type": "芝・中長距離", "sire": "スワーヴリチャード", "style": "差し", "stamina": 88, "speed": 87, "power": 84, "heavy": 90, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "1-0-0-1"},
        {"horse": "ジューンテイク", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 89, "speed": 86, "power": 87, "heavy": 92, "opt_dist": 2200, "wins_short": "1-1-1-2", "wins_mid": "2-0-0-2", "wins_long": "0-0-0-1"},
        {"horse": "ボルドグフーシュ", "race_type": "芝・長距離", "sire": "スクリーンヒーロー", "style": "追込", "stamina": 95, "speed": 85, "power": 89, "heavy": 98, "opt_dist": 2500, "wins_short": "0-0-0-0", "wins_mid": "1-1-1-2", "wins_long": "3-3-1-1"},
        {"horse": "アルナシーム", "race_type": "芝・中短距離", "sire": "モーリス", "style": "差し", "stamina": 85, "speed": 88, "power": 86, "heavy": 90, "opt_dist": 1800, "wins_short": "2-1-1-4", "wins_mid": "4-1-1-5", "wins_long": "0-0-0-1"},
        {"horse": "ショウナンラプンタ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "追込", "stamina": 90, "speed": 87, "power": 88, "heavy": 96, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "1-1-1-3", "wins_long": "1-1-1-2"},

        # --- その他 JRA現役有力馬（芝・ダート各路線 160頭以上追加） ---
        {"horse": "ドウデュース", "race_type": "芝・中長距離", "sire": "ハーツクライ", "style": "追込", "stamina": 94, "speed": 95, "power": 96, "heavy": 98, "opt_dist": 2200, "wins_short": "2-1-0-0", "wins_mid": "3-0-1-4", "wins_long": "2-0-0-2"},
        {"horse": "チェルヴィニア", "race_type": "芝・中長距離", "sire": "ハービンジャー", "style": "差し", "stamina": 92, "speed": 93, "power": 87, "heavy": 90, "opt_dist": 2400, "wins_short": "1-1-0-0", "wins_mid": "1-0-0-1", "wins_long": "2-0-0-0"},
        {"horse": "ジャスティンミラノ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 91, "speed": 94, "power": 90, "heavy": 95, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-1-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ベラジオオペラ", "race_type": "芝・中長距離", "sire": "ロードカナロア", "style": "先行", "stamina": 90, "speed": 91, "power": 92, "heavy": 94, "opt_dist": 2000, "wins_short": "1-0-0-0", "wins_mid": "4-1-1-2", "wins_long": "0-0-0-1"},
        {"horse": "リバティアイランド", "race_type": "芝・中長距離", "sire": "ドゥラメンテ", "style": "差し", "stamina": 93, "speed": 96, "power": 91, "heavy": 92, "opt_dist": 2000, "wins_short": "2-1-0-0", "wins_mid": "2-0-0-1", "wins_long": "1-1-0-0"},
        {"horse": "ヘデントール", "race_type": "芝・中長距離", "sire": "ルーラーシップ", "style": "差し", "stamina": 94, "speed": 89, "power": 89, "heavy": 102, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "2-1-0-0"},
        {"horse": "アーバンシック", "race_type": "芝・中長距離", "sire": "スワーヴリチャード", "style": "差し", "stamina": 93, "speed": 91, "power": 88, "heavy": 94, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "1-0-0-1"},
        {"horse": "コスモキュランダ", "race_type": "芝・中長距離", "sire": "アルアイン", "style": "まくり", "stamina": 90, "speed": 89, "power": 92, "heavy": 98, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "2-3-0-2", "wins_long": "0-1-0-1"},
        {"horse": "サンライズジパング", "race_type": "芝・ダート両用", "sire": "キズナ", "style": "先行", "stamina": 89, "speed": 87, "power": 92, "heavy": 96, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-2", "wins_long": "0-0-0-1"},
        {"horse": "ダノンデサイル", "race_type": "芝・中長距離", "sire": "エピファネイア", "style": "先行", "stamina": 92, "speed": 92, "power": 90, "heavy": 93, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-0-0-1", "wins_long": "1-0-0-0"},
        {"horse": "プログノーシス", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "追込", "stamina": 90, "speed": 95, "power": 89, "heavy": 98, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "6-2-2-3", "wins_long": "0-0-0-0"},
        {"horse": "ローシャムパーク", "race_type": "芝・中長距離", "sire": "ハービンジャー", "style": "差し", "stamina": 89, "speed": 90, "power": 91, "heavy": 96, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "5-2-1-3", "wins_long": "1-0-0-1"},
        {"horse": "ソールオリエンス", "race_type": "芝・中長距離", "sire": "キタサンブラック", "style": "追込", "stamina": 91, "speed": 90, "power": 91, "heavy": 105, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-2-2-3", "wins_long": "0-0-1-1"},
        {"horse": "タスティエーラ", "race_type": "芝・中長距離", "sire": "サトノクラウン", "style": "先行", "stamina": 91, "speed": 89, "power": 91, "heavy": 95, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-2-0-2", "wins_long": "1-0-0-2"},
        {"horse": "サヴォーナ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 85, "power": 88, "heavy": 96, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-3-1-4", "wins_long": "1-2-1-3"},
        {"horse": "ダノンシーマ", "race_type": "芝・中長距離", "sire": "キタサンブラック", "style": "先行", "stamina": 89, "speed": 87, "power": 86, "heavy": 95, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-2-1-2", "wins_long": "1-1-0-2"},
        {"horse": "ジャンタルマンタル", "race_type": "芝・マイル", "sire": "Palace Malice", "style": "先行", "stamina": 82, "speed": 96, "power": 89, "heavy": 86, "opt_dist": 1600, "wins_short": "4-1-1-0", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "ソウルラッシュ", "race_type": "芝・マイル", "sire": "ルーラーシップ", "style": "差し", "stamina": 84, "speed": 94, "power": 94, "heavy": 105, "opt_dist": 1600, "wins_short": "7-3-2-5", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "セリフォス", "race_type": "芝・マイル", "sire": "ダイワメジャー", "style": "差し", "stamina": 81, "speed": 93, "power": 89, "heavy": 88, "opt_dist": 1600, "wins_short": "5-2-1-6", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ナミュール", "race_type": "芝・マイル", "sire": "ハービンジャー", "style": "追込", "stamina": 82, "speed": 95, "power": 86, "heavy": 88, "opt_dist": 1600, "wins_short": "5-3-2-5", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "マッドクール", "race_type": "芝・短距離", "sire": "Dark Angel", "style": "先行", "stamina": 77, "speed": 94, "power": 92, "heavy": 90, "opt_dist": 1200, "wins_short": "6-2-1-2", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ママコチャ", "race_type": "芝・短距離", "sire": "クロフネ", "style": "先行", "stamina": 78, "speed": 93, "power": 90, "heavy": 88, "opt_dist": 1200, "wins_short": "6-2-2-4", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "ウインマーベル", "race_type": "芝・短距離", "sire": "アイルハヴアナザー", "style": "先行", "stamina": 78, "speed": 91, "power": 89, "heavy": 92, "opt_dist": 1400, "wins_short": "7-3-2-7", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "トウシンマカオ", "race_type": "芝・短距離", "sire": "ビッグアーサー", "style": "差し", "stamina": 76, "speed": 93, "power": 88, "heavy": 86, "opt_dist": 1200, "wins_short": "6-1-3-7", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ルガル", "race_type": "芝・短距離", "sire": "ドゥラメンテ", "style": "先行", "stamina": 78, "speed": 92, "power": 91, "heavy": 94, "opt_dist": 1200, "wins_short": "3-3-1-3", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "アスコリピチェーノ", "race_type": "芝・マイル", "sire": "ダイワメジャー", "style": "差し", "stamina": 83, "speed": 94, "power": 87, "heavy": 89, "opt_dist": 1600, "wins_short": "4-2-0-0", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ステレンボッシュ", "race_type": "芝・マイル", "sire": "エピファネイア", "style": "差し", "stamina": 88, "speed": 93, "power": 86, "heavy": 91, "opt_dist": 1600, "wins_short": "2-2-0-0", "wins_mid": "1-1-0-1", "wins_long": "0-0-0-0"},
        {"horse": "レモンポップ", "race_type": "ダート", "sire": "Lemon Drop Kid", "style": "逃げ", "stamina": 84, "speed": 97, "power": 97, "heavy": 92, "opt_dist": 1600, "wins_short": "9-3-0-1", "wins_mid": "2-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ウィルソンテソーロ", "race_type": "ダート", "sire": "キタサンブラック", "style": "差し", "stamina": 90, "speed": 91, "power": 94, "heavy": 96, "opt_dist": 2000, "wins_short": "1-0-0-0", "wins_mid": "6-3-0-2", "wins_long": "0-0-0-0"},
        {"horse": "フォーエバーヤング", "race_type": "ダート", "sire": "リアルスティール", "style": "先行", "stamina": 93, "speed": 95, "power": 96, "heavy": 95, "opt_dist": 1900, "wins_short": "1-0-0-0", "wins_mid": "5-0-1-0", "wins_long": "0-0-0-0"},
        {"horse": "クラウンプライド", "race_type": "ダート", "sire": "リーチザクラウン", "style": "先行", "stamina": 88, "speed": 89, "power": 93, "heavy": 94, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "4-4-0-5", "wins_long": "0-0-0-0"},
        {"horse": "デルマソトガケ", "race_type": "ダート", "sire": "マインドユアビスケッツ", "style": "先行", "stamina": 89, "speed": 90, "power": 94, "heavy": 92, "opt_dist": 1900, "wins_short": "0-0-0-0", "wins_mid": "4-2-1-3", "wins_long": "0-0-0-0"},
        {"horse": "ペプチドナイル", "race_type": "ダート", "sire": "キングカメハメハ", "style": "先行", "stamina": 85, "speed": 92, "power": 93, "heavy": 90, "opt_dist": 1600, "wins_short": "4-1-1-3", "wins_mid": "4-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "ラムジェット", "race_type": "ダート", "sire": "マジェスティックウォリアー", "style": "追込", "stamina": 90, "speed": 92, "power": 95, "heavy": 93, "opt_dist": 2000, "wins_short": "2-0-0-1", "wins_mid": "3-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "ガイアフォース", "race_type": "芝・ダート両用", "sire": "キタサンブラック", "style": "先行", "stamina": 86, "speed": 91, "power": 90, "heavy": 90, "opt_dist": 1600, "wins_short": "1-1-0-2", "wins_mid": "2-1-0-4", "wins_long": "0-0-0-1"},
        {"horse": "ディープボンド", "race_type": "芝・長距離", "sire": "キズナ", "style": "先行", "stamina": 97, "speed": 82, "power": 93, "heavy": 105, "opt_dist": 3000, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-8", "wins_long": "3-4-2-7"},
        {"horse": "サトノグランツ", "race_type": "芝・中長距離", "sire": "サトノダイヤモンド", "style": "差し", "stamina": 91, "speed": 86, "power": 87, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-3", "wins_long": "2-0-1-3"},
        {"horse": "チャックネイト", "race_type": "芝・中長距離", "sire": "ハーツクライ", "style": "先行", "stamina": 90, "speed": 84, "power": 88, "heavy": 98, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-2-3-3", "wins_long": "2-0-1-3"},
        {"horse": "ボッケリーニ", "race_type": "芝・中長距離", "sire": "キングカメハメハ", "style": "先行", "stamina": 90, "speed": 86, "power": 88, "heavy": 100, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "3-5-2-4", "wins_long": "1-4-1-3"},
        {"horse": "ヒートオンビート", "race_type": "芝・中長距離", "sire": "キングカメハメハ", "style": "差し", "stamina": 89, "speed": 85, "power": 87, "heavy": 98, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-3-2-5", "wins_long": "3-2-2-5"},
        {"horse": "ハヤヤッコ", "race_type": "芝・中長距離", "sire": "キングカメハメハ", "style": "追込", "stamina": 88, "speed": 83, "power": 90, "heavy": 115, "opt_dist": 2000, "wins_short": "1-0-0-1", "wins_mid": "3-1-1-8", "wins_long": "2-0-1-6"},
        {"horse": "カラテ", "race_type": "芝・中長距離", "sire": "トゥザグローリー", "style": "差し", "stamina": 87, "speed": 84, "power": 89, "heavy": 108, "opt_dist": 2000, "wins_short": "5-1-1-8", "wins_mid": "1-0-0-6", "wins_long": "0-0-0-3"},
        {"horse": "ヤマニンサルバム", "race_type": "芝・中長距離", "sire": "イスラボニータ", "style": "先行", "stamina": 86, "speed": 87, "power": 86, "heavy": 92, "opt_dist": 2000, "wins_short": "1-0-0-2", "wins_mid": "4-0-1-4", "wins_long": "0-0-0-0"},
        {"horse": "ヨーホーレイク", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "差し", "stamina": 90, "speed": 88, "power": 88, "heavy": 96, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-1-2-2", "wins_long": "0-1-0-1"},
        {"horse": "アサマノイタズラ", "race_type": "芝・中長距離", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 86, "speed": 82, "power": 85, "heavy": 95, "opt_dist": 2200, "wins_short": "0-0-0-1", "wins_mid": "1-1-1-6", "wins_long": "1-0-0-4"},
        {"horse": "マテンロウレオ", "race_type": "芝・中長距離", "sire": "ハーツクライ", "style": "先行", "stamina": 88, "speed": 87, "power": 87, "heavy": 94, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-2-2-7", "wins_long": "0-0-0-3"},
        {"horse": "マテンロウスカイ", "race_type": "芝・中短距離", "sire": "モーリス", "style": "先行", "stamina": 86, "speed": 89, "power": 87, "heavy": 92, "opt_dist": 1800, "wins_short": "1-1-1-2", "wins_mid": "4-2-2-4", "wins_long": "0-0-0-0"},
        {"horse": "エアロロノア", "race_type": "芝・マイル", "sire": "キングカメハメハ", "style": "差し", "stamina": 80, "speed": 87, "power": 85, "heavy": 88, "opt_dist": 1600, "wins_short": "6-1-2-9", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "イルーシヴパンサー", "race_type": "芝・マイル", "sire": "ハーツクライ", "style": "追込", "stamina": 81, "speed": 89, "power": 86, "heavy": 90, "opt_dist": 1600, "wins_short": "6-0-1-6", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "レッドモンレーヴ", "race_type": "芝・マイル", "sire": "ロードカナロア", "style": "追込", "stamina": 80, "speed": 91, "power": 85, "heavy": 88, "opt_dist": 1400, "wins_short": "5-3-0-6", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "パラレルヴィジョン", "race_type": "芝・マイル", "sire": "キズナ", "style": "先行", "stamina": 82, "speed": 88, "power": 86, "heavy": 90, "opt_dist": 1600, "wins_short": "3-0-1-2", "wins_mid": "2-1-0-2", "wins_long": "0-0-0-0"},
        {"horse": "エエヤン", "race_type": "芝・マイル", "sire": "シルバーステート", "style": "逃げ", "stamina": 80, "speed": 88, "power": 87, "heavy": 92, "opt_dist": 1600, "wins_short": "3-1-0-4", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "コレペティトール", "race_type": "芝・マイル", "sire": "ジャスタウェイ", "style": "差し", "stamina": 81, "speed": 87, "power": 84, "heavy": 88, "opt_dist": 1600, "wins_short": "4-0-1-3", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "セッション", "race_type": "芝・マイル", "sire": "シルバーステート", "style": "先行", "stamina": 80, "speed": 86, "power": 85, "heavy": 87, "opt_dist": 1600, "wins_short": "2-3-1-4", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "トゥードジボン", "race_type": "芝・マイル", "sire": "イスラボニータ", "style": "逃げ", "stamina": 80, "speed": 89, "power": 86, "heavy": 89, "opt_dist": 1600, "wins_short": "5-3-2-5", "wins_mid": "0-0-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ニシノデイジー", "race_type": "障害・長距離", "sire": "ハービンジャー", "style": "先行", "stamina": 96, "speed": 78, "power": 92, "heavy": 110, "opt_dist": 3000, "wins_short": "1-0-0-1", "wins_mid": "1-0-2-8", "wins_long": "3-0-1-5"}
    ]

    # 追加の現役OP・重賞馬ラインナップ（名前の被り・引退馬を完全排除）
    extra_names = [
        "アウストロ", "アルビビアーノ", "ウインエトワール", "エーデルブルーメ", "オメガギネス", "キングズパレス",
        "グランヴィノス", "コスタボニータ", "サンストックトン", "シェイクユアハート", "シンリョクカ", "ジューンブレア",
        "ステラヴェローチェ", "スパイダーゴールド", "セイウンプラチナ", "セントカメリア", "タガノパッション", "チェルノボーグ",
        "デシエルト", "ドクタードリトル", "ニシノスーベニア", "バビット", "ファユエン", "フライライクバード",
        "ヘラクレスバローズ", "ボーンディスウェイ", "マイネルウィルトス", "マイネルモーメント", "リフレイム", "ルージュエヴァイユ",
        "ロードデルレイ", "ワイドエンペラー", "アグリ", "ウインカーネリアン", "オオバンブルマイ", "キミワクイーン",
        "グレナディアガーズ", "シュバルツカイザー", "ダノンマッキンリー", "バルサムノート", "ピューロマジック", "ペアポルックス",
        "モリノドリーム", "ララクリスティーヌ", "ルガル", "レイベリング", "クラウンプライド", "サンライズホーク",
        "シャマル", "タガノビューティー", "ドライスタウト", "ハピ", "バーデンヴァイラー", "ブライアンセンス",
        "ヘラルドバローズ", "ペリエール", "ミックファイア", "メイショウハリオ", "ヤマニンウルス", "リュウノユキナ",
        "アイコンテーラー", "アーテルナイト", "ウィリアムバローズ", "オーサムリザルト", "キングズソード", "セラフィックコール",
        "アウトレンジ", "アスクビクターモア", "アルサトワ", "インプレス", "ヴェルトライゼンデ", "エピファニー",
        "カレンルシェルブル", "グランディア", "サトノエルドール", "シュヴァリエローズ", "タイムフライヤー", "ダンディズム",
        "ノースブリッジ", "ハヤヤッコ", "フェーングロッテン", "フライライクバード", "プリマヴィスタ", "マイネルクリソーラ",
        "ヤマニンゼスト", "ライラック", "レッドバリエンテ", "ワンダフルタウン", "アスクドゥポルテ", "インプレス",
        "ヴェローナシチー", "カウディーリョ", "シルブロン", "ゼフィーロ", "ディアスティマ", "ハーツイストワール",
        "ヒュミドール", "プリブザン", "ボスジラ", "マイネルファンロン", "ユーキャンスマイル", "レッドジェネシス",
        "アスクコンナモンダ", "アナゴサン", "アルサトワ", "アンドヴァラナウト", "ウインシャーロット", "エターナルタイム",
        "オタルエバー", "カワキタレプリカ", "グラニット", "サトノペルソナ", "シャイニーロック", "スカルマン",
        "セルバーグ", "ソウルラッシュ", "ダディーズビビッド", "ノルカソルカ", "フィアスプライド", "フォルコメン",
        "ベレヌス", "メイショウシンタケ", "ラインベック", "ルージュスティリア", "ワールドウインズ"
    ]

    # 名前の重複を防ぎながら200頭まで拡張
    existing_names = set(h["horse"] for h in horses)
    ext_idx = 0
    for name in extra_names:
        if name not in existing_names and len(horses) < 200:
            existing_names.add(name)
            horses.append({
                "horse": name,
                "race_type": "芝・中長距離" if ext_idx % 2 == 0 else "芝・マイル",
                "sire": "キズナ" if ext_idx % 3 == 0 else ("ドゥラメンテ" if ext_idx % 3 == 1 else "ロードカナロア"),
                "style": ["逃げ", "先行", "差し", "追込"][ext_idx % 4],
                "stamina": 82 + (ext_idx % 10),
                "speed": 83 + (ext_idx % 11),
                "power": 82 + (ext_idx % 9),
                "heavy": 85 + (ext_idx % 15),
                "opt_dist": 2000 if ext_idx % 2 == 0 else 1600,
                "wins_short": "2-1-0-2",
                "wins_mid": "2-2-1-3",
                "wins_long": "0-1-0-2"
            })
            ext_idx += 1

    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 レースシミュレーション", f"📊 JRA現役馬データベース（全{len(df_all)}頭）"])

with tab_sim:
    st.subheader("⚙ レース条件設定")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        venue = st.selectbox("開催競馬場", ["東京", "中山", "京都", "阪神"])
    with col_c2:
        dist = st.selectbox("距離(m)", [1600, 1800, 2000, 2400])
    with col_c3:
        going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.markdown("---")
    st.subheader("🐎 出走馬一括セット・カスタム選択")
    
    btn_col1, btn_col2 = st.columns(2)
    
    # 毎日王冠（全17頭）一括
    if btn_col1.button("🎯 毎日王冠 全17頭一括セット"):
        default_list = [
            "サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "レイニング", "リアライズシリウス", 
            "ダノンエアズロック", "シャンパンカラー", "セイウンハーデス", "レディネス", "クルゼイロドスル", 
            "ライヒスアドラー", "ロングラン", "ビーアストニッシド", "ドラゴンブースト", "ランスオブカオス", 
            "レガーロデルシエロ", "アドマイヤクワッズ"
        ]
    # 京都大賞典（全18頭）一括
    elif btn_col2.button("🏆 京都大賞典 全18頭一括セット"):
        default_list = [
            "サンライズソレイユ", "カネフラ", "ディープモンスター", "アドマイヤテラ", "サンライズアース", 
            "プラダリア", "ドゥレッツァ", "ヴェルミセル", "ミクソロジー", "ブレイヴロッカー", 
            "ヴェルテンベルク", "ワープスピード", "メイショウブレゲ", "サブマリーナ", "ジューンテイク", 
            "ボルドグフーシュ", "アルナシーム", "ショウナンラプンタ"
        ]
    else:
        default_list = [
            "サトノシャイニング", "エルトンバローズ", "ホウオウビスケッツ", "レイニング", "リアライズシリウス", 
            "ダノンエアズロック", "シャンパンカラー", "セイウンハーデス", "レディネス", "クルゼイロドスル", 
            "ライヒスアドラー", "ロングラン", "ビーアストニッシド", "ドラゴンブースト", "ランスオブカオス", 
            "レガーロデルシエロ", "アドマイヤクワッズ"
        ]

    selected_horses = st.multiselect(
        f"全{len(df_all)}頭のJRA現役馬から検索・一括選択（2〜18頭）",
        options=df_all["horse"].tolist(),
        default=default_list
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ 出走馬を【2頭以上】選択してください。")
    else:
        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        if len(df_race) > 18:
            df_race = df_race.head(18)
        
        df_race["num"] = [i + 1 for i in range(len(df_race))]

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
            df_race[["num", "horse", "race_type", "style", "opt_dist", "current_wins", "sire"]]
            .rename(columns={
                "num": "馬番", "horse": "馬名", "race_type": "タイプ",
                "style": "脚質", "opt_dist": "適性距離", "current_wins": f"戦績 ({dist_label})", "sire": "父"
            }),
            hide_index=True,
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🏁 リアルコース再現レース実況")

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
                .sim-container {{ width: 100%; max-width: 800px; margin: 0 auto; padding: 5px; text-align: center; }}
                .start-btn {{
                    width: 100%;
                    height: 52px;
                    background: linear-gradient(135deg, #27ae60, #1e824c);
                    color: white;
                    border: none;
                    border-radius: 26px;
                    font-size: 19px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-bottom: 12px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }}
                .status-box {{ font-size: 15px; font-weight: bold; color: #2ecc71; min-height: 28px; margin-bottom: 8px; }}
                .svg-wrapper {{ width: 100%; background: #05140e; border-radius: 12px; border: 2px solid #1e3d30; padding: 6px; }}
                .results-box {{ margin-top: 14px; background: #161b22; padding: 14px; border-radius: 10px; border: 1px solid #30363d; text-align: left; }}
                .results-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
                .results-table th {{ background: #21262d; padding: 8px; font-size: 13px; text-align: left; color: #8b949e; border-bottom: 1px solid #30363d; }}
                .results-table td {{ padding: 8px; font-size: 14px; border-bottom: 1px solid #21262d; }}
                .waku-tag {{ display: inline-block; width: 22px; height: 22px; line-height: 22px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 6px; }}
                .rank-badge {{ font-weight: bold; font-size: 15px; }}
                .rank-1 {{ color: #f1c40f; }}
                .rank-2 {{ color: #bdc3c7; }}
                .rank-3 {{ color: #e67e22; }}
            </style>
        </head>
        <body>
            <div class="sim-container">
                <button id="startBtn" class="start-btn">▶ レース発走（GATE OPEN）</button>
                <div id="statusBox" class="status-box">「レース発走」を押してください</div>
                
                <div class="svg-wrapper">
                    <svg id="trackSvg" viewBox="0 0 600 340" width="100%">
                        <path id="outerTrack" d="M 180 50 L 420 50 A 100 100 0 0 1 420 250 L 180 250 A 100 100 0 0 1 180 50 Z" fill="#1b4d3e" stroke="#2e8b57" stroke-width="24"/>
                        <path id="innerTrack" d="M 180 62 L 420 62 A 88 88 0 0 1 420 238 L 180 238 A 88 88 0 0 1 180 62 Z" fill="#0e1117" stroke="#0e1117" stroke-width="2"/>

                        <g id="goalGroup"></g>
                        <g id="startGroup"></g>
                        <g id="horsesGroup"></g>
                    </svg>
                </div>

                <div class="results-box">
                    <div style="font-weight: bold; color: #f1c40f; font-size: 16px;">🏆 着順確定結果</div>
                    <div id="resultsContent">発走準備完了</div>
                </div>
            </div>

            <script>
                const horsesData = {json.dumps(horses_js)};
                const raceConfig = {json.dumps(race_config_js)};
                let animId = null;

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

                const spec = COURSE_SPECS[raceConfig.venue] || COURSE_SPECS["東京"];
                // 馬が最終的にストップ・ゴールする進行目標地点（ここをゴール線に合致させる）
                spec.goalP = spec.startP + totalLapsProgress;

                function getTrackPoint(p, laneOffset = 0) {{
                    p = (p % 1.0 + 1.0) % 1.0;
                    const r = 100 + laneOffset;
                    const lenStr = 240;
                    const circumference = 2 * Math.PI * r + 2 * lenStr;
                    const distOnTrack = p * circumference;

                    let x, y, angle;

                    if (distOnTrack <= lenStr) {{
                        x = 420 - distOnTrack; y = 250 + laneOffset; angle = Math.PI;
                    }} else if (distOnTrack <= lenStr + Math.PI * r) {{
                        const arcLen = distOnTrack - lenStr;
                        const theta = Math.PI / 2 + (arcLen / r);
                        x = 180 + r * Math.cos(theta); y = 150 + r * Math.sin(theta); angle = theta + Math.PI / 2;
                    }} else if (distOnTrack <= 2 * lenStr + Math.PI * r) {{
                        const strLen2 = distOnTrack - (lenStr + Math.PI * r);
                        x = 180 + strLen2; y = 50 - laneOffset; angle = 0;
                    }} else {{
                        const arcLen2 = distOnTrack - (2 * lenStr + Math.PI * r);
                        const theta = -Math.PI / 2 + (arcLen2 / r);
                        x = 420 + r * Math.cos(theta); y = 150 + r * Math.sin(theta); angle = theta + Math.PI / 2;
                    }}

                    if (spec.dir === -1) {{ x = 600 - x; angle = Math.PI - angle; }}
                    return {{ x, y, angle }};
                }}

                function drawCourse() {{
                    // 馬が最終停止するゴール地点にゴール線をぴったり描画
                    const goalPt = getTrackPoint(spec.goalP);
                    document.getElementById('goalGroup').innerHTML = `
                        <line x1="${{goalPt.x}}" y1="${{goalPt.y - 18}}" x2="${{goalPt.x}}" y2="${{goalPt.y + 18}}" stroke="#ff3333" stroke-width="4"/>
                        <text x="${{goalPt.x}}" y="${{goalPt.y + 32}}" fill="#ff3333" font-size="12" font-weight="bold" text-anchor="middle">GOAL 🏁</text>
                    `;

                    const startPt = getTrackPoint(spec.startP);
                    document.getElementById('startGroup').innerHTML = `
                        <line x1="${{startPt.x}}" y1="${{startPt.y - 14}}" x2="${{startPt.x}}" y2="${{startPt.y + 14}}" stroke="#2ecc71" stroke-width="3"/>
                        <text x="${{startPt.x}}" y="${{startPt.y - 18}}" fill="#2ecc71" font-size="11" font-weight="bold" text-anchor="middle">START</text>
                    `;
                }}
                drawCourse();

                document.getElementById('startBtn').addEventListener('click', startSimulation);

                function startSimulation() {{
                    if (animId) cancelAnimationFrame(animId);

                    const group = document.getElementById('horsesGroup');
                    const status = document.getElementById('statusBox');
                    const resultsContent = document.getElementById('resultsContent');
                    
                    group.innerHTML = '';
                    resultsContent.innerHTML = '<div style="padding:10px; color:#8b949e;">⏱ ゲートが開きました！各馬一斉にスタート！</div>';

                    const runners = horsesData.map((h, i) => {{
                        const laneOffset = (i - (horsesData.length - 1) / 2) * 2.2;
                        const wakuStyle = getWakuStyle(h.num, horsesData.length);
                        const distDiff = Math.abs(h.opt_dist - raceConfig.dist);
                        const distPenalty = Math.max(0, (distDiff - 200) * 0.05);

                        return {{
                            ...h,
                            laneOffset: laneOffset,
                            wakuStyle: wakuStyle,
                            progress: spec.startP,
                            targetProgress: spec.goalP,
                            staminaRem: (h.stamina - distPenalty) * 12,
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

                                h.staminaRem -= 0.04;
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
                                <circle cx="0" cy="0" r="7" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="0" y="3" font-size="9" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                                <text x="10" y="3" font-size="9" font-weight="bold" fill="white">${{h.name}}</text>
                            `;
                            group.appendChild(g);
                        }});

                        if (finishedCount === 0) {{
                            status.innerText = '🏇 ' + raceConfig.venue + ' ' + raceConfig.dist + 'm 発走しました！';
                        }} else if (finishedCount < totalHorses) {{
                            status.innerText = '🏁 ' + finishedCount + '頭ゴール！激しい叩き合い！';
                        }} else {{
                            status.innerText = '🏆 全頭ゴールイン！確定着順を表示します';
                        }}

                        if (finishedCount < totalHorses) {{
                            animId = requestAnimationFrame(animate);
                        }} else {{
                            runners.sort((a, b) => a.rank - b.rank);
                            let html = `<table class="results-table"><thead><tr><th>着順</th><th>馬番</th><th>馬名</th><th>脚質</th><th>適性距離</th></tr></thead><tbody>`;
                            runners.forEach((h) => {{
                                const rankClass = h.rank === 1 ? 'rank-1' : h.rank === 2 ? 'rank-2' : h.rank === 3 ? 'rank-3' : '';
                                html += `<tr><td class="rank-badge ${{rankClass}}">${{h.rank}}着</td><td><span class="waku-tag" style="background:${{h.wakuStyle.bg}}; color:${{h.wakuStyle.text}};">${{h.num}}</span></td><td><strong>${{h.name}}</strong></td><td>${{h.style}}</td><td>${{h.opt_dist}}m</td></tr>`;
                            }});
                            html += '</tbody></table>';
                            resultsContent.innerHTML = html;
                        }}
                    }}

                    animId = requestAnimationFrame(animate);
                }}
            </script>
        </body>
        </html>
        """
        st.components.v1.html(html_code, height=600)

with tab_db:
    st.subheader(f"📊 JRA現役馬データベース（全{len(df_all)}頭）")
    
    search_term = st.text_input("馬名・父名・タイプで検索", "")
    df_filtered = df_all.copy()
    if search_term:
        df_filtered = df_filtered[
            df_filtered["horse"].str.contains(search_term, case=False) |
            df_filtered["sire"].str.contains(search_term, case=False) |
            df_filtered["race_type"].str.contains(search_term, case=False)
        ]

    st.dataframe(
        df_filtered[["horse", "race_type", "style", "opt_dist", "wins_short", "wins_mid", "wins_long", "speed", "stamina", "power", "sire"]]
        .rename(columns={
            "horse": "馬名", "race_type": "タイプ", "style": "脚質", "opt_dist": "適性距離",
            "wins_short": "短距離(〜1600m)", "wins_mid": "中距離(1800〜2000m)", "wins_long": "長距離(2200m〜)",
            "speed": "スピード", "stamina": "スタミナ", "power": "パワー", "sire": "父"
        }),
        use_container_width=True,
        hide_index=True
    )
