import streamlit as st
import pandas as pd

# --- 定数と製剤データの定義 ---
# 各製剤1mLあたりの含有量
# 単位: g (ブドウ糖, アミノ酸, 窒素), mEq (電解質), mmol (リン)
COMPOSITIONS = {
    "ソルデム3AG": {
        "glucose": 0.075,
        "Na": 0.035,
        "K": 0.020,
        "Cl": 0.035,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "生理食塩水": {
        "glucose": 0,
        "Na": 0.154,
        "K": 0,
        "Cl": 0.154,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "20%糖液": {
        "glucose": 0.200,
        "Na": 0,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "50%糖液": {
        "glucose": 0.500,
        "Na": 0,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "プレアミンP": {
        "glucose": 0,
        "Na": 0.003,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0.076,
        "N": 0.01175,
        "P": 0,
        "Ca": 0,
    },
    "KCl": {
        "glucose": 0,
        "Na": 0,
        "K": 1.0,
        "Cl": 1.0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "10%NaCl": {
        "glucose": 0,
        "Na": 1.711,
        "K": 0,
        "Cl": 1.711,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },  # 10% NaCl
    "リン酸Na": {
        "glucose": 0,
        "Na": 0.75,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0.5,
        "Ca": 0,
    },  # Na 0.75 mEq/mL, P 0.5 mmol/mL
    "カルチコール": {
        "glucose": 0,
        "Na": 0,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0.39,
    },  # 8.5% グルコン酸Ca
    "蒸留水": {
        "glucose": 0,
        "Na": 0,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },
    "ヘパリン": {
        "glucose": 0,
        "Na": 0,
        "K": 0,
        "Cl": 0,
        "amino_acid": 0,
        "N": 0,
        "P": 0,
        "Ca": 0,
    },  # 計算には含めない
}

# --- Streamlit UI の構築 ---
st.set_page_config(layout="wide")
st.title("新生児TPN計算ツール 👶")
st.write("点滴の組成、体重、流速を入力して、1日・体重あたりの投与量を計算します。")

# --- 入力セクション (サイドバー) ---
with st.sidebar:
    st.header("💉 投与内容の入力")

    # 体重と流速
    weight_g = st.number_input(
        "体重 (g)", min_value=100, max_value=10000, value=1000, step=1
    )
    flow_rate = st.number_input(
        "流速 (mL/hr)",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        format="%.1f",
    )

    st.subheader("輸液組成 (合計50mL)")
    # 輸液量の入力
    s3ag_vol = st.number_input(
        "ソルデム3AG (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    saline_vol = st.number_input(
        "生理食塩水 (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    d20_vol = st.number_input(
        "20%糖液 (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    d50_vol = st.number_input(
        "50%糖液 (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    preamin_vol = st.number_input(
        "プレアミンP (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    kcl_vol = st.number_input(
        "KCl (mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.1, format="%.1f"
    )
    nacl_vol = st.number_input(
        "10% NaCl (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    na_p_vol = st.number_input(
        "リン酸Na (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    calticol_vol = st.number_input(
        "カルチコール (mL)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.1f",
    )
    dw_vol = st.number_input(
        "蒸留水 (mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.5, format="%.1f"
    )
    heparin_vol = st.number_input(
        "ヘパリン (mL)",
        min_value=0.0,
        max_value=5.0,
        value=0.05,
        step=0.01,
        format="%.1f",
    )

    # 計算ボタン
    calc_button = st.button("🧮 計算実行")

# --- 計算と結果表示 ---
if calc_button:
    # --- バリデーション (入力チェック) ---
    error_messages = []
    # 1. 体重チェック
    if not (500 <= weight_g <= 5000):
        error_messages.append(f"体重が500g~5000gの範囲外です。(現在: {weight_g}g)")

    # 2. 輸液合計量チェック (ヘパリン除く)
    total_volume_except_heparin = (
        s3ag_vol
        + saline_vol
        + d20_vol
        + d50_vol
        + preamin_vol
        + na_p_vol
        + calticol_vol
    )
    if not (abs(total_volume_except_heparin - 50.0) < 1e-9):  # 浮動小数点数の誤差を考慮
        error_messages.append(
            f"ヘパリン以外の合計輸液量が50mLになっていません。(現在: {total_volume_except_heparin:.1f}mL)"
        )

    # 3. リンとカルシウムの同時投与チェック
    if na_p_vol > 0 and calticol_vol > 0:
        error_messages.append(
            "リン酸Naとカルチコールは同時に投与できません。どちらかを0にしてください。"
        )

    # エラーがあれば表示して終了
    if error_messages:
        for msg in error_messages:
            st.error(f"❌ {msg}")
    else:
        st.success("✅ 入力チェックをクリアしました。計算結果を表示します。")

        # --- 計算ロジック ---
        weight_kg = weight_g / 1000.0
        total_infusion_day = flow_rate * 24  # 1日の総輸液量 (mL/day)

        # 混合液50mL中の各成分の総量を計算
        total_contents = {key: 0.0 for key in COMPOSITIONS["ソルデム3AG"]}
        volumes = {
            "ソルデム3AG": s3ag_vol,
            "生理食塩水": saline_vol,
            "20%糖液": d20_vol,
            "50%糖液": d50_vol,
            "プレアミンP": preamin_vol,
            "リン酸Na": na_p_vol,
            "カルチコール": calticol_vol,
            "10%NaCl": nacl_vol,
            "KCl": kcl_vol,
            "蒸留水": dw_vol,
        }

        for name, vol in volumes.items():
            if vol > 0:
                for key in total_contents:
                    total_contents[key] += COMPOSITIONS[name][key] * vol

        # 1日の投与量 (体重あたり)
        daily_per_kg = {
            key: (value / 50.0) * total_infusion_day / weight_kg
            for key, value in total_contents.items()
        }

        # GIRと糖濃度、NPC/N比の計算
        total_glucose_g = total_contents["glucose"]
        glucose_concentration = (total_glucose_g / 50.0) * 100
        gir = (flow_rate * glucose_concentration * 10) / (weight_kg * 60)  # mg/kg/min

        total_n_g = total_contents["N"]
        npc_kcal = total_glucose_g * 3.4  # 糖のカロリー
        npc_n_ratio = npc_kcal / total_n_g if total_n_g > 0 else 0

        # --- 結果の表示 ---
        st.markdown("---")
        st.header("📊 計算結果")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("基本情報")
            st.metric(label="体重 (kg)", value=f"{weight_kg:.3f}")
            st.metric(
                label="1日あたり総水分量 (mL/kg/day)",
                value=f"{total_infusion_day / weight_kg:.1f}",
            )
            st.metric(label="輸液糖濃度 (%)", value=f"{glucose_concentration:.1f}")
            st.metric(label="GIR (mg/kg/min)", value=f"{gir:.2f}")
            st.metric(
                label="NPC/N比",
                value=f"{npc_n_ratio:.0f}" if npc_n_ratio > 0 else "N/A",
            )

        with col2:
            st.subheader("1日あたり投与量 (/kg/day)")
            # データフレームで結果をきれいに表示
            result_df = pd.DataFrame(
                {
                    "成分": [
                        "ブドウ糖 (g)",
                        "アミノ酸 (g)",
                        "Na (mEq)",
                        "K (mEq)",
                        "Cl (mEq)",
                        "P (mmol)",
                        "Ca (mEq)",
                    ],
                    "投与量": [
                        daily_per_kg["glucose"],
                        daily_per_kg["amino_acid"],
                        daily_per_kg["Na"],
                        daily_per_kg["K"],
                        daily_per_kg["Cl"],
                        daily_per_kg["P"],
                        daily_per_kg["Ca"],
                    ],
                }
            )
            result_df["投与量"] = result_df["投与量"].map("{:.2f}".format)
            st.table(result_df.set_index("成分"))

        st.markdown("---")
        st.subheader("📝 参考: 混合液の濃度 (/Lあたり)")

        # 50mLあたりの総量を20倍して1Lあたりの濃度に換算
        contents_per_liter = {key: value * 20 for key, value in total_contents.items()}

        contents_df = pd.DataFrame(
            {
                "成分": [
                    "ブドウ糖 (g/L)",
                    "アミノ酸 (g/L)",
                    "Na (mEq/L)",
                    "K (mEq/L)",
                    "Cl (mEq/L)",
                    "P (mmol/L)",
                    "Ca (mEq/L)",
                    "窒素 (g/L)",
                ],
                "濃度": [
                    contents_per_liter["glucose"],
                    contents_per_liter["amino_acid"],
                    contents_per_liter["Na"],
                    contents_per_liter["K"],
                    contents_per_liter["Cl"],
                    contents_per_liter["P"],
                    contents_per_liter["Ca"],
                    contents_per_liter["N"],
                ],
            }
        )
        contents_df["濃度"] = contents_df["濃度"].map("{:.1f}".format)
        st.table(contents_df.set_index("成分"))

else:
    st.info("サイドバーで各値を入力し、「計算実行」ボタンを押してください。")
