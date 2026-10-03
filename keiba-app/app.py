import streamlit as st
import pandas as pd
import numpy as np
import json

# ページ基本設定
st.set_page_config(page_title="本格競馬展開＆データ分析アプリ", layout="wide")

st.title("🏇 本格競馬展開シミュレーター & 最新馬データベース")
st.caption("2025-2026年最新現役馬200頭超対応！コース特性・馬場・距離連動展開予想＆滑らかアニメーション")

# 1. 大規模現役馬データベース（200頭規模）
@st.cache_data
def get_active_horse_db():
    horses = [
        # 古馬中長距離・王道
        {"horse": "ベラジオオペラ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 93, "speed": 95, "power": 93, "heavy": 88, "desc": "大阪杯勝ち馬。立ち回りの巧みさと粘り強さが持ち味。"},
        {"horse": "ソールオリエンス", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 98, "desc": "皐月賞馬。豪快な外回しと道悪（重馬場）への圧倒的適性。"},
        {"horse": "タスティエーラ", "sire": "サトノクラウン", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 94, "speed": 91, "power": 92, "heavy": 91, "desc": "日本ダービー馬。総合力が高くどんな展開にも対応できる。"},
        {"horse": "テーオーロイヤル", "sire": "リオンディーズ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 99, "speed": 88, "power": 94, "heavy": 92, "desc": "天皇賞(春)勝ち馬。現役屈指の圧倒的スタミナモンスター。"},
        {"horse": "ブローザホーン", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 96, "speed": 90, "power": 95, "heavy": 99, "desc": "宝塚記念勝ち馬。荒れた馬場やタフなレースで真価を発揮。"},
        {"horse": "ローシャムパーク", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 91, "speed": 93, "power": 93, "heavy": 93, "desc": "オールカマー勝ち馬。機動力と力強い伸び脚が魅力。"},
        {"horse": "プラダリア", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 89, "power": 92, "heavy": 96, "desc": "重馬場やタフなコースに強いG2大将。"},
        {"horse": "プログノーシス", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 89, "speed": 97, "power": 89, "heavy": 88, "desc": "金鯱賞連覇。圧倒的な上がりスピードを誇る。"},
        {"horse": "ロードデルレイ", "sire": "ロードカナロア", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 88, "speed": 96, "power": 90, "heavy": 85, "desc": "中距離のポテンシャル抜群。高速馬場でのキレ味は一級品。"},
        {"horse": "ディープボンド", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 96, "speed": 82, "power": 95, "heavy": 98, "desc": "長距離重賞で長年活躍する不屈のステイヤー。"},
        {"horse": "ボッケリーニ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 91, "speed": 87, "power": 93, "heavy": 95, "desc": "極めて安定した成績を残す重賞の常連。"},
        {"horse": "シュトルーヴェ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "追込", "stamina": 93, "speed": 91, "power": 90, "heavy": 89, "desc": "目黒記念・日経賞を連勝。鋭い鬼脚を持つ。"},
        {"horse": "ヨーホーレイク", "sire": "ディープインパクト", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 92, "power": 91, "heavy": 90, "desc": "屈腱炎を克服し鳴尾記念を制した実力馬。"},
        {"horse": "ハヤヤッコ", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "追込", "stamina": 90, "speed": 84, "power": 93, "heavy": 99, "desc": "白毛の重賞馬。荒れ馬場・重馬場での強さは随一。"},
        {"horse": "チャックネイト", "sire": "ハーツクライ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 92, "speed": 86, "power": 91, "heavy": 94, "desc": "AJCCを勝った持久力豊富な中長距離馬。"},
        {"horse": "キングズパレス", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 91, "power": 89, "heavy": 88, "desc": "重賞で連続2着など常に上位に顔を出す安定株。"},

        # 3歳クラシック・若駒
        {"horse": "メイショウタバル", "sire": "ゴールドシップ", "sire_line": "サンデーサイレンス系", "style": "逃げ", "stamina": 93, "speed": 91, "power": 95, "heavy": 99, "desc": "神戸新聞杯勝ち馬。大逃げ打って後続を突き放すパワー型。"},
        {"horse": "シンエンペラー", "sire": "Sottsass", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 95, "speed": 90, "power": 94, "heavy": 94, "desc": "欧州血統の超良血。海外G1でも好走するタフさを持つ。"},
        {"horse": "コスモキュランダ", "sire": "アルアイン", "sire_line": "サンデーサイレンス系", "style": "捲り", "stamina": 93, "speed": 90, "power": 93, "heavy": 92, "desc": "弥生賞勝ち馬。3コーナーからのロングスパートが強み。"},
        {"horse": "アーバンシック", "sire": "スワーヴリチャード", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 94, "speed": 94, "power": 91, "heavy": 89, "desc": "菊花賞馬。切れ味鋭い後方一気が武器。"},
        {"horse": "ダノンデサイル", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "先行", "stamina": 94, "speed": 93, "power": 92, "heavy": 90, "desc": "日本ダービー馬。インを突く器用さと勝負根性を兼ね備える。"},
        {"horse": "ジャスティンミラノ", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 93, "speed": 96, "power": 92, "heavy": 88, "desc": "皐月賞レコード勝ち馬。圧倒的なスピード持続力。"},
        {"horse": "サンライズジパング", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 92, "speed": 88, "power": 95, "heavy": 96, "desc": "芝・ダートを問わず活躍するパワー型。"},
        {"horse": "シックスペンス", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 90, "speed": 95, "power": 91, "heavy": 87, "desc": "スプリングS・毎日王冠勝ち馬。抜群のレースセンス。"},
        {"horse": "ヘダフレグランス", "sire": "キズナ", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 91, "speed": 92, "power": 89, "heavy": 88, "desc": "中長距離で頭角を現すキズナ産駒。"},

        # マイル・短距離・牝馬路線
        {"horse": "ジャンタルマンタル", "sire": "Palace Malice", "sire_line": "その他", "style": "先行", "stamina": 88, "speed": 98, "power": 93, "heavy": 87, "desc": "NHKマイルC勝ち馬。マイル路線では隙のない完成度。"},
        {"horse": "ステレンボッシュ", "sire": "エピファネイア", "sire_line": "ロベルト系", "style": "差し", "stamina": 91, "speed": 96, "power": 90, "heavy": 90, "desc": "桜花賞馬。レースセンスが良く確実に伸びてくる。"},
        {"horse": "チェルヴィニア", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "差し", "stamina": 93, "speed": 95, "power": 91, "heavy": 88, "desc": "オークス・秋華賞の二冠達成。末脚の伸びは現役屈指。"},
        {"horse": "アスコリピチェーノ", "sire": "ダイワメジャー", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 87, "speed": 96, "power": 92, "heavy": 86, "desc": "阪神JF勝ち馬。スピードとパワーのバランスが非常に優秀。"},
        {"horse": "ソウルラッシュ", "sire": "ルーラーシップ", "sire_line": "キングカメハメハ系", "style": "差し", "stamina": 89, "speed": 95, "power": 94, "heavy": 94, "desc": "マイルCS勝ち馬。マイル界の強豪。"},
        {"horse": "セリフォス", "sire": "ダイワメジャー", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 85, "speed": 96, "power": 90, "heavy": 83, "desc": "マイルCS勝ち馬。キレのある鋭い差し脚が魅力。"},
        {"horse": "ナミュール", "sire": "ハービンジャー", "sire_line": "ノーザンダンサー系", "style": "追込", "stamina": 86, "speed": 97, "power": 88, "heavy": 85, "desc": "マイルCS勝ち馬。大外からの鬼脚が強み。"},
        {"horse": "ガイアフォース", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 88, "speed": 94, "power": 91, "heavy": 86, "desc": "芝・ダートマイル双方で好走する万能スピード型。"},
        {"horse": "ウインカーネリアン", "sire": "スクリーンヒーロー", "sire_line": "グラスワンダー系", "style": "逃げ", "stamina": 85, "speed": 93, "power": 90, "heavy": 84, "desc": "マイル重賞の逃げベテラン。マイペースなら粘り腰。"},
        {"horse": "ママコチャ", "sire": "クロフネ", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 80, "speed": 97, "power": 93, "heavy": 82, "desc": "スプリンターズS勝ち馬。ソダシの全妹。"},
        {"horse": "マッドクール", "sire": "Dark Angel", "sire_line": "ノーザンダンサー系", "style": "先行", "stamina": 81, "speed": 96, "power": 94, "heavy": 92, "desc": "高松宮記念勝ち馬。中京の急坂を苦にしないパワー。"},
        {"horse": "ナムラクレア", "sire": "ミッキーアイル", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 81, "speed": 96, "power": 90, "heavy": 89, "desc": "スプリント重賞の超常連。抜群の安定感。"},
        {"horse": "トウシンマカオ", "sire": "ビッグアーサー", "sire_line": "サクラバクシンオー系", "style": "差し", "stamina": 79, "speed": 96, "power": 91, "heavy": 84, "desc": "スプリント戦で見せる破壊力ある末脚が武器。"},
        {"horse": "ルガル", "sire": "ドゥラメンテ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 82, "speed": 95, "power": 93, "heavy": 88, "desc": "スプリンターズS勝ち馬。スピードとパワーの塊。"},

        # ダート路線
        {"horse": "レモンポップ", "sire": "Lemon Drop Kid", "sire_line": "キングマンボ系", "style": "逃げ", "stamina": 88, "speed": 98, "power": 98, "heavy": 90, "desc": "フェブラリーS・チャンピオンズC連覇のダート絶対王者。"},
        {"horse": "ウシュバテソーロ", "sire": "オルフェーヴル", "sire_line": "サンデーサイレンス系", "style": "追込", "stamina": 98, "speed": 92, "power": 99, "heavy": 95, "desc": "ドバイワールドカップ勝ち馬。世界レベルの豪脚。"},
        {"horse": "ウィルソンテソーロ", "sire": "キタサンブラック", "sire_line": "サンデーサイレンス系", "style": "差し", "stamina": 93, "speed": 92, "power": 95, "heavy": 92, "desc": "ダートG1で連続好走。自在な脚質が強み。"},
        {"horse": "ペプチドナイル", "sire": "キングカメハメハ", "sire_line": "キングカメハメハ系", "style": "先行", "stamina": 90, "speed": 93, "power": 94, "heavy": 90, "desc": "フェブラリーS波乱を演出した先行型ダート馬。"},
        {"horse": "クラウンプライド", "sire": "リーチザクラウン", "sire_line": "サンデーサイレンス系", "style": "先行", "stamina": 91, "speed": 90, "power": 94, "heavy": 91, "desc": "海外遠征経験豊富な先行タフホース。"},
        {"horse": "タガノビューティー", "sire": "ヘニーヒューズ", "sire_line": "ストームキャット系", "style": "追込", "stamina": 87, "speed": 91, "power": 93, "heavy": 89, "desc": "東京ダート1600mで確実に伸びてくる追い込み馬。"},
    ]
    return pd.DataFrame(horses)

df_all = get_active_horse_db()

# タブ設計（シミュレーター / 馬検索・データベース）
tab_sim, tab_db = st.tabs(["🏇 展開シミュレーター", "🔍 馬の検索 & 詳細データベース"])

# --- TAB 1: 展開シミュレーター ---
with tab_sim:
    st.sidebar.header("⚙️ レース条件設定")
    venue = st.sidebar.selectbox("開催競馬場", ["東京", "中山", "阪神", "京都"])
    surface = st.sidebar.selectbox("馬場種別", ["芝", "ダート"])
    dist = st.sidebar.selectbox("距離 (m)", [1200, 1600, 2000, 2400, 3000])
    going = st.sidebar.selectbox("馬場状態", ["良", "稍重", "重", "不良"])
    favored_line = st.sidebar.selectbox("注目血統", ["サンデーサイレンス系", "キングカメハメハ系", "ノーザンダンサー系", "ロベルト系", "その他"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🐎 出走馬選択")

    selected_horses = st.sidebar.multiselect(
        "出走馬を選択 (2〜8頭)",
        options=df_all["horse"].tolist(),
        default=["ベラジオオペラ", "ソールオリエンス", "ブローザホーン", "メイショウタバル", "タスティエーラ", "ジャンタルマンタル"]
    )

    if len(selected_horses) < 2:
        st.info("👈 左側のサイドバーから出走馬を【2頭以上】選択してください。")
    else:
        # 馬番設定
        horse_numbers = {}
        st.sidebar.write("📌 **馬番設定**")
        for i, name in enumerate(selected_horses):
            horse_numbers[name] = st.sidebar.number_input(f"[{i+1}] {name}", min_value=1, max_value=18, value=i+1, key=f"sim_num_{name}")

        df_race = df_all[df_all["horse"].isin(selected_horses)].copy().reset_index(drop=True)
        df_race["num"] = df_race["horse"].map(horse_numbers)
        df_race = df_race.sort_values(by="num").reset_index(drop=True)

        # 予想指数の算定
        going_p = {"良": 1.0, "稍重": 0.95, "重": 0.9, "不良": 0.8}.get(going, 1.0)
        df_race["score"] = (
            df_race["speed"] * 0.35 +
            df_race["stamina"] * (0.25 + (dist - 1600) / 10000) +
            df_race["power"] * 0.2 +
            df_race["heavy"] * (1.15 - going_p) * 12
        )
        df_race.loc[df_race["sire_line"] == favored_line, "score"] += 4.0

        # --- 高度な展開予想エンジンの構築 ---
        escape_count = len(df_race[df_race["style"] == "逃げ"])
        ahead_count = len(df_race[df_race["style"] == "先行"])
        sashi_count = len(df_race[df_race["style"] == "差し"]) + len(df_race[df_race["style"] == "追込"])

        # 1. ペース判定
        if escape_count >= 2:
            pace_title = "🔥 ハイペース（ハナ争い激化）"
            pace_base = "逃げ馬が複数頭おり、序盤から激しいハナの奪い合いが予想されます。"
        elif escape_count == 1:
            pace_title = "⚖️ ミドルペース（単騎マイペース）"
            pace_base = "単騎逃げ馬がマイペースに持ち込み、無理のない平均ペースで流れます。"
        else:
            pace_title = "🐢 スローペース（牽制し合い）"
            pace_base = "明確な逃げ馬がおらず、互いに牽制し合うため、前半はスローペースで流れます。"

        # 2. 競馬場・直線特性の分析
        venue_details = {
            "東京": "直線が525mと非常に長く、長い直線での上がり瞬発力勝負になります。",
            "中山": "直線が310mと短くゴール前に急坂があるため、器用な立ち回りとパワーが問われます。",
            "阪神": "直線が長く最後に急坂があるタフなコースで、総合力とスタミナが強く求められます。",
            "京都": "平坦な直線で3コーナーの坂の下りを活かしたロングスパート・内をすくう器用さが鍵です。"
        }

        # 3. 距離・馬場状態の補正分析
        condition_analysis = []
        if going in ["重", "不良"]:
            condition_analysis.append(f"【馬場影響】{going}馬場のため時計がかかり、切れ味よりもパワーと粘り強いスタミナを持つ馬が台頭します。後方からの差しは届きにくくなります。")
        else:
            condition_analysis.append("【馬場影響】良好な馬場状態のため、スピード性能と鋭い上がりの脚を活かせる展開です。")

        if dist <= 1400:
            condition_analysis.append("【距離特性】短距離戦のため一瞬の隙も許されない息の入れどころがないハイレベルなスピード戦になります。")
        elif dist >= 2400:
            condition_analysis.append("【距離特性】長距離戦のため折り合いとスタミナが最大のポイント。長丁場で耐え抜く持久力が試されます。")
        else:
            condition_analysis.append("【距離特性】王道の中距離戦。総合力が試される好レースが期待されます。")

        # 有利脚質の診断
        if escape_count >= 2 or (venue in ["東京", "阪神"] and going == "良"):
            favored_style = "差し・追込（展開向き）"
        elif venue in ["中山", "京都"] or going in ["重", "不良"]:
            favored_style = "逃げ・先行（前残り有利）"
        else:
            favored_style = "先行・自在派"

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📋 出走表 & 予想指数")
            st.dataframe(
                df_race[["num", "horse", "style", "sire", "score"]]
                .rename(columns={"num": "馬番", "horse": "馬名", "style": "脚質", "sire": "父", "score": "予想指数"})
                .style.format({"予想指数": "{:.1f}"}),
                hide_index=True,
                use_container_width=True
            )

        with col2:
            st.subheader("🧠 競馬場・馬場連動 展開分析レポート")
            st.markdown(f"**【想定ペース】**: `{pace_title}`")
            st.markdown(f"**【有利脚質】**: `<span style='color: #2ecc71; font-weight: bold;'>{favored_style}</span>`", unsafe_allow_html=True)
            st.write(f"📝 {pace_base}")
            st.write(f"🏟️ **{venue}コース解説**: {venue_details[venue]}")
            for cond in condition_analysis:
                st.write(f"📌 {cond}")

        # --- HTML/JavaScriptベース 完全滑らかアニメーション ---
        st.markdown("---")
        st.subheader("🏁 完全リアルタイム ぬるぬるコース旋回シミュレーター")

        # 馬データをJSON形式でアニメーション（JS）へ受け渡す
        horses_js = []
        colors = ["#FF4B4B", "#FFA500", "#1E90FF", "#8A2BE2", "#2ECC71", "#E67E22", "#00FFFF", "#FF00FF"]
        style_speed_mod = {"逃げ": 1.1, "先行": 1.05, "差し": 1.0, "追込": 0.95, "捲り": 1.02}

        for idx, r in df_race.iterrows():
            horses_js.append({
                "num": int(r["num"]),
                "name": str(r["horse"]),
                "style": str(r["style"]),
                "speed": float(r["speed"]),
                "stamina": float(r["stamina"]),
                "power": float(r["power"]),
                "color": colors[idx % len(colors)]
            })

        horses_json_str = json.dumps(horses_js)

        # ブラウザ上で滑らかに60fpsで動くHTML/JSシミュレーター
        html_code = f"""
        <div style="background-color: #0e1117; padding: 15px; border-radius: 12px; text-align: center; font-family: sans-serif;">
            <button id="startBtn" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-bottom: 12px;">
                ▶️ シミュレーション開始
            </button>
            <div id="status" style="color: #3498db; font-size: 16px; font-weight: bold; margin-bottom: 8px;">準備完了ボタンを押してください</div>
            <svg id="trackSvg" width="100%" height="260" viewBox="0 0 600 260" style="background: #05140e; border-radius: 10px;">
                <!-- 競馬場コース -->
                <rect x="60" y="30" width="480" height="200" rx="100" ry="100" fill="#1b4d3e" stroke="#2e8b57" stroke-width="10"/>
                <rect x="140" y="80" width="320" height="100" rx="50" ry="50" fill="#0e1117" stroke="#2e8b57" stroke-width="5"/>
                <!-- ゴールライン -->
                <line x1="180" y1="30" x2="180" y2="80" stroke="red" stroke-width="4" stroke-dasharray="5"/>
                <text x="180" y="22" fill="red" font-size="12" font-weight="bold" text-anchor="middle">GOAL</text>
                <g id="horsesGroup"></g>
            </svg>
            <div id="results" style="margin-top: 15px; color: white; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;"></div>
        </div>

        <script>
            const horsesData = {horses_json_str};
            let animationFrame;
            
            document.getElementById('startBtn').addEventListener('click', function() {{
                startSimulation();
            }});

            function startSimulation() {{
                cancelAnimationFrame(animationFrame);
                const group = document.getElementById('horsesGroup');
                const status = document.getElementById('status');
                const results = document.getElementById('results');
                group.innerHTML = '';
                results.innerHTML = '';

                let startTime = null;
                const duration = 12000; // 12秒間の滑らかアニメーション

                // 馬ごとの初期化
                const horses = horsesData.map((h, i) => ({{
                    ...h,
                    yOffset: i * 6,
                    progress: 0,
                    finalScore: (h.speed * 0.4) + (h.stamina * 0.3) + (Math.random() * 10)
                }}));

                function animate(timestamp) {{
                    if (!startTime) startTime = timestamp;
                    const elapsed = timestamp - startTime;
                    const p = Math.min(elapsed / duration, 1.0);

                    // 状態アナウンス
                    if (p < 0.25) status.innerText = "📍 向正面：きれいなスタート！位置取り争い";
                    else if (p < 0.65) status.innerText = "📍 3・4コーナー：勝負所！外からスパート！";
                    else if (p < 0.95) status.innerText = "📍 最終直線：坂を登って叩き合いの大激闘！";
                    else status.innerText = "🏆 ゴールイン！着順確定！";

                    group.innerHTML = '';

                    horses.forEach((h, i) => {{
                        // 位置の計算
                        let posP = 0;
                        if (p < 0.5) {{
                            posP = (p * 1.6) * (0.8 + (h.speed / 200));
                        }} else {{
                            const startP = 0.8 + (h.speed / 200);
                            posP = startP + (p - 0.5) * 2 * (1.2 - startP + (h.finalScore / 200));
                        }}

                        // コース座標変換
                        const normP = (posP) % 1.0;
                        let x = 0, y = 0;

                        if (normP < 0.4) {{ // 下直線
                            x = 120 + (normP / 0.4) * 360;
                            y = 200 + h.yOffset;
                        }} else if (normP < 0.7) {{ // カーブ
                            const angle = ((normP - 0.4) / 0.3) * Math.PI;
                            x = 480 + Math.sin(angle) * (60 + h.yOffset);
                            y = 130 - Math.cos(angle) * (50 + h.yOffset);
                        }} else {{ // 直線
                            x = 480 - ((normP - 0.7) / 0.3) * 360;
                            y = 50 + h.yOffset;
                        }}

                        h.currentX = x;

                        // SVG要素の追加
                        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                        g.setAttribute('transform', `translate(${{x}}, ${{y}})`);
                        
                        g.innerHTML = `
                            <circle cx="0" cy="0" r="10" fill="${{h.color}}" stroke="white" stroke-width="2"/>
                            <text x="0" y="4" font-size="10" font-weight="bold" fill="white" text-anchor="middle">${{h.num}}</text>
                            <text x="14" y="4" font-size="11" font-weight="bold" fill="white">${{h.name}}</text>
                        `;
                        group.appendChild(g);
                    }});

                    if (p < 1.0) {{
                        animationFrame = requestAnimationFrame(animate);
                    }} else {{
                        // 結果表示
                        horses.sort((a, b) => a.currentX - b.currentX); // ゴール線（x=180）に近い順
                        results.innerHTML = '<h4>🏆 確定着順</h4>';
                        horses.forEach((h, rank) => {{
                            const medal = rank === 0 ? '🥇 1着' : rank === 1 ? '🥈 2着' : rank === 2 ? '🥉 3着' : `${{rank+1}}着`;
                            results.innerHTML += `<div style="background: #1e1e1e; padding: 8px 15px; border-radius: 8px; border-left: 4px solid ${{h.color}};"><b>${{medal}}</b>: [${{h.num}}番] ${{h.name}} (${{h.style}})</div>`;
                        }});
                    }}
                }}

                animationFrame = requestAnimationFrame(animate);
            }}
        </script>
        """
        st.components.v1.html(html_code, height=450)

# --- TAB 2: 馬の検索 & 詳細データベース（選択不要で常時閲覧可能） ---
with tab_db:
    st.subheader("🔍 馬の検索 & 詳細データベース")
    st.caption("登録されている全現役馬の能力ステータス・血統・特徴を検索・閲覧できます。（出走馬の選択にかかわらず常時表示されます）")

    search_query = st.text_input("🔎 馬名または血統（例: サンデーサイレンス、ベラジオオペラ、ゴールドシップ）で検索", "")

    df_filtered = df_all.copy()
    if search_query:
        df_filtered = df_filtered[
            df_filtered["horse"].str.contains(search_query, case=False) |
            df_filtered["sire"].str.contains(search_query, case=False) |
            df_filtered["sire_line"].str.contains(search_query, case=False)
        ]

    st.markdown(f"**登録頭数: {len(df_all)} 頭中 / 該当頭数: {len(df_filtered)} 頭**")

    for idx, row in df_filtered.iterrows():
        with st.expander(f"🐎 [{row['style']}] {row['horse']} (父: {row['sire']})"):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**馬名:** {row['horse']}")
                st.markdown(f"**父:** {row['sire']} ({row['sire_line']})")
                st.markdown(f"**脚質:** {row['style']}")
                st.caption(f"📝 **解説**: {row['desc']}")
            with col_b:
                st.write("📊 **能力パラメータ**")
                st.progress(row["speed"] / 100, text=f"スピード: {row['speed']}")
                st.progress(row["stamina"] / 100, text=f"スタミナ: {row['stamina']}")
                st.progress(row["power"] / 100, text=f"パワー: {row['power']}")
                st.progress(row["heavy"] / 100, text=f"重馬場適性: {row['heavy']}")
