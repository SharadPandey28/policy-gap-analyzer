import streamlit as st
import pandas as pd
import plotly.express as px
import tempfile
import os

from app.service import analyze_policy


# ======================================================
# PAGE CONfIG
# ======================================================
st.set_page_config(
    page_title="Cybersecurity Policy Gap Analyzer",
    layout="wide"
)

st.title("🔐 Cybersecurity Policy Gap Analyzer")
st.caption("Offline AI + NLP powered compliance dashboard (Ollama local)")


# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.header("Settings")
# FRAMEWORK
framework = st.sidebar.selectbox(
    "Framework",
    ["NIST CSF", "CIS Controls v8"]
)
# ANALYSIS
analysis_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Quick", "Standard", "Deep"]
)
# RISK LEVEL
risk_level = st.sidebar.slider(
    "Detection Strictness",
    1, 5, 3
)

st.sidebar.markdown("---")
st.sidebar.write("✅ Fully offline")
st.sidebar.write("✅ Local LLM (Ollama)")
st.sidebar.write("✅ No cloud APIs")


# ======================================================
# FILE UPLOAD
# ======================================================
uploaded_file = st.file_uploader(
    "Upload Policy Document (.pdf or .txt)",
    type=["pdf", "txt"]
)

analyze_btn = st.button("Analyze Policy")


# ======================================================
# RUN ANALYSIS
# ======================================================
if analyze_btn:

    if not uploaded_file:
        st.warning("Please upload a file first")
        st.stop()

    with st.spinner("Running offline NLP + Ollama analysis..."):

        suffix = "." + uploaded_file.name.split(".")[-1]

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(uploaded_file.read())
        tmp.close()

        result = analyze_policy(tmp.name)

        os.unlink(tmp.name)

    st.success("Analysis Complete ✅")


    # ======================================================
    # DATA PREP
    # ======================================================
    df = pd.DataFrame(result["gap_report"])

    covered = len(df[df.coverage == "Covered"])
    partial = len(df[df.coverage == "Partial"])
    missing = len(df[df.coverage == "Missing"])
    total = len(df)

    compliance = round((covered / total) * 100) if total else 0


    # ======================================================
    # TABS
    # ======================================================
    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "📋 Gap Analysis",
        "🛠 Revised Policy & Roadmap"
    ])


    # ======================================================
    # TAB 1 — OVERVIEW
    # ======================================================
    with tab1:

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Controls", total)
        col2.metric("Covered", covered)
        col3.metric("Compliance Score", f"{compliance}%")

        st.progress(compliance / 100)

        # Pie chart
        pie_df = pd.DataFrame({
            "Status": ["Covered", "Partial", "Missing"],
            "Count": [covered, partial, missing]
        })

        st.plotly_chart(
            px.pie(
                pie_df,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map={
                    "Covered": "green",
                    "Partial": "orange",
                    "Missing": "red"
                }
            ),
            use_container_width=True
        )

        # Risk summary
        if compliance >= 80:
            st.success("Low Risk – Policy mostly compliant")
        elif compliance >= 50:
            st.warning("Moderate Risk – Some gaps exist")
        else:
            st.error("High Risk – Critical controls missing")


    # ======================================================
    # TAB 2 — GAP ANALYSIS
    # ======================================================
    with tab2:

        st.subheader("Control Level Results")

        st.dataframe(df, use_container_width=True)

        st.plotly_chart(
            px.bar(
                pie_df,
                x="Status",
                y="Count",
                text="Count",
                color="Status"
            ),
            use_container_width=True
        )

        # download CSV
        st.download_button(
            "⬇ Download Gap Report (CSV)",
            df.to_csv(index=False),
            "gap_report.csv"
        )


    # ======================================================
    # TAB 3 — REVISED POLICY + ROADMAP
    # ======================================================
    with tab3:

        st.subheader("AI Revised Policy")

        st.text_area(
            "",
            result["revised_policy"],
            height=350
        )

        st.download_button(
            "⬇ Download Revised Policy",
            result["revised_policy"],
            "revised_policy.txt"
        )

        st.divider()

        st.subheader("Remediation Roadmap")

        st.text_area(
            "",
            result["roadmap"],
            height=200
        )

        st.download_button(
            "⬇ Download Roadmap",
            result["roadmap"],
            "roadmap.txt"
        )
