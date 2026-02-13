import streamlit as st
from supabase import create_client, Client

# Use your existing Supabase details
url: str = "https://your-project-url.supabase.co"
key: str = "your-anon-key" 
supabase: Client = create_client(url, key)

def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response
    except Exception as e:
        st.error(f"Login failed: {e}")

# Add this to your Account page UI
if st.button("Login"):
    user = login_user(email, password)
    if user:
        st.success("Logged in successfully!")
        st.session_state['user'] = user
