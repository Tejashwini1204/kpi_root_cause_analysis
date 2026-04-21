import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors #type: error
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


# ---------------- REPORT FUNCTION ----------------
def generate_report(df, kpi):

    os.makedirs("reports", exist_ok=True)

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='TitleStyle', fontSize=20, alignment=TA_CENTER, spaceAfter=15))
    styles.add(ParagraphStyle(name='InsightStyle', fontSize=13, alignment=TA_JUSTIFY, leading=20))

    pdf_path = "reports/final_report.pdf"
    content = []

    # ---------------- TITLE ----------------
    content.append(Paragraph("KPI Root Cause Analysis Report", styles["TitleStyle"]))
    content.append(Spacer(1, 15))

    # ---------------- KPI SUMMARY ----------------
    numeric = df.select_dtypes(include="number")

    if kpi == "All":
        total = numeric.sum().sum()
        avg = numeric.mean().mean()
    else:
        total = df[kpi].sum()
        avg = df[kpi].mean()

    count = len(df)

    data = [
        ["KPI", kpi],
        ["Total", round(total, 2)],
        ["Average", round(avg, 2)],
        ["Records", count]
    ]

    table = Table(data, colWidths=[120, 200])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(Paragraph("KPI Summary", styles["Heading2"]))
    content.append(Spacer(1, 8))
    content.append(table)
    content.append(Spacer(1, 25))

    # ---------------- HEATMAP ----------------
    # ---------------- HEATMAP (FIXED FOR ALL) ----------------
    try:

        heat_path = "reports/heatmap.png"

        if kpi == "All":

            # 🔥 FULL correlation (same as dashboard)
            corr = numeric.corr()

        else:

            if kpi in numeric.columns and len(numeric.columns) > 2:
                corr_target = numeric.corr()[kpi].abs().sort_values(ascending=False)
                top_cols = corr_target.index[:6]
                corr = numeric[top_cols].corr()
            else:
                corr = None

        if corr is not None:

            plt.figure(figsize=(6,5))
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
            plt.tight_layout()
            plt.savefig(heat_path)
            plt.close()

            content.append(Paragraph("Correlation Heatmap", styles["Heading2"]))
            content.append(Image(heat_path, width=400, height=300))
            content.append(Spacer(1, 20))

    except:
        pass

    # ---------------- HISTOGRAM ----------------
    try:
        if kpi != "All":

            hist_path = "reports/hist.png"

            plt.figure(figsize=(6,4))
            sns.histplot(df[kpi], bins=30, kde=True)
            plt.title(f"{kpi} Distribution")
            plt.tight_layout()
            plt.savefig(hist_path)
            plt.close()

            content.append(Paragraph("KPI Distribution", styles["Heading2"]))
            content.append(Image(hist_path, width=400, height=250))
            content.append(Spacer(1, 20))

    except:
        pass

    # ---------------- BOXPLOT ----------------
    try:
        if kpi != "All":

            box_path = "reports/box.png"

            plt.figure(figsize=(6,4))
            sns.boxplot(y=df[kpi])
            plt.title("Outlier Detection")
            plt.tight_layout()
            plt.savefig(box_path)
            plt.close()

            content.append(Paragraph("Outlier Detection", styles["Heading2"]))
            content.append(Image(box_path, width=400, height=250))
            content.append(Spacer(1, 20))

    except:
        pass

    # ---------------- PIE (FIXED FOR ALL) ----------------
    try:
        if kpi != "All":

            cat_cols = df.select_dtypes(include="object").columns

            if len(cat_cols) > 0:

                category = cat_cols[0]
                pie_data = df.groupby(category)[kpi].sum().reset_index()

                pie_path = "reports/pie.png"

                plt.figure(figsize=(6,6))
                plt.pie(pie_data[kpi], labels=pie_data[category], autopct='%1.1f%%')
                plt.title(f"{kpi} Contribution by {category}")
                plt.tight_layout()
                plt.savefig(pie_path)
                plt.close()

                content.append(Paragraph("KPI Contribution by Category", styles["Heading2"]))
                content.append(Image(pie_path, width=400, height=300))
                content.append(Spacer(1, 25))

    except:
        pass

    # ---------------- FINAL INSIGHT ----------------
    try:
        if kpi != "All" and kpi in numeric.columns:

            corr = numeric.corr()[kpi].sort_values()
            neg = corr.head(2).index.tolist()

            insight_text = f"""
            The KPI '{kpi}' is dropping mainly because areas like {', '.join(neg)} are not performing well. 
            Improving these areas can increase overall performance.
            """

            insight_box = Table([[Paragraph(insight_text, styles["InsightStyle"])]], colWidths=[450])

            insight_box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 12),
            ]))

            content.append(Paragraph("Conclusion", styles["Heading2"]))
            content.append(Spacer(1, 10))
            content.append(insight_box)

    except:
        pass

    # ---------------- BUILD PDF ----------------
    pdf = SimpleDocTemplate(pdf_path)
    pdf.build(content)

    return pdf_path


# ---------------- STREAMLIT ----------------
def show():

    st.title("📄 Reports")

    if "df" not in st.session_state or "kpi" not in st.session_state:
        st.error("⚠️ Please load dataset and KPI in Dashboard first")
        return

    df = st.session_state["df"]
    kpi = st.session_state["kpi"]

    if st.button("🚀 Generate PDF Report"):

        with st.spinner("Generating premium report..."):
            path = generate_report(df, kpi)

        st.success("✅ Report Ready!")

        with open(path, "rb") as f:
            st.download_button(
                "📥 Download Report",
                f,
                file_name="KPI_Report.pdf"
            )