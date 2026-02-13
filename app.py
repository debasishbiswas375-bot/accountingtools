import streamlit as st
from supabase import create_client

# Project Connection
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# 1. Page Config
st.set_page_config(page_title="TallyTools.in", page_icon="🚀", layout="wide")

# 2. CSS for Google-style Profile Icon
st.markdown("""
    <style>
    .google-avatar {
        width: 45px; height: 45px; border-radius: 50%;
        border: 2px solid #4285F4; object-fit: cover;
        float: right; margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header with Dynamic Profile Icon
col_h1, col_h2 = st.columns([10, 1])
with col_h1:
    st.title("🚀 TallyTools.in")
with col_h2:
    if 'user' in st.session_state:
        # Google-style initial avatar
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">', unsafe_allow_html=True)
    else:
        st.markdown('<img src="https://ui-avatars.com/api/?name=?&background=cccccc" class="google-avatar">', unsafe_allow_html=True)

# 4. Sidebar Google-style User Report
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        try:
            # This line connects to the SQL table you created
            profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            data = profile.data
            
            st.markdown(f"📧 **Mail ID:**\n`{user.email}`")
            st.markdown(f"👤 **Name:**\n{user.email.split('@')[0].title()}")
            
            st.divider()
            st.markdown("### 💳 Plan Details")
            st.metric("Credits Available", f"{data['points']} pts")
            st.info(f"**Status:** {data['rank']}")
            st.progress(data['points'] / 100)
            
            if st.button("Sign Out"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except Exception:
            st.warning("⚠️ Profile data not found. Please refresh the page.")
    else:
        st.info("Log in to see your account report.")

# 5. Main Content
st.subheader("Free Accounting Education & Tally Automation")
st.divider()
c1, c2, c3 = st.columns(3)
with c1: st.markdown("### 📖 Learning Hub")
with c2: st.markdown("### 🛠️ Tally Converter")
with c3: st.markdown("### 🏆 My Progress")
