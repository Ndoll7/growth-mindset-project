
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="🔄 Smart File Converter & Data Cleaner", layout="wide")
st.title("🚀 Advanced File Converter & Data Cleaner")
st.write("Upload CSV or Excel files, clean data, check unique values, and convert formats easily!")

files = st.file_uploader(
    "📤 Upload CSV or Excel Files", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"📄 {file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"🧹 Remove Duplicates from {file.name}"):
            df = df.drop_duplicates()
            st.success("✅ Duplicates Removed!")
            st.dataframe(df.head())

        if st.checkbox(f"🛠️ Fill Missing Values in {file.name}"):
            numeric_columns = df.select_dtypes(include=["number"]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
            st.success("✅ Missing Values Filled with Mean!")
            st.dataframe(df.head())

        if st.checkbox(f"🔍 Show Unique Values (UV) in {file.name}"):
            unique_values = {col: df[col].nunique() for col in df.columns}
            st.write("### Unique Values per Column:")
            st.json(unique_values)

        selected_columns = st.multiselect(
            f"🗂️ Select Columns to Keep from {file.name}",
            df.columns,
            default=list(df.columns)
        )
        df = df[selected_columns]
        st.dataframe(df.head())

        format_choice = st.radio(
            f"💾 Choose format to download {file.name}:",
            ["CSV", "Excel"],
            key=file.name
        )

        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button(
                "📥 Download File",
                file_name=new_name,
                data=output,
                mime=mime
            )

        st.success("🎉 Processing Complete!")
