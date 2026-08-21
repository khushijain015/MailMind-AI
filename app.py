import streamlit as st
from streamlit_oauth import OAuth2Component

st.set_page_config(
    page_title="MailMind AI",
    page_icon="📧",
    layout="wide"
)

oauth2 = OAuth2Component(
    client_id=st.secrets["auth_google"]["client_id"],
    client_secret=st.secrets["auth_google"]["client_secret"],
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
)

st.title("📧 MailMind AI")
st.subheader("Executive Email Intelligence Platform")

if "token" not in st.session_state:
    result = oauth2.authorize_button(
        name="🔐 Continue with Google",
        redirect_uri=st.secrets["auth_google"]["redirect_uri"],
        scope="openid email profile",
        key="google",
    )

    if result and "token" in result:
        st.session_state["token"] = result["token"]
        st.rerun()

    st.info("Sign in with your Google account to access MailMind AI.")
    st.stop()

st.success("✅ Successfully signed in!")

st.write("Welcome to MailMind AI 🎉")

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric("Unread Emails", "127")
col2.metric("High Priority", "18")
col3.metric("Meetings Today", "6")

st.markdown("## AI Inbox Preview")

emails = [
    ["CEO", "Board meeting moved to 4 PM", "High"],
    ["HR", "Policy update for all employees", "Medium"],
    ["Amazon", "Your order has been shipped", "Low"],
    ["Client", "Urgent feedback required", "High"],
]

st.table(
    {
        "Sender": [e[0] for e in emails],
        "Subject": [e[1] for e in emails],
        "Priority": [e[2] for e in emails],
    }
)

if st.button("Logout"):
    del st.session_state["token"]
    st.rerun()
