import streamlit as st
from supabase import create_client

# Connection details
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

st.set_page_config(page_title="TallyTools.in", page_icon="🚀", layout="wide")

# --- CSS for Google Logo ---
st.markdown("""
    <style>
    .profile-pic {
        width: 42px; height: 42px; border-radius: 50%;
        border: 2px solid #4285F4; object-fit: cover; float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header with Logo ---
c1, c2 = st.columns([10, 1])
with c1:
    st.title("🚀 TallyTools.in")
with c2:
    if 'user' in st.session_state:
        # Use email initial for the Google-style icon
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="profile-pic">', unsafe_allow_html=True)

# --- Sidebar User Report ---
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        try:
            # Fetch the 100 points we just set up in SQL
            p = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            
            st.write(f"📧 **Mail ID:**\n{user.email}")
            st.write(f"👤 **Name:**\n{user.email.split('@')[0].title()}")
            
            st.divider()
            st.info(f"**Plan:** {p.data['rank']}")
            st.metric("Credits Available", f"{p.data['points']} pts")
            st.progress(p.data['points'] / 100)
            
            if st.button("Sign Out"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except:
            st.warning("Please run the SQL script in Supabase.")
    else:
        st.write("Logged out")

# --- Main Content ---
st.subheader("Free Accounting Education & Tally Automation")
st.divider()
cols = st.columns(3)
cols[0].markdown("### 📖 Learn")
cols[1].markdown("### 🛠️ Automate")
cols[2].markdown("### 🏆 Progress")
