import streamlit as st
import pandas as pd

st.set_page_config(page_title="Flight Timetable Extractor", layout="wide")
st.title("🛫 Flight Timetable Extractor")

uploaded_file = st.file_uploader("Upload a Flight Timetable (Excel .xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        excel_data = pd.ExcelFile(uploaded_file)
        if 'exportData' not in excel_data.sheet_names:
            st.error("Excel file must contain a sheet named 'exportData'.")
        else:
            df = excel_data.parse('exportData')
            df_filtered = df[['Flight No.', 'Route', 'Departure Time at Org.']].copy()
            df_filtered[['Flight Date', 'Departure Time']] = df_filtered['Departure Time at Org.'].str.extract(r'(\\d{2}-\\w{3}-\\d{4}) (\\d{2}:\\d{2})')
            df_filtered['Destination'] = df_filtered['Route'].str.split('-').str[-1]
            final_df = df_filtered[['Flight Date', 'Departure Time', 'Flight No.', 'Destination']].sort_values(by='Departure Time').reset_index(drop=True)

            st.success("✅ Timetable extracted!")
            st.dataframe(final_df, use_container_width=True)

            csv = final_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download as CSV", csv, "timetable.csv", "text/csv")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload an Excel file to get started.")
