import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

# --- HELPER FUNCTIONS ---
def format_xml(elem):
    """Adds indentation to the XML for readability."""
    from xml.dom import minidom
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_tally_xml(df):
    # Root Element
    envelope = ET.Element("ENVELOPE")
    
    # Header Section
    header = ET.SubElement(envelope, "HEADER")
    ET.SubElement(header, "TALLYREQUEST").text = "Import Data"
    
    # Body Section
    body = ET.SubElement(envelope, "BODY")
    import_data = ET.SubElement(body, "IMPORTDATA")
    
    req_desc = ET.SubElement(import_data, "REQUESTDESC")
    ET.SubElement(req_desc, "REPORTNAME").text = "Vouchers"
    
    req_data = ET.SubElement(import_data, "REQUESTDATA")
    
    for _, row in df.iterrows():
        tally_msg = ET.SubElement(req_data, "TALLYMESSAGE", {"xmlns:UDF": "TallyUDF"})
        
        # Voucher Setup
        vch = ET.SubElement(tally_msg, "VOUCHER", VCHTYPE=str(row['Voucher Type']), ACTION="Create")
        
        # Convert date to Tally format (YYYYMMDD)
        vch_date = pd.to_datetime(row['Date']).strftime('%Y%m%d')
        ET.SubElement(vch, "DATE").text = vch_date
        ET.SubElement(vch, "VOUCHERNUMBER").text = str(row['Voucher No'])
        ET.SubElement(vch, "NARRATION").text = str(row['Narration'])
        
        # Ledger Entry
        all_ledger = ET.SubElement(vch, "ALLLEDGERENTRIES.LIST")
        ET.SubElement(all_ledger, "LEDGERNAME").text = str(row['Ledger Name'])
        ET.SubElement(all_ledger, "ISDEEMEDPOSITIVE").text = "Yes" if row['Amount'] > 0 else "No"
        ET.SubElement(all_ledger, "AMOUNT").text = str(row['Amount'])

    return format_xml(envelope)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Converter | TallyTools", layout="wide")
st.title("🛠️ Professional Excel to Tally XML")

st.markdown("""
### Instructions:
1. Download the **[Sample Template](https://your-link-here.com)**.
2. Fill in your accounting data.
3. Upload and convert.
""")

uploaded_file = st.file_uploader("Upload your transaction Excel", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        
        with st.expander("Preview Data"):
            st.dataframe(df)

        if st.button("Generate XML for Tally"):
            xml_output = create_tally_xml(df)
            
            st.download_button(
                label="📥 Download .XML File",
                data=xml_output,
                file_name=f"Tally_Import_{datetime.now().strftime('%Y%m%d')}.xml",
                mime="application/xml"
            )
            st.balloons()
            
    except Exception as e:
        st.error(f"Error processing file: {e}")
