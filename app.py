import streamlit as st
from supabase import create_client

# Project Connection
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# --- 1. CSS for Google-style Profile Icon ---
st.markdown("""
    <style>
    .google-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #4285F4; /* Google Blue */
        object-fit: cover;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Top Header with Dynamic Icon ---
col1, col2 = st.columns([10, 1])
with col1:
    st.title("🚀 TallyTools.in")
with col2:
    if 'user' in st.session_state:
        # Initial-based avatar
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">', unsafe_allow_html=True)
    else:
        st.markdown('<img src="https://ui-avatars.com/api/?name=?&background=cccccc" class="google-avatar">', unsafe_allow_html=True)

# --- 3. Sidebar User Report ---
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        try:
            # Fetch real-time data
            profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            data = profile.data
            
            st.markdown(f"📧 **Mail ID:**\n`{user.email}`")
            st.markdown(f"👤 **Name:**\n{user.email.split('@')[0].title()}")
            
            st.divider()
            st.markdown("### 💳 Plan Details")
            st.info(f"**Current Plan:** Starter (100 Credits)")
            st.metric("Credits Available", f"{data['points']} pts")
            st.progress(data['points'] / 100) # Progress bar based on 100 initial credits
            
            if st.button("Logout"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except Exception:
            st.error("Could not load profile. Ensure SQL script was run.")
    else:
        st.warning("No user logged in.")
        st.info("Please login in the 'Account' page to see your report.")

# --- 4. Main Page Content ---
st.subheader("Free Accounting Education & Tally Automation")
st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 📖 Learn")
    st.write("Deep dive into accounting principles.")
with c2:
    st.markdown("### 🛠️ Automate")
    st.write("Convert Excel to Tally XML.")
with c3:
    st.markdown("### 🏆 Progress")
    st.write("Track your scores.")
