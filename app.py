import streamlit as st
from streamlit_oauth import OAuth2Component
st.set_page_config(page_title="MailMind AI", page_icon="📧")

# Login screen
if not st.user.is_logged_in:
    st.title("📧 MailMind AI")
    st.subheader("Executive Email Intelligence Platform")

    if st.button("Continue with Google"):
        st.login("google")
    st.stop()

# After login
st.title("📧 MailMind AI")
st.success(f"Welcome, {st.user.name}!")
st.write(st.user.email)

# Gmail API
service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(userId="me", maxResults=10).execute()
messages = results.get("messages", [])

st.subheader("Latest Emails")

for msg in messages:
    email = service.users().messages().get(
        userId="me", id=msg["id"], format="metadata"
    ).execute()

    headers = email["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")

    st.write(f"**{subject}**")
    st.caption(sender)
    st.divider()

if st.button("Logout"):
    st.logout()

