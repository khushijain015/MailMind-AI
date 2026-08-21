import streamlit as st
from streamlit_oauth import OAuth2Component

st.set_page_config(page_title="MailMind AI", page_icon="📧")

# OAuth Component
oauth2 = OAuth2Component(
    client_id=st.secrets["auth_google"]["client_id"],
    client_secret=st.secrets["auth_google"]["client_secret"],
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
)

# Keep token in session
if "token" not in st.session_state:
    st.session_state.token = None

st.title("📧 MailMind AI")
st.subheader("Executive Email Intelligence Platform")

# LOGIN
if st.session_state.token is None:

    token = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com/favicon.ico",
        redirect_uri="https://mailmind-ai-015.streamlit.app/oauth2callback",
        scope="openid email profile https://www.googleapis.com/auth/gmail.readonly",
        key="google",
    )

    # Save token immediately
    if token:
        st.session_state.token = token
        st.rerun()

# AFTER LOGIN
else:
    st.success("✅ Logged in successfully!")

    st.write("### Access Token")
    st.code(st.session_state.token["token"]["access_token"])

    st.write("### Token Info")
    st.json(st.session_state.token)

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()
