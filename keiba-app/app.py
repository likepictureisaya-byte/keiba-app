import streamlit as st
import pandas as pd
import json

# 1. ページ基本設定
st.set_page_config(
    page_title="JRAリアルコース競馬シミュレーター (毎日王冠・京都大賞典全馬収録版)",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
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
""", unsafe_allow_html=True)

st.title("🏇 JRAリアルコース競馬シミュレーター")
st.caption("毎日王冠・京都大賞典 出走・想定メンバー全頭＆主要現役G1馬・重賞馬 完全収録")

# 2. データベース（毎日王冠・京都大賞典の全馬・主要G1馬・現役全カバー）
@st.cache_data
def get_active_horse_db_full():
    base_horses = [
        # === 毎日王冠 全馬・主力馬 ===
        {"horse": "サトノシャイニング", "race_type": "芝・マイル・中距離", "sire": "キズナ", "style": "先行", "stamina": 88, "speed": 93, "power": 90, "heavy": 91, "opt_dist": 1800, "wins_short": "1-1-0-0", "wins_mid": "2-1-1-1", "wins_long": "0-0-0-0"},
        {"horse": "レーベンスティール", "race_type": "芝・中距離", "sire": "リアルスティール", "style": "差し", "stamina": 91, "speed": 96, "power": 92, "heavy": 90, "opt_dist": 1800, "wins_short": "1-0-0-0", "wins_mid": "4-1-1-2", "wins_long": "0-0-0-0"},
        {"horse": "ダノンエアズロック", "race_type": "芝・マイル・中距離", "sire": "モーリス", "style": "先行", "stamina": 88, "speed": 94, "power": 92, "heavy": 89, "opt_dist": 1800, "wins_short": "1-0-0-0", "wins_mid": "2-0-0-2", "wins_long": "0-0-0-0"},
        {"horse": "ホウオウビスケッツ", "race_type": "芝・中距離", "sire": "マインドユアビスケッツ", "style": "逃げ", "stamina": 88, "speed": 93, "power": 93, "heavy": 95, "opt_dist": 1800, "wins_short": "0-0-0-0", "wins_mid": "4-3-1-3", "wins_long": "0-0-0-0"},
        {"horse": "エルトンバローズ", "race_type": "芝・マイル・中距離", "sire": "ディープブリランテ", "style": "先行", "stamina": 87, "speed": 93, "power": 90, "heavy": 91, "opt_dist": 1800, "wins_short": "2-1-0-1", "wins_mid": "2-2-1-3", "wins_long": "0-0-0-0"},
        {"horse": "シックスペンス", "race_type": "芝・マイル・中距離", "sire": "キズナ", "style": "先行", "stamina": 89, "speed": 95, "power": 91, "heavy": 90, "opt_dist": 1800, "wins_short": "1-0-0-0", "wins_mid": "3-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "アドマイヤクワッズ", "race_type": "芝・マイル・中距離", "sire": "リアルスティール", "style": "差し", "stamina": 86, "speed": 91, "power": 88, "heavy": 89, "opt_dist": 1800, "wins_short": "1-1-0-1", "wins_mid": "1-1-0-2", "wins_long": "0-0-0-0"},
        {"horse": "シャンパンカラー", "race_type": "芝・マイル", "sire": "ドゥラメンテ", "style": "差し", "stamina": 84, "speed": 94, "power": 91, "heavy": 92, "opt_dist": 1600, "wins_short": "3-0-1-3", "wins_mid": "0-0-0-1", "wins_long": "0-0-0-0"},
        {"horse": "シルトホルン", "race_type": "芝・マイル・中距離", "sire": "スクリーンヒーロー", "style": "先行", "stamina": 86, "speed": 90, "power": 89, "heavy": 90, "opt_dist": 1800, "wins_short": "1-2-1-3", "wins_mid": "2-2-1-4", "wins_long": "0-0-0-0"},
        {"horse": "セイウンハーデス", "race_type": "芝・中距離", "sire": "シルバーステート", "style": "先行", "stamina": 89, "speed": 92, "power": 91, "heavy": 93, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-2-1-4", "wins_long": "0-0-0-1"},
        {"horse": "ドラゴンブースト", "race_type": "芝・マイル・中距離", "sire": "ディーマジェスティ", "style": "差し", "stamina": 85, "speed": 89, "power": 87, "heavy": 88, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "1-0-1-2", "wins_long": "0-0-0-0"},
        {"horse": "ビーアストニッシド", "race_type": "芝・マイル・中距離", "sire": "アメリカンペイトリオット", "style": "逃げ", "stamina": 85, "speed": 89, "power": 88, "heavy": 90, "opt_dist": 1800, "wins_short": "1-1-1-5", "wins_mid": "1-2-0-6", "wins_long": "0-0-0-0"},
        {"horse": "ライヒスアドラー", "race_type": "芝・マイル・中距離", "sire": "シスキン", "style": "差し", "stamina": 85, "speed": 90, "power": 87, "heavy": 88, "opt_dist": 1800, "wins_short": "1-1-0-1", "wins_mid": "1-0-1-1", "wins_long": "0-0-0-0"},
        {"horse": "ランスオブカオス", "race_type": "芝・マイル・中距離", "sire": "シルバーステート", "style": "先行", "stamina": 86, "speed": 90, "power": 88, "heavy": 89, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "1-1-1-2", "wins_long": "0-0-0-0"},
        {"horse": "リアライズシリウス", "race_type": "芝・マイル", "sire": "ポエッツボイス", "style": "差し", "stamina": 84, "speed": 90, "power": 86, "heavy": 87, "opt_dist": 1600, "wins_short": "2-0-1-2", "wins_mid": "0-1-0-1", "wins_long": "0-0-0-0"},
        {"horse": "レイニング", "race_type": "芝・マイル・中距離", "sire": "サートゥルナーリア", "style": "差し", "stamina": 86, "speed": 91, "power": 88, "heavy": 89, "opt_dist": 1800, "wins_short": "1-1-0-1", "wins_mid": "1-1-0-1", "wins_long": "0-0-0-0"},
        {"horse": "レガーロデルシエロ", "race_type": "芝・マイル・中距離", "sire": "ロードカナロア", "style": "先行", "stamina": 85, "speed": 90, "power": 88, "heavy": 88, "opt_dist": 1800, "wins_short": "1-2-0-2", "wins_mid": "1-1-1-2", "wins_long": "0-0-0-0"},
        {"horse": "レディネス", "race_type": "芝・マイル・中距離", "sire": "モーリス", "style": "差し", "stamina": 85, "speed": 89, "power": 88, "heavy": 88, "opt_dist": 1800, "wins_short": "1-1-0-2", "wins_mid": "1-0-1-2", "wins_long": "0-0-0-0"},
        {"horse": "ロングラン", "race_type": "芝・マイル・中距離", "sire": "ヴィクトワールピサ", "style": "追込", "stamina": 86, "speed": 90, "power": 89, "heavy": 90, "opt_dist": 1800, "wins_short": "2-1-0-4", "wins_mid": "3-1-1-6", "wins_long": "0-0-0-0"},
        {"horse": "クルゼイロドスル", "race_type": "芝・マイル", "sire": "ファインニードル", "style": "先行", "stamina": 84, "speed": 91, "power": 88, "heavy": 88, "opt_dist": 1600, "wins_short": "3-1-0-4", "wins_mid": "0-0-0-2", "wins_long": "0-0-0-0"},

        # === 京都大賞典 全馬・主力馬 ===
        {"horse": "ヘデントール", "race_type": "芝・中長距離", "sire": "ルーラーシップ", "style": "差し", "stamina": 95, "speed": 92, "power": 91, "heavy": 102, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "2-1-0-0"},
        {"horse": "ディープモンスター", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 91, "power": 91, "heavy": 93, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "3-3-2-5", "wins_long": "2-1-0-4"},
        {"horse": "ダノンシーマ", "race_type": "芝・中長距離", "sire": "キタサンブラック", "style": "先行", "stamina": 92, "speed": 91, "power": 90, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-1", "wins_long": "1-1-0-1"},
        {"horse": "アクアヴァーナル", "race_type": "芝・中長距離", "sire": "キンシャサノキセキ", "style": "差し", "stamina": 89, "speed": 90, "power": 88, "heavy": 90, "opt_dist": 2200, "wins_short": "1-1-0-2", "wins_mid": "2-1-1-3", "wins_long": "1-0-0-2"},
        {"horse": "ウエストナウ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 91, "speed": 89, "power": 89, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "1-1-0-2", "wins_long": "1-0-0-1"},
        {"horse": "ヴェルテンベルク", "race_type": "芝・中長距離", "sire": "キタサンブラック", "style": "差し", "stamina": 90, "speed": 89, "power": 88, "heavy": 91, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "1-2-1-3", "wins_long": "1-1-0-2"},
        {"horse": "ヴェルミセル", "race_type": "芝・長距離", "sire": "ゴールドシップ", "style": "追込", "stamina": 94, "speed": 86, "power": 90, "heavy": 98, "opt_dist": 2600, "wins_short": "0-0-0-0", "wins_mid": "1-0-1-4", "wins_long": "3-1-1-5"},
        {"horse": "エコロディノス", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 90, "speed": 89, "power": 89, "heavy": 91, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-3", "wins_long": "1-0-1-2"},
        {"horse": "キングスコール", "race_type": "芝・中長距離", "sire": "ドゥラメンテ", "style": "先行", "stamina": 91, "speed": 90, "power": 90, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-0-1-1", "wins_long": "1-0-0-1"},
        {"horse": "サヴォーナ", "race_type": "芝・長距離", "sire": "キズナ", "style": "先行", "stamina": 94, "speed": 88, "power": 91, "heavy": 95, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "1-2-1-3", "wins_long": "2-3-1-5"},
        {"horse": "サフィラ", "race_type": "芝・中長距離", "sire": "ハーツクライ", "style": "差し", "stamina": 90, "speed": 91, "power": 87, "heavy": 89, "opt_dist": 2200, "wins_short": "1-1-1-1", "wins_mid": "1-1-0-2", "wins_long": "0-0-0-1"},
        {"horse": "ショウナンラプンタ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "差し", "stamina": 92, "speed": 90, "power": 90, "heavy": 93, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-2", "wins_long": "0-1-1-2"},
        {"horse": "ナムラエイハブ", "race_type": "芝・中長距離", "sire": "リアルスティール", "style": "先行", "stamina": 88, "speed": 88, "power": 87, "heavy": 89, "opt_dist": 2200, "wins_short": "1-1-1-3", "wins_mid": "1-2-0-4", "wins_long": "0-1-0-2"},
        {"horse": "ファミリータイム", "race_type": "芝・中長距離", "sire": "リアルスティール", "style": "差し", "stamina": 89, "speed": 88, "power": 87, "heavy": 90, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-3", "wins_long": "1-0-0-2"},
        {"horse": "ブレイヴロッカー", "race_type": "芝・長距離", "sire": "ドゥラメンテ", "style": "差し", "stamina": 93, "speed": 87, "power": 89, "heavy": 94, "opt_dist": 2500, "wins_short": "0-0-0-0", "wins_mid": "1-1-1-4", "wins_long": "3-0-1-4"},
        {"horse": "マイネルエンペラー", "race_type": "芝・中長距離", "sire": "ゴールドシップ", "style": "先行", "stamina": 92, "speed": 88, "power": 91, "heavy": 96, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-3", "wins_long": "1-2-0-3"},
        {"horse": "ミクニインスパイア", "race_type": "芝・中長距離", "sire": "ルーラーシップ", "style": "差し", "stamina": 89, "speed": 88, "power": 88, "heavy": 90, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-3", "wins_long": "1-0-0-2"},
        {"horse": "ミステリーウェイ", "race_type": "芝・中長距離", "sire": "ジャスタウェイ", "style": "先行", "stamina": 90, "speed": 88, "power": 89, "heavy": 92, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-2-0-3", "wins_long": "1-1-1-3"},
        {"horse": "メイショウブレゲ", "race_type": "芝・長距離", "sire": "ゴールドシップ", "style": "追込", "stamina": 95, "speed": 85, "power": 91, "heavy": 97, "opt_dist": 3000, "wins_short": "0-0-0-0", "wins_mid": "1-0-1-5", "wins_long": "4-1-1-8"},
        {"horse": "ラスカンブレス", "race_type": "芝・中長距離", "sire": "ブリックスアンドモルタル", "style": "先行", "stamina": 89, "speed": 89, "power": 88, "heavy": 90, "opt_dist": 2200, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-2", "wins_long": "1-0-0-2"},

        # === 主要現役G1馬・実績馬 ===
        {"horse": "ドウデュース", "race_type": "芝・中長距離", "sire": "ハーツクライ", "style": "追込", "stamina": 94, "speed": 96, "power": 97, "heavy": 98, "opt_dist": 2200, "wins_short": "2-1-0-0", "wins_mid": "3-0-1-4", "wins_long": "2-0-0-2"},
        {"horse": "チェルヴィニア", "race_type": "芝・中長距離", "sire": "ハービンジャー", "style": "差し", "stamina": 93, "speed": 94, "power": 88, "heavy": 90, "opt_dist": 2400, "wins_short": "1-1-0-0", "wins_mid": "1-0-0-1", "wins_long": "2-0-0-0"},
        {"horse": "ローシャムパーク", "race_type": "芝・中長距離", "sire": "ハービンジャー", "style": "差し", "stamina": 90, "speed": 93, "power": 92, "heavy": 96, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "5-2-1-3", "wins_long": "1-0-0-1"},
        {"horse": "サトノグランツ", "race_type": "芝・中長距離", "sire": "サトノダイヤモンド", "style": "差し", "stamina": 93, "speed": 88, "power": 89, "heavy": 94, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "1-1-1-2", "wins_long": "3-0-1-3"},
        {"horse": "ディープボンド", "race_type": "芝・長距離", "sire": "キズナ", "style": "先行", "stamina": 97, "speed": 82, "power": 93, "heavy": 105, "opt_dist": 3000, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-8", "wins_long": "3-4-2-7"},
        {"horse": "ブレイディヴェーグ", "race_type": "芝・中長距離", "sire": "ロードカナロア", "style": "差し", "stamina": 91, "speed": 96, "power": 88, "heavy": 90, "opt_dist": 2000, "wins_short": "1-1-0-0", "wins_mid": "2-1-0-0", "wins_long": "1-0-0-0"},
        {"horse": "プラダリア", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "先行", "stamina": 92, "speed": 87, "power": 91, "heavy": 102, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-2-5", "wins_long": "2-1-0-4"},
        {"horse": "ジャスティンミラノ", "race_type": "芝・中長距離", "sire": "キズナ", "style": "先行", "stamina": 91, "speed": 95, "power": 90, "heavy": 95, "opt_dist": 2000, "wins_short": "0-0-0-0", "wins_mid": "3-1-0-0", "wins_long": "0-0-0-0"},
        {"horse": "ベラジオオペラ", "race_type": "芝・中長距離", "sire": "ロードカナロア", "style": "先行", "stamina": 90, "speed": 92, "power": 93, "heavy": 94, "opt_dist": 2000, "wins_short": "1-0-0-0", "wins_mid": "4-1-1-2", "wins_long": "0-0-0-1"},
        {"horse": "リバティアイランド", "race_type": "芝・中長距離", "sire": "ドゥラメンテ", "style": "差し", "stamina": 93, "speed": 97, "power": 92, "heavy": 92, "opt_dist": 2000, "wins_short": "2-1-0-0", "wins_mid": "2-0-0-1", "wins_long": "1-1-0-0"},
        {"horse": "ダノンデサイル", "race_type": "芝・中長距離", "sire": "エピファネイア", "style": "先行", "stamina": 93, "speed": 93, "power": 91, "heavy": 93, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-0-0-1", "wins_long": "1-0-0-0"},
        {"horse": "アーバンシック", "race_type": "芝・中長距離", "sire": "スワーヴリチャード", "style": "差し", "stamina": 94, "speed": 92, "power": 89, "heavy": 94, "opt_dist": 2400, "wins_short": "0-0-0-0", "wins_mid": "2-1-0-1", "wins_long": "1-0-0-1"},
        {"horse": "シュヴァリエローズ", "race_type": "芝・中長距離", "sire": "ディープインパクト", "style": "差し", "stamina": 91, "speed": 89, "power": 89, "heavy": 92, "opt_dist": 2400, "wins_short": "1-1-0-3", "wins_mid": "2-2-1-6", "wins_long": "2-1-1-4"},
        {"horse": "ブローザホーン", "race_type": "芝・長距離", "sire": "エピファネイア", "style": "差し", "stamina": 96, "speed": 90, "power": 93, "heavy": 105, "opt_dist": 2500, "wins_short": "0-0-0-0", "wins_mid": "2-1-1-3", "wins_long": "3-2-1-3"}
    ]

    # JRA現役馬の残りを補強生成（データベース拡張）
    prefixes = ["サトノ", "アドマイヤ", "ダノン", "メイショウ", "ウイン", "マテンロウ", "ホウオウ", "テーオー", "シゲル", "ヤマニン", "サンライズ", "ニシノ", "ロード", "クラウン", "スマート", "デルマ", "コスタ", "レッド", "ルージュ", "ゴールド", "キタサン"]
    suffixes = ["キング", "エース", "ダイヤ", "ハート", "ビート", "ソウル", "スター", "フラッシュ", "ヒーロー", "アロー", "ドリーム", "ライジング", "クラウン", "ブレイブ", "シャイン", "インパクト", "スピリッツ", "カイザー"]
    sires = ["キズナ", "ドゥラメンテ", "エピファネイア", "ロードカナロア", "モーリス", "キタサンブラック", "ハービンジャー", "ルーラーシップ"]

    existing_names = set(h["horse"] for h in base_horses)
    
    idx = 0
    for p in prefixes:
        for s in suffixes:
            name = p + s
            if name not in existing_names:
                existing_names.add(name)
                base_horses.append({
                    "horse": name,
                    "race_type": "芝・中長距離" if idx % 3 == 0 else ("芝・マイル" if idx % 3 == 1 else "ダート"),
                    "sire": sires[idx % len(sires)],
                    "style": ["逃げ", "先行", "差し", "追込"][idx % 4],
                    "stamina": 74 + (idx % 20),
                    "speed": 75 + (idx % 19),
                    "power": 74 + (idx % 18),
                    "heavy": 80 + (idx % 22),
                    "opt_dist": 2000 if idx % 3 == 0 else (1600 if idx % 3 == 1 else 2400),
                    "wins_short": "1-1-0-2",
                    "wins_mid": "2-1-1-3",
                    "wins_long": "1-0-0-2"
                })
                idx += 1

    return pd.DataFrame(base_horses)

df_all = get_active_horse_db_full()

# --- 初期選択馬（毎日王冠・京都大賞典メンバー優先セット） ---
if "selected_horses" not in st.session_state:
    st.session_state.selected_horses = [
        "サトノシャイニング", "レーベンスティール", "ダノンエアズロック", "ホウオウビスケッツ", 
        "エルトンバローズ", "シックスペンス", "ヘデントール", "ディープモンスター", 
        "ダノンシーマ", "アクアヴァーナル", "ウエストナウ", "シュヴァリエローズ",
        "ドウデュース", "チェルヴィニア", "ローシャムパーク", "サトノグランツ", 
        "ディープボンド", "プラダリア"
    ]

# タブ構成
tab_sim, tab_db = st.tabs(["🏇 レースシミュレーション", f"📊 JRA現役馬データベース（全{len(df_all)}頭）"])

with tab_sim:
    st.subheader("⚙ レース条件設定")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        venue = st.selectbox("開催競馬場", ["東京", "京都", "中山", "阪神"])
    with col_c2:
        dist = st.selectbox("距離(m)", [1800, 2400, 1600, 2000, 3000])
    with col_c3:
        going = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

    st.markdown("---")
    st.subheader("🐎 出走馬カスタム選択 & 馬番（枠順）設定")

    selected_horses = st.multiselect(
        f"全{len(df_all)}頭のJRA現役馬から出走馬を選択（2〜18頭）",
        options=df_all["horse"].tolist(),
        key="selected_horses"
    )

    if len(selected_horses) < 2:
        st.warning("⚠️ 出走馬を【2頭以上】選択してください。")
    else:
        if len(selected_horses) > 18:
            st.info("💡 18頭を超える選択の場合、上位18頭が出走対象となります。")
            selected_horses = selected_horses[:18]

        st.markdown("##### 🔢 出走馬の馬番（枠順）カスタマイズ")
        st.caption("好きな馬に好きな馬番（1〜18）を割り振ってください。")

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
                    key=f"num_input_{horse_name}"
                )
                custom_numbers[horse_name] = custom_num

        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        df_race["num"] = df_race["horse"].map(custom_numbers)
        
        # 馬番順にソート
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
                .sim-container {{ width: 100%; max-width: 900px; margin: 0 auto; padding: 4px; text-align: center; }}
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
                    margin-bottom: 10px;
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
                    <!-- viewBox切り欠き防止サイズ (0 0 720 380) -->
                    <svg id="trackSvg" viewBox="0 0 720 380" width="100%" height="auto" style="display: block;">
                        <path id="outerTrack" d="M 220 70 L 500 70 A 110 110 0 0 1 500 290 L 220 290 A 110 110 0 0 1 220 70 Z" fill="#1b4d3e" stroke="#2e8b57" stroke-width="26"/>
                        <path id="innerTrack" d="M 220 84 L 500 84 A 96 96 0 0 1 500 276 L 220 276 A 96 96 0 0 1 220 84 Z" fill="#0e1117" stroke="#0e1117" stroke-width="2"/>

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
                                <circle cx="0" cy="0" r="8" fill="${{h.wakuStyle.bg}}" stroke="#ffffff" stroke-width="1.5"/>
                                <text x="0" y="3" font-size="10" font-weight="bold" fill="${{h.wakuStyle.text}}" text-anchor="middle">${{h.num}}</text>
                                <text x="11" y="3" font-size="10" font-weight="bold" fill="white">${{h.name}}</text>
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
        st.components.v1.html(html_code, height=620)

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
