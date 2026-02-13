import streamlit as st
from supabase import create_client

# Project Connection
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

st.set_page_config(page_title="TallyTools.in", page_icon="🚀", layout="wide")

# --- CSS for Google-style Profile Icon ---
st.markdown("""
    <style>
    .google-avatar {
        width: 45px; height: 45px; border-radius: 50%;
        border: 2px solid #4285F4; object-fit: cover;
        float: right; margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header with Dynamic Icon ---
col1, col2 = st.columns([10, 1])
with col1:
    st.title("🚀 TallyTools.in")
with col2:
    if 'user' in st.session_state:
        # Initial-based avatar mimicking Google
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">', unsafe_allow_html=True)

# --- Sidebar User Report ---
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        try:
            # This fetches the 100 points you just set up in SQL
            profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            data = profile.data
            
            st.markdown(f"📧 **Mail ID:**\n`{user.email}`")
            st.markdown(f"👤 **Name:**\n{user.email.split('@')[0].title()}")
            
            st.divider()
            st.markdown("### 💳 Plan Details")
            st.metric("Credits Available", f"{data['points']} pts")
            st.progress(data['points'] / 100) # Progress bar for the 100 initial credits
            
            if st.button("Sign Out"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except Exception:
            # Safety message if SQL wasn't fully applied to your user
            st.warning("⚠️ Profile not synced. Please re-run the 'Retroactive' part of the SQL script.")
    else:
        st.info("Log in to see your account report.")

# Main Page Content
st.subheader("Free Accounting Education & Tally Automation")
