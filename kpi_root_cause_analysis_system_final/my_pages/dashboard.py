import streamlit as st
import pandas as pd
import plotly.express as px
import io


# ---------------- LOAD DATA ----------------
def load_data(file_bytes):
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except:
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), sep=";")
        except:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding="latin1")

    return df.dropna(axis=1, how="all")


# ---------------- MAIN FUNCTION ----------------
def show():

    st.subheader("📂 Upload Dataset")

    file = st.file_uploader("Upload CSV")

    if file is not None:
        st.session_state["uploaded_file"] = file.getvalue()

    file_bytes = st.session_state.get("uploaded_file", None)

    if file_bytes:

        df = load_data(file_bytes)
        st.session_state["df"] = df

        st.success("Dataset Loaded Successfully")
        st.write("📌 Columns:", list(df.columns))

        # ---------------- KPI SELECTION ----------------
        numeric_cols = df.select_dtypes(include="number").columns
        numeric_cols = [c for c in numeric_cols if "id" not in c.lower() and "code" not in c.lower()]

        if len(numeric_cols) == 0:
            st.error("No numeric columns found for KPI")
            return

        # 🔥 ADD "ALL"
        kpi_options = ["All"] + list(numeric_cols)

        st.subheader("🎯 Select KPI")

        kpi = st.selectbox("Choose KPI", kpi_options)

        st.session_state["kpi"] = kpi

        # ---------------- KPI METRICS ----------------
        if kpi != "All":

            total = df[kpi].sum()
            avg = df[kpi].mean()
            count = len(df)

            st.session_state["total"] = total
            st.session_state["avg"] = avg
            st.session_state["count"] = count

            c1, c2, c3 = st.columns(3)

            c1.markdown(f"<div class='metric-container'>Total<br>{round(total,2)}</div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-container'>Average<br>{round(avg,2)}</div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-container'>Records<br>{count}</div>", unsafe_allow_html=True)

        else:
            st.subheader("📊 Overall Dataset Summary")
            st.dataframe(df.describe())

        # ---------------- HEATMAP ----------------
        st.subheader("🔥 Correlation Heatmap")

        numeric = df.select_dtypes(include="number")

        if len(numeric.columns) > 1:

            if kpi == "All":
                corr = numeric.corr()
            else:
                corr_target = numeric.corr()[kpi].abs().sort_values(ascending=False)
                top_cols = corr_target.index[:6]
                corr = numeric[top_cols].corr()

            fig_heat = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="RdBu"
            )

            st.plotly_chart(fig_heat, use_container_width=True)
            #st.session_state["fig"] = fig_heat
            st.session_state["heatmap_fig"] = fig_heat

        # ---------------- DISTRIBUTION ----------------
        if kpi != "All":
            st.subheader("📊 KPI Distribution")

            fig_hist = px.histogram(df, x=kpi, nbins=30)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.session_state["hist_fig"] = fig_hist

        # ---------------- OUTLIER ----------------
        if kpi != "All":
            st.subheader("⚠️ Outlier Detection")

            fig_box = px.box(df, y=kpi)
            st.plotly_chart(fig_box, use_container_width=True)
            st.session_state["box_fig"] = fig_box

       
        # ---------------- PIE CHART (CATEGORY IMPACT) ----------------
        if kpi != "All":

            st.subheader("🥧 KPI Contribution by Category")

            # find best categorical column
            cat_cols = df.select_dtypes(include="object").columns

            if len(cat_cols) > 0:

                category = cat_cols[0]  # pick first categorical

                pie_data = df.groupby(category)[kpi].sum().reset_index()

                fig_pie = px.pie(
                    pie_data,
                    names=category,
                    values=kpi,
                    title=f"{kpi} Contribution by {category}"
                )

                st.plotly_chart(fig_pie, use_container_width=True)

            else:
                st.info("No categorical column available for pie chart")
                # ✅ CLEAR OLD VALUE (VERY IMPORTANT)
                st.session_state["pie_fig"] = None

        # ---------------- LOW KPI RECORDS ----------------
        if kpi != "All":
            st.subheader("📉 Low KPI Records (Root Cause)")

            try:
                low_data = df.nsmallest(5, kpi)
                st.dataframe(low_data)
            except:
                st.warning("Unable to extract low records")

        # ---------------- 🤖 AI INSIGHT ----------------
        #if kpi != "All":

            #st.subheader("🧠 AI Insight")

            #corr = numeric.corr()[kpi].sort_values()

            #neg = corr.head(2)
            #pos = corr.tail(2)

           # st.write(f"""
            #KPI **{kpi}** total is **{round(df[kpi].sum(),2)}**.

            #🔻 Negative factors: {list(neg.index)}  
            #🔺 Positive factors: {list(pos.index)}  

            #👉 Improve negative factors to increase KPI.
            #""")

        # ---------------- 🤖 WHY KPI DROPPED ----------------
        if kpi != "All":

            st.subheader("🤖 Why KPI Dropped (Auto Explanation)")

            numeric = df.select_dtypes(include="number")
            corr = numeric.corr()[kpi].sort_values()

            neg = corr.head(3)
            pos = corr.tail(3)

            low_data = df.nsmallest(5, kpi)

            explanation = f"""
            The KPI **{kpi}** shows fluctuations due to multiple factors.

            🔻 Major reasons for drop:
            """

            for col, val in neg.items():
                explanation += f"\n- {col} has negative correlation ({round(val,2)})"

            explanation += "\n\n📉 Observations from lowest records:\n"

            for col in low_data.columns[:3]:
                explanation += f"- {col} values are relatively low or inconsistent\n"

            explanation += f"""
            
            🔺 Positive drivers:
            """

            for col, val in pos.items():
                explanation += f"\n- {col} improves KPI ({round(val,2)})"

            explanation += """

            👉 Final Insight:
            KPI is dropping mainly due to negative influencing variables and poor-performing records.
            Improving these factors can stabilize and increase KPI performance.
            """

            st.write(explanation)

        # ---------------- 📈 PREDICTION ----------------
        if kpi != "All":

            try:
                from sklearn.linear_model import LinearRegression

                st.subheader("📈 KPI Prediction")

                X = numeric.drop(columns=[kpi])
                y = numeric[kpi]

                X = X.fillna(0)
                y = y.fillna(0)

                if len(X.columns) > 0:

                    model = LinearRegression()
                    model.fit(X, y)

                    sample = X.iloc[-1:].values
                    pred = model.predict(sample)[0]

                    st.metric("Predicted KPI", round(pred, 2))

            except:
                st.info("Install scikit-learn for prediction feature")

    else:
        st.info("Please upload a dataset to continue")