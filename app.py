import streamlit as st
import pandas as pd
from parallel_audit import audit_many

st.set_page_config(
    page_title="Beardly SEO Lead Finder",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Beardly SEO Bulk Auditor")

st.write(
"""
Upload a CSV containing a column named **website**.
The system will crawl each site and run an SEO audit.
"""
)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        if "website" not in df.columns:
            st.error("CSV must contain a column called 'website'")
        else:

            websites = df["website"].dropna().tolist()

            st.success(f"{len(websites)} websites loaded.")

            if st.button("Start SEO Audit"):

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []

                total = len(websites)

                for i, chunk_start in enumerate(range(0, total, 20)):

                    chunk = websites[chunk_start:chunk_start+20]

                    status_text.text(f"Auditing websites {chunk_start+1} - {min(chunk_start+20,total)}")

                    chunk_results = audit_many(chunk)

                    results.extend(chunk_results)

                    progress_bar.progress(min((chunk_start+20)/total,1.0))

                results_df = pd.DataFrame(results)

                st.subheader("Audit Results")

                st.dataframe(results_df, use_container_width=True)

                csv = results_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "Download Results CSV",
                    csv,
                    "seo_audit_results.csv",
                    "text/csv"
                )

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
