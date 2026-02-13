import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO

def generate_tally_xml(df):
    # Simplified Tally XML Logic
    envelope = ET.Element("ENVELOPE")
    header = ET.SubElement(envelope, "HEADER")
    ET.SubElement(header, "TALLYREQUEST").text = "Import Data"
    
    body = ET.SubElement(envelope, "BODY")
    import_data = ET.SubElement(body, "IMPORTDATA")
    request_desc = ET.SubElement(import_data, "REQUESTDESC")
    ET.SubElement(request_desc, "REPORTNAME").text = "All Masters"
    
    request_data = ET.SubElement(import_data, "REQUESTDATA")
    
    for _, row in df.iterrows():
        tally_msg = ET.SubElement(request_data, "TALLYMESSAGE")
        ledger = ET.SubElement(tally_msg, "LEDGER", NAME=str(row['Ledger Name']))
        ET.SubElement(ledger, "PARENT").text = str(row['Group'])
        ET.SubElement(ledger, "OPENINGBALANCE").text = str(row['Amount'])

    return ET.tostring(envelope, encoding='utf-8')

st.title("🛠️ Excel to Tally XML")
st.write("Upload an Excel file with columns: **Ledger Name**, **Group**, **Amount**")

uploaded_file = st.file_uploader("Choose Excel File", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Preview of data:", df.head())
    
    if st.button("Generate Tally XML"):
        xml_data = generate_tally_xml(df)
        st.download_button(
            label="📥 Download Tally XML",
            data=xml_data,
            file_name="tally_import.xml",
            mime="application/xml"
        )
