import streamlit as st

st.title("👤 My Account")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.warning("Database connection (Supabase) required for this step.")

with tab2:
    st.write("Join 80,000+ members (AccountingCoach style!)")
    new_email = st.text_input("Register Email")
    if st.button("Create Account"):
        st.success("Account created! (Simulation)")
