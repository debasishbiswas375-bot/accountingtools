import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="TallyTools.in | Learn & Automate",
    page_icon="📊",
    layout="wide"
)

# 2. Custom Styling (The "Tiny Things")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Learning Hub", "Excel to Tally XML", "My Dashboard"])

# 4. Main Page Logic
if selection == "Home":
    st.title("Welcome to TallyTools.in")
    st.subheader("The AccountingCoach for Tally Users")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### 📚 Learn\nMaster debits, credits, and Tally ERP/Prime basics.")
    with col2:
        st.success("### 🛠️ Automate\nConvert your Excel data to Tally XML in seconds.")

elif selection == "Excel to Tally XML":
    st.header("Excel to Tally XML Converter")
    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])
    if uploaded_file:
        st.write("Processing file...")
        # Your xml_generator.py logic goes here
