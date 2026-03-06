import streamlit as st
import pandas as pd
from audit import audit_site

st.title("Beardly SEO Bulk Auditor")

uploaded_file = st.file_uploader("Upload CSV with websites", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if "website" not in df.columns:
        st.error("CSV must contain a column named 'website'")
    else:

        results = []

        progress = st.progress(0)

        for i, url in enumerate(df["website"]):

            score, issues, data = audit_site(url)

            results.append({
    "website": url,
    "seo_score": score,
    "title": data.get("title"),
    "word_count": data.get("word_count"),
    "internal_links": data.get("internal_links"),
    "issues": ", ".join(issues)
})

            progress.progress((i+1)/len(df))

        results_df = pd.DataFrame(results)

        st.subheader("Audit Results")
        st.dataframe(results_df)

        csv = results_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Results CSV",
            csv,
            "seo_audit_results.csv",
            "text/csv"
        )
