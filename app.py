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
    .profile-pic {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #1a73e8;
        object-fit: cover;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Top Header with Logo ---
col1, col2 = st.columns([10, 1])
with col1:
    st.title("🚀 TallyTools.in")
with col2:
    # Placeholder profile image
    st.markdown('<img src="https://ui-avatars.com/api/?name=User&background=random" class="profile-pic">', unsafe_allow_html=True)

# --- Sidebar User Report (Google Style) ---
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        
        # Fetching Plan Details from our Profiles table
        try:
            profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            p_data = profile.data
            
            st.info(f"📧 **Email:**\n{user.email}")
            st.success(f"👤 **Name:**\n{p_data.get('email').split('@')[0].capitalize()}")
            
            with st.expander("💳 Plan & Credits"):
                st.write(f"**Current Plan:** Free Tier")
                st.write(f"**Credits Left:** {p_data.get('points')} pts")
                st.write(f"**Status:** {p_data.get('rank')}")
                st.progress(p_data.get('points')/1000) # Progress bar for credits
                
        except Exception:
            st.error("Login to view full report.")
    else:
        st.warning("No user logged in.")
        if st.button("Go to Login Page"):
            st.info("Navigate to 'Account' in the sidebar.")

# --- Main App Content ---
st.subheader("Free Accounting Education & Tally Automation")
st.divider()

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("### 📖 Learn")
    st.write("Deep dive into accounting principles.")
with col_b:
    st.markdown("### 🛠️ Automate")
    st.write("Convert Excel to Tally XML.")
with col_c:
    st.markdown("### 🏆 Progress")
    st.write("Track your scores.")
