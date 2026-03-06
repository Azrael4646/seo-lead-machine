import streamlit as st
from audit import audit_site
from email_finder import find_email

st.title("Beardly SEO Lead Finder")

website = st.text_input("Enter business website")

if st.button("Run SEO Audit"):

    score, issues, html = audit_site(website)

    emails = find_email(html)

    st.subheader("SEO Score")
    st.write(score)

    st.subheader("Issues Found")
    st.write(issues)

    st.subheader("Emails Found")
    st.write(emails)
