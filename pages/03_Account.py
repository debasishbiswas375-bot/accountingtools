import streamlit as st
from supabase import create_client

# Project Details
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

st.title("👤 My TallyTools Account")

# 1. AUTHENTICATION UI
if 'user' not in st.session_state:
    mode = st.radio("Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Proceed"):
        try:
            if mode == "Register":
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.info("Check your email (including Spam) to confirm!")
            else:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['user'] = res.user
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# 2. LOGGED-IN DASHBOARD
else:
    user = st.session_state['user']
    st.success(f"Welcome, {user.email}")
    
    # Safety Check: Try to fetch profile, but don't crash if table is missing
    try:
        profile = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        if profile.data:
            col1, col2 = st.columns(2)
            col1.metric("Credits", f"{profile.data['points']} pts")
            col2.metric("Rank", profile.data['rank'])
    except Exception:
        st.warning("Profile data not found. Ensure you ran the SQL script in Supabase Editor.")

    if st.button("Sign Out"):
        supabase.auth.sign_out()
        del st.session_state['user']
        st.rerun()
