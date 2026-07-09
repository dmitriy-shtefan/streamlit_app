import pandas as pd
import streamlit as st


st.title("Simple Data Viewer")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Data Summary")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:
        st.subheader("Chart")
        selected_column = st.selectbox("Choose a numeric column", numeric_columns)
        st.line_chart(df[selected_column])
    else:
        st.info("No numeric columns found for charting.")
else:
    st.info("Please upload a CSV file.")
