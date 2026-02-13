import streamlit as st
from supabase import create_client
from datetime import datetime, timezone

# -----------------------------
# 1. Supabase Setup
# -----------------------------
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(URL, KEY)

st.set_page_config(page_title="TallyTools.in", page_icon="🚀", layout="wide")

# -----------------------------
# 2. Basic Styling
# -----------------------------
st.markdown("""
    <style>
    .google-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #4285F4;
        float: right;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# 3. Get Logged-in User
# -----------------------------
auth_response = supabase.auth.get_user()

if auth_response and auth_response.user:
    user = auth_response.user
    st.session_state["user"] = user
else:
    user = None

# -----------------------------
# 4. Header
# -----------------------------
col_h1, col_h2 = st.columns([10, 1])

with col_h1:
    st.title("🚀 TallyTools.in")

with col_h2:
    if user:
        initial = user.email[0].upper()
        st.markdown(
            f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">',
            unsafe_allow_html=True
        )

# -----------------------------
# 5. Sidebar Account Panel
# -----------------------------
with st.sidebar:
    st.header("Account Report")

    if user:
        try:
            uid = user.id
            email = user.email

            # Check profile
            profile = supabase.table("profiles").select("*").eq("id", uid).execute()

            # If profile does not exist → create automatically
            if not profile.data:
                supabase.table("profiles").insert({
                    "id": uid,
                    "email": email,
                    "rank": "Starter Plan",
                    "points": 100,
                    "plan_started_at": datetime.now(timezone.utc).isoformat()
                }).execute()

                profile = supabase.table("profiles").select("*").eq("id", uid).execute()

            data = profile.data[0]

            # -----------------------------
            # Plan Logic
            # -----------------------------
            start_date = datetime.fromisoformat(
                data["plan_started_at"].replace("Z", "+00:00")
            )
            now = datetime.now(timezone.utc)
            days_passed = (now - start_date).days

            if data["rank"] == "Pro Pack":
                days_left = 90 - days_passed
                st.warning(f"👑 **Pro Pack** ({max(0, days_left)} days left)")
                st.metric("Credits", "Unlimited")
            else:
                days_left = 30 - days_passed
                st.success(f"🔓 **Starter Plan** ({max(0, days_left)} days left)")
                st.metric("Credits Available", f"{data['points']} pts")
                st.progress(max(0, min(data["points"] / 100, 1.0)))

            st.markdown(f"📧 **Mail:**\n`{email}`")

            if st.button("Sign Out"):
                supabase.auth.sign_out()
                st.session_state.clear()
                st.rerun()

        except Exception as e:
            st.error("Profile sync error.")
            st.write(str(e))

    else:
        st.info("Log in to access your Tally tools.")

# -----------------------------
# 6. Main Content
# -----------------------------
st.subheader("Accounting Automation Hub")
st.write("Convert your Excel and PDF files to Tally XML format instantly.")
