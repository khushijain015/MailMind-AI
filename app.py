import streamlit as st
st.set_page_config(page_title="MailMind AI", page_icon="📧")

if not st.user.is_logged_in:
    st.title("📧 MailMind AI")
    st.subheader("Executive Email Intelligence Platform")

    st.write("Sign in with your Google account")

    if st.button("🔐 Continue with Google"):
        st.login("google")

    st.stop()

st.title("📧 MailMind AI")
st.success(f"Welcome {st.user.name}!")

st.write("Email:", st.user.email)

if st.button("Logout"):
    st.logout()
