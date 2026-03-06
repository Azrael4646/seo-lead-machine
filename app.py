import streamlit as st
import pandas as pd
from maps_scraper import get_maps_leads
from parallel_audit import audit_many

st.title("Beardly SEO Lead Finder")

tab1 = st.title(["Google Maps Lead Generator"])

# ----------------------------
# Google Maps Lead Generator
# ----------------------------

with tab1:

    query = st.text_input("Search Google Maps (example: plumber cape town)")

    if st.button("Find Businesses"):

        leads = get_maps_leads(query)

        df = pd.DataFrame(leads)

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Leads",
            csv,
            "maps_leads.csv",
            "text/csv"
        )

        # Run SEO audit automatically
        websites = df["website"].dropna().tolist()

        if websites:

            st.write("Running SEO audits...")

            results = audit_many(websites)

            results_df = pd.DataFrame(results)

            st.subheader("SEO Audit Results")

            st.dataframe(results_df)

            csv = results_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download SEO Leads",
                csv,
                "seo_leads.csv",
                "text/csv"
            )
