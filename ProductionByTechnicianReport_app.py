
import streamlit as st
import pandas as pd

st.title("CSV Data Processor")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Step 1: Filter out rows where column R is 0
    if 'R' in df.columns:
        df = df[df['R'] != 0]
    else:
        df = df[df.iloc[:, 17] != 0]

    # Step 2: Map codes in column K
    pest_codes = ['GOP', 'GPC', 'GQP', 'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
                  'GQ1', 'GQ2', 'GQ3', 'GQ4', 'IRP', 'MR1', 'MR2', 'MR3', 'MR4', 'MR5', 'MR6', 'MR7', 'MR8', 'MR9',
                  'MRO', 'MRN', 'MRD', 'RP1', 'RP2', 'RP3', 'RP4', 'RP5', 'RP6', 'RP7', 'RP8', 'RP9', 'RPD', 'RPN', 'RPO', 'PPS', 'CBA', 'GQI']

    mosq_codes = ['1TM', '1MB', '2MB', '2T', '2TM', '3MB', '3T', '3TM', '4MB', '4T', '4TM', '5MB', '5T', '5TM', '6MB', '6T', '6TM',
                  '7MB', '7T', '7TM', '8MB', '8T', '8TM', '9MB', '9T', '9TM', '10X', '10Y', '11X', '11Y', 'GME', 'GMI', 'H10',
                  'H11', 'H12', 'H13', 'H14', 'HY1', 'HY2', 'HY3', 'HY4', 'HY5', 'HY6', 'HY7', 'HY8', 'HY9', 'IHM', 'IMT', 'IOM',
                  'MSV', 'NTM', 'OM1', 'OM2', 'OM3', 'OM4', 'OM5', 'OM6', 'OM7', 'OM8', 'OM9', 'OMA', 'OMB', 'OMC', 'OMD',
                  'OME', 'OMF', 'OMG', 'OMH', 'OMI', 'OMJ', 'OTM', 'ZTM', 'GIM', 'GOM']

    turf_codes = ['GH1', 'GH2', 'GH3', 'GH4', 'GH5', 'GH6', 'GH7', 'GH8', 'GH9', 'GHA', 'GIT',
                  'GT1', 'GT2', 'GT3', 'GT4', 'GT5', 'GT6', 'GT7', 'GT8', 'GT9', 'DCE', 'LSC']

    term_codes = ['TR1', 'TR2', 'TR3', 'TR4', 'TR5', 'TR6', 'TR7', 'TR8', 'TR9', 'TRD', 'TRN', 'TRO', 'TSC', 'TSV']

    code_map = {**{code: 'Pest' for code in pest_codes},
                **{code: 'Mosq' for code in mosq_codes},
                **{code: 'Turf' for code in turf_codes},
                **{code: 'Term' for code in term_codes}}

    if 'K' in df.columns:
        df['K'] = df['K'].astype(str).str.strip().str.upper().map(code_map).fillna(df['K'])
    else:
        col_index = 10
        col_name = df.columns[col_index]
        df[col_name] = df[col_name].astype(str).str.strip().str.upper().map(code_map).fillna(df[col_name])

    st.success("Processing complete!")
    st.dataframe(df)

    # Offer download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download processed CSV", csv, "processed.csv", "text/csv")
