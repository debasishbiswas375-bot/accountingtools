import streamlit as st
from supabase import create_client

# Project details
URL = "https://aombczanizdhiulwkuhf.supabase.co"
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

st.title("👤 My TallyTools Account")

if 'user' not in st.session_state:
    mode = st.radio("Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Proceed"):
        try:
            if mode == "Register":
                # Explicitly telling Supabase to send you back to the live site
                res = supabase.auth.sign_up({
                    "email": email, 
                    "password": password,
                    "options": {
                        "email_redirect_to": "https://accountingtools.streamlit.app/Account"
                    }
                })
                st.info("Check your email (including Spam) to confirm your account!")
            else:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state['user'] = res.user
                st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")
else:
    st.success(f"Logged in as {st.session_state['user'].email}")
    if st.button("Sign Out"):
        supabase.auth.sign_out()
        del st.session_state['user']
        st.rerun()
