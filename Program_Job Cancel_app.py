
import streamlit as st
import pandas as pd
import io

st.title("CSV Cleaner and Filter")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Step 2: Read CSV file
    df = pd.read_csv(uploaded_file)

    # Step 3: Standardize and clean column names
    df.columns = df.columns.str.strip()

    st.write("### Original Data Preview")
    st.dataframe(df.head())

    # Step 4: Define target columns
    program_status_col = 'StandardPrice'  # CL
    program_code_col = 'ProgramCode'      # CI

    if program_status_col not in df.columns or program_code_col not in df.columns:
        st.error(f"Columns '{program_status_col}' or '{program_code_col}' not found in the uploaded CSV.")
    else:
        # Step 5: Ensure values are strings, strip whitespace, and convert to uppercase
        df[program_status_col] = df[program_status_col].astype(str).str.strip().str.upper()
        df[program_code_col] = df[program_code_col].astype(str).str.strip().str.upper()

        # Step 6: Clean and filter StandardPrice thoroughly
        df[program_status_col] = (
            df[program_status_col]
            .str.replace(r"[^\d.]", "", regex=True)     # Remove all non-digit/dot characters
            .str.replace(r"\.0*$", "", regex=True)     # Remove trailing '.0', '.00', etc.
            .str.strip()
        )

        # Convert to numeric
        df[program_status_col] = pd.to_numeric(df[program_status_col], errors='coerce')

        # Drop rows where value is 0 or NaN
        df = df[(df[program_status_col].notnull()) & (df[program_status_col] != 0)]

        # Step 7: Remove rows where ProgramCode is 'GQI'
        df = df[df[program_code_col] != 'GQI']

        st.write("### Cleaned Data Preview")
        st.dataframe(df.head())

        # Step 8: Prepare file for download
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name='filtered_program_data.csv',
            mime='text/csv',
        )
