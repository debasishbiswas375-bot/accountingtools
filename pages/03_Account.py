import streamlit as st
from supabase import create_client

# Project details
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

if 'user' in st.session_state:
    user_id = st.session_state['user'].id
    
    # Fetch profile data from the table we just created
    profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    
    if profile.data:
        st.subheader(f"Welcome back, {profile.data['email']}!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Points", profile.data['points'])
        with col2:
            st.metric("Rank", profile.data['rank'])
            
    if st.button("Sign Out"):
        supabase.auth.sign_out()
        del st.session_state['user']
        st.rerun()
