import streamlit as st

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

st.write("**Email:**", st.user.email)

if st.button("Logout"):
    st.logout()
