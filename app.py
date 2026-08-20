import streamlit as st
import pandas as pd

st.set_page_config(page_title="MailMind AI", page_icon="📧")

user_name = "Khushi"

st.markdown("# 📧 MailMind AI")
st.markdown("### Executive Email Intelligence Platform")

st.write(
    "Transform crowded inboxes into actionable insights using AI-powered email summarization, priority detection, and business analytics."
)

st.markdown("---")

# Sample inbox (our AI output)
emails = [
    {
        "Category":"HR",
        "Priority":"High",
        "Summary":"Interview scheduled for Friday at 11:00 AM",
        "Action":"Confirm availability",
        "Deadline":"Today 5:00 PM",
        "Full Email":"From: Deloitte HR\n\nSubject: Interview Confirmation\n\nYour interview is scheduled for Friday at 11:00 AM.\nPlease confirm before 5:00 PM today."
    },
    {
        "Category":"Academic",
        "Priority":"High",
        "Summary":"Business Analytics assignment due",
        "Action":"Submit assignment",
        "Deadline":"21 Aug",
        "Full Email":"From: Professor Sharma\n\nSubject: Assignment Deadline\n\nSubmit the Business Analytics assignment before 21 August 11:59 PM."
    },
    {
        "Category":"Personal",
        "Priority":"Low",
        "Summary":"Amazon order has been shipped",
        "Action":"Track package",
        "Deadline":"22 Aug",
        "Full Email":"From: Amazon\n\nSubject: Order Shipped\n\nYour wireless mouse has been shipped and will arrive on 22 August."
    }
]

df = pd.DataFrame(emails)

st.markdown(
    """
    <div style="padding:18px;border-radius:12px;background:#E8F5E9;border-left:6px solid #2E7D32;">
        <h4 style="margin:0;color:#1B5E20;">✨ AI Analysis Complete</h4>
        <p style="margin:6px 0 0 0;color:#2E7D32;">
            MailMind successfully analyzed 3 emails and generated actionable insights.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.dataframe(
    df.drop(columns=["Full Email"]),
    use_container_width=True
)
col1, col2, col3 = st.columns(3)

col1.metric("📧 Total Emails", len(df))
col2.metric("🔴 High Priority", (df["Priority"] == "High").sum())
col3.metric("🟢 Low Priority", (df["Priority"] == "Low").sum())
st.subheader("📂 Filter Inbox")
st.markdown("---")
st.subheader("☀️ Daily Executive Brief")

high = (df["Priority"] == "High").sum()
low = (df["Priority"] == "Low").sum()

st.info(
    f"""
    **Good Morning, {user_name}!**

    You received **{len(df)} emails** today.

    **{high} require immediate attention** and **{low} are informational.**

    **Estimated reading time:** 1 minute.
    """
)

st.markdown("---")
st.subheader("✅ AI Action Center")

for _, row in df.iterrows():
    if row["Priority"] == "High":
        st.error(f"🔴 {row['Action']}  |  {row['Deadline']}")
    else:
        st.success(f"🟢 {row['Action']}  |  {row['Deadline']}")
st.markdown("---")
st.subheader("🗓️ Upcoming Deadlines")

for _, row in df.iterrows():
    st.write(f"**📅 {row['Deadline']}**")
    st.caption(row["Action"])
# Existing code continues
st.subheader("📂 Smart Inbox")

search = st.text_input(
    "🔍 Search emails",
    placeholder="Interview, Amazon, Assignment..."
)

selected_priority = st.selectbox(
    "Choose Priority",
    ["All", "High", "Low"]
)
st.markdown("---")
st.subheader("📊 Productivity Analytics")

urgent_pct = round((high / len(df)) * 100)
top_category = df["Category"].mode()[0]
pending = (df["Priority"] == "High").sum()

a, b, c, d = st.columns(4)

a.metric("Urgent", f"{urgent_pct}%")
b.metric("Top Category", top_category)
c.metric("Pending", pending)
d.metric("Read Time", "1 min")

if selected_priority == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Priority"] == selected_priority].copy()

if search:
    filtered_df = filtered_df[
        filtered_df.astype(str)
        .apply(lambda col: col.str.contains(search, case=False))
        .any(axis=1)
    ]

st.markdown("---")
st.subheader("📬 Smart Inbox")

for _, row in filtered_df.iterrows():

    if row["Priority"] == "High":
        priority_color = "#E53935"
        badge = "🔴 HIGH"
    else:
        priority_color = "#43A047"
        badge = "🟢 LOW"

    st.markdown(
        f"""
        <div style="
            border:1px solid #E0E0E0;
            border-left:6px solid {priority_color};
            border-radius:12px;
            padding:16px;
            margin-bottom:14px;
            background:white;
        ">
            <div style="display:flex;justify-content:space-between;">
                <b>{row['Category']}</b>
                <span>{badge}</span>
            </div>

            <h4 style="margin:10px 0 6px 0;">
                {row['Summary']}
            </h4>

            <p><b>Action:</b> {row['Action']}</p>
            <p><b>Deadline:</b> {row['Deadline']}</p>

            <hr>

            <b>Full Email</b>
            <p>{row['Full Email']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )