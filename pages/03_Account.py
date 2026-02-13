import streamlit as st
from supabase import create_client, Client

# 1. Setup Credentials
# Use the 'Project URL' from your project settings and the 'Publishable key' from your screenshot
URL = "https://aombczanizdhiulwkuhf.supabase.co"

# It's best to put this in Streamlit Secrets, but for testing you can paste it here:
KEY = st.secrets.get("SUPABASE_KEY", "sb_publishable_4B_eNTDDXmA8LQA8OxFEbw_77NGYbBL")

# 2. Initialize Connection with Error Handling
@st.cache_resource
def init_connection():
    try:
        return create_client(URL, KEY)
    except Exception as e:
        st.error(f"Failed to create Supabase client: {e}")
        return None

supabase = init_connection()

st.title("👤 My TallyTools Account")

# Stop the app if connection failed
if not supabase:
    st.warning("Please configure your SUPABASE_KEY in Streamlit Secrets to continue.")
    st.stop()

# 3. User Interface Logic
if 'user' not in st.session_state:
    mode = st.radio("Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Sign In"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['user'] = res.user
                st.success("Welcome back!")
                st.rerun()
            except Exception as e:
                st.error("Invalid email or password.")

    else:
        if st.button("Create Account"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.info("Success! Check your inbox for a confirmation email.")
            except Exception as e:
                st.error(f"Registration failed: {e}")

else:
    # Dashboard for logged in users
    user = st.session_state['user']
    st.subheader(f"Hello, {user.email}")
    
    st.info("You are now part of the TallyTools community. Start learning to earn points!")
    
    if st.button("Logout"):
        supabase.auth.sign_out()
        del st.session_state['user']
        st.rerun()
