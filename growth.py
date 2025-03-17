import streamlit as st  
import pandas as pd 
from io import BytesIO 

st.set_page_config(page_title="📀 Data Sweeper", layout="wide")
# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #3D8D7A;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("📀 Data Sweeper Sterling Integrator")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File Uploader
uploaded_files = st.file_uploader("Upload CSV or Excel Files:", type=["csv", "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"🔍 {file.name} - Preview")
        st.dataframe(df.head())
        #automatic fill missing value
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing value filled successfully!")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Shoe Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
            #conversion option
            format_choice = st.radio(f" 🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"Download {file.name} as {format_choice}"):
                output = BytesIO()
                if format_choice == "CSV":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = file.name.replace(ext, "csv")
                else:
                    df.to_excel(output, index=False)
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")
                output.seek(0)
                st.download_button(" Download File", file_name=new_name, data=output, mime=mime)

st.success("👏 All files processed successfully!")
