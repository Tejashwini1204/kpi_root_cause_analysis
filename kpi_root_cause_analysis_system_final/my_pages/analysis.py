import streamlit as st
import pandas as pd

def show():

    # ---------------- SESSION CHECK ----------------
    if "df" not in st.session_state:
        st.warning("Upload dataset in Dashboard first")
        return

    if "kpi" not in st.session_state:
        st.warning("Select KPI in Dashboard first")
        return

    df = st.session_state["df"].copy()
    kpi = st.session_state["kpi"]

    st.subheader("📉 KPI Drop Detection")

    # ---------------- CLEAN DATA ----------------
    # convert all numeric safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        st.error("No numeric data available")
        return

    # ---------------- HANDLE KPI ----------------
    if kpi == "All":
        st.info("⚠️ Using average of numeric columns")

        df["kpi_calc"] = numeric.mean(axis=1)

    else:
        if kpi not in df.columns:
            st.error("Selected KPI not found")
            return

        if kpi not in numeric.columns:
            st.error("Selected KPI is not numeric")
            return

        df["kpi_calc"] = pd.to_numeric(df[kpi], errors="coerce")

    # ---------------- DROP DETECTION ----------------
    df["change"] = df["kpi_calc"].pct_change()

    # remove invalid rows
    df = df.dropna(subset=["change"])

    drops = df[df["change"] < -0.2]

    if not drops.empty:
        st.error("🚨 KPI Drops Detected")
        st.dataframe(drops.head())
    else:
        st.success("✅ No major drops detected")

    # ---------------- ROOT CAUSE ----------------
    st.subheader("🔍 Root Cause Analysis")

    numeric = df.select_dtypes(include="number")

    if numeric.shape[1] < 2:
        st.warning("Not enough numeric columns for correlation")
        return

    try:
        if kpi == "All":
            corr_series = numeric.corr().mean().sort_values()
        else:
            corr_series = numeric.corr()[kpi].drop(kpi).sort_values()

        st.write("📉 Negative Factors")
        st.dataframe(corr_series.head(3))

        st.write("📈 Positive Factors")
        st.dataframe(corr_series.tail(3))

    except Exception as e:
        st.error("Error in correlation calculation")
        return

    # ---------------- AI STYLE EXPLANATION ----------------
    st.subheader("🤖 Why KPI Dropped?")

    try:
        negatives = corr_series.head(2).index.tolist()

        if negatives:
            explanation = f"""
            The KPI drop is mainly influenced by {', '.join(negatives)}.
            These factors show negative correlation with the KPI.
            """
            st.info(explanation)
        else:
            st.info("No strong negative factors found")

    except:
        st.warning("Not enough data for explanation")