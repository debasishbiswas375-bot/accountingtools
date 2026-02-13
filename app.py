import streamlit as st
from supabase import create_client

# Project Connection
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# CSS for the Google-style profile icon
st.markdown("""<style>.google-avatar { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #4285F4; float: right; }</style>""", unsafe_allow_html=True)

# Top Header
col1, col2 = st.columns([10, 1])
with col1: st.title("🚀 TallyTools.in")
with col2:
    if 'user' in st.session_state:
        # Dynamic avatar based on your email
        initial = st.session_state['user'].email[0].upper()
        st.markdown(f'<img src="https://ui-avatars.com/api/?name={initial}&background=random" class="google-avatar">', unsafe_allow_html=True)

# Sidebar User Report showing your 100 points
with st.sidebar:
    st.header("Account Report")
    if 'user' in st.session_state:
        user = st.session_state['user']
        # This fetches the points from the SQL table you created
        try:
            profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
            if profile.data:
                st.write(f"📧 **Mail:** {user.email}")
                st.metric("Credits Available", f"{profile.data['points']} pts")
                st.progress(profile.data['points'] / 100)
            if st.button("Sign Out"):
                supabase.auth.sign_out()
                del st.session_state['user']
                st.rerun()
        except:
            st.warning("Profile syncing... please refresh.")
