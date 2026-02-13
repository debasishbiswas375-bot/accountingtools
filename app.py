import streamlit as st

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="TallyTools.in | Master Accounting",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for a clean "AccountingCoach" look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🚀 TallyTools.in")
    st.subheader("Free Accounting Education & Tally Automation")
    
    st.divider()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📖 Learn")
        st.write("Deep dive into accounting principles, just like a coach.")
        if st.button("Start Learning"):
            st.info("Navigate to 'Learning Hub' in the sidebar.")

    with col2:
        st.markdown("### 🛠️ Automate")
        st.write("Convert Excel ledgers and vouchers to Tally XML instantly.")
        if st.button("Open Converter"):
            st.info("Navigate to 'Tally XML Converter' in the sidebar.")

    with col3:
        st.markdown("### 🏆 Progress")
        st.write("Track your scores and earn certificates.")
        if st.button("View Dashboard"):
            st.info("Log in via the 'Account' section.")

if __name__ == "__main__":
    main()
