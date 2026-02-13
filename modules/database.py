import os
import streamlit as st
from supabase import create_client, Client

# Your Supabase Credentials from the screenshot
SUPABASE_URL = "https://aombczanizdhiulwkuhf.supabase.co"
# Replace with your actual project 'anon' or 'service_role' key found in Supabase Settings
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "Deba9002043666") 

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def init_user_table():
    """Run this once to ensure your 'profiles' table exists in Supabase."""
    # You can also run this SQL in your Supabase SQL Editor:
    # CREATE TABLE profiles (id uuid REFERENCES auth.users, email text, points int DEFAULT 0);
    pass
