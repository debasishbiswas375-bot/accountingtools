import streamlit as st
from supabase import create_client

# Constants
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets.get("SUPABASE_KEY", "YOUR_ANON_KEY") # Set this in Streamlit Secrets
supabase = create_client(URL, KEY)

st.title("👤 My TallyTools Account")

if 'user' not in st.session_state:
    mode = st.radio("Choose Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Sign In"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['user'] = res.user
                st.success("Successfully logged in!")
                st.rerun()
            except Exception as e:
                st.error("Login failed. Please check your credentials.")

    else:
        if st.button("Create Account"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.info("Check your email for a confirmation link!")
            except Exception as e:
                st.error(f"Registration error: {e}")

else:
    # --- LOGGED IN DASHBOARD ---
    user = st.session_state['user']
    st.subheader(f"Welcome, {user.email}")
    
    # Progress Display (AccountingCoach Style)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Points", "150", "+25")
        st.write("Current Rank: **Junior Bookkeeper**")
    
    with col2:
        st.write("### 🏅 Achievements")
        st.caption("✅ First XML Conversion")
        st.caption("✅ Basics Quiz Passed")

    if st.button("Logout"):
        supabase.auth.sign_out()
        del st.session_state['user']
        st.rerun()
