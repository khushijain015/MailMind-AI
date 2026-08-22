import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64

st.set_page_config(page_title="MailMind AI", page_icon="📧")

# ---------- LOGIN ----------
if not st.user.is_logged_in:
    st.title("📧 MailMind AI")
    st.subheader("Executive Email Intelligence Platform")

    if st.button("Continue with Google"):
        st.login()

    st.stop()

# ---------- HOME ----------
st.title("📧 MailMind AI")
st.success(f"Welcome, {st.user.name}!")
st.write(st.user.email)

# Create Gmail service using OAuth token
creds = Credentials(token=st.context.headers["X-Streamlit-Token"])
service = build("gmail", "v1", credentials=creds)

st.header("📥 Latest Emails")

results = service.users().messages().list(
    userId="me",
    maxResults=10
).execute()

messages = results.get("messages", [])

if not messages:
    st.info("No emails found.")
else:
    for msg in messages:
        email = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = email["payload"]["headers"]

        sender = next((h["value"] for h in headers if h["name"]=="From"), "")
        subject = next((h["value"] for h in headers if h["name"]=="Subject"), "")
        date = next((h["value"] for h in headers if h["name"]=="Date"), "")

        with st.expander(subject if subject else "(No Subject)"):
            st.write(f"**From:** {sender}")
            st.write(f"**Date:** {date}")
