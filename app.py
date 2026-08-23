import streamlit as st
from streamlit_oauth import OAuth2Component
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

st.set_page_config(page_title="MailMind AI", page_icon="📧")
st.write("Loaded secrets:", list(st.secrets.keys()))
st.stop()

oauth2 = OAuth2Component(
    client_id=st.secrets["auth_google"]["client_id"],
    client_secret=st.secrets["auth_google"]["client_secret"],
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
)

if "token" not in st.session_state:
    st.session_state.token = None

st.title("📧 MailMind AI")

if st.session_state.token is None:

    result = oauth2.authorize_button(
        name="Continue with Google",
        redirect_uri=st.secrets["auth"]["redirect_uri"],
        scope="openid email profile https://www.googleapis.com/auth/gmail.readonly",
        key="google",
    )

    if result:
        st.session_state.token = result["token"]
        st.rerun()

    st.stop()

# Gmail
creds = Credentials(token=st.session_state.token["access_token"])
service = build("gmail", "v1", credentials=creds)

profile = service.users().getProfile(userId="me").execute()

st.success(f"Welcome {profile['emailAddress']}")

st.header("📥 Latest Emails")

results = service.users().messages().list(userId="me", maxResults=10).execute()

messages = results.get("messages", [])

for msg in messages:
    mail = service.users().messages().get(
        userId="me",
        id=msg["id"],
        format="metadata",
        metadataHeaders=["Subject", "From"],
    ).execute()

    subject = "No Subject"
    sender = "Unknown"

    for h in mail["payload"]["headers"]:
        if h["name"] == "Subject":
            subject = h["value"]
        if h["name"] == "From":
            sender = h["value"]

    st.write(f"**{subject}**")
    st.caption(sender)
    st.divider()

if st.button("Logout"):
    st.session_state.token = None
    st.rerun()
