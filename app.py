import streamlit as st
from supabase import create_client

# These names must match your Secrets exactly
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

# If the URL is fixed in Step 1, this will no longer crash
supabase = create_client(URL, KEY)

st.set_page_config(page_title="TallyTools.in", page_icon="🚀", layout="wide")

# 2. UI Styling for Circular Profile Icon
st.markdown("""
    <style>
    .google-avatar {
        width: 45px; height: 45px; border-radius: 50%;
        border: 2px solid #4285F4; float: right; margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header with Dynamic Avatar
col_h1, col_h2 = st.columns([10, 1])
with col_h1:
    st.title("🚀 TallyTools.in")
with col_h2:
    if 'user' in st.session_state:
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">', unsafe_allow_html=True)

# 4. Sidebar Account Report with Expiry Logic
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        try:
            # Fetch data from Supabase
            response = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            data = response.data
            
            # Calculate Time Remaining
            # Note: plan_started_at is a string, we convert to datetime object
            start_date = datetime.fromisoformat(data['plan_started_at'].replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            days_passed = (now - start_date).days
            
            if data['rank'] == "Pro Pack":
                days_left = 90 - days_passed # 3 Months
                st.warning(f"👑 **Pro Pack** ({max(0, days_left)} days left)")
                st.metric("Credits", "Unlimited")
            else:
                days_left = 30 - days_passed # 1 Month
                st.success(f"🔓 **Starter Plan** ({max(0, days_left)} days left)")
                st.metric("Credits Available", f"{data['points']} pts")
                st.progress(max(0, min(data['points'] / 100, 1.0)))

            st.markdown(f"📧 **Mail:**\n`{user.email}`")
            
            if st.button("Sign Out"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except Exception:
            st.warning("🔄 Syncing profile... Please refresh.")
    else:
        st.info("Log in to access your Tally tools.")

# 5. Main Content
st.subheader("Accounting Automation Hub")
st.write("Convert your Excel and PDF files to Tally XML format instantly.")
