import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from dashboard import show_dashboard  # Assuming dashboard.py exists
from utils_1 import clean_on_merge

# Set wide layout
st.set_page_config(page_title="JSON & Excel Processor", layout="wide")

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.title("JSON & Excel Processor & Viewer with Dashboard")

# Upload multiple JSON or Excel files
uploaded_files = st.file_uploader(
    "Upload JSON or Excel files",
    type=["json", "xlsx", "xls"],
    accept_multiple_files=True
)

# Process button
if st.button("Process Data") and uploaded_files:
    all_data = []

    for file in uploaded_files:
        try:
            if file.name.lower().endswith(".json"):
                data = json.load(file)
                if isinstance(data, dict):
                    df = pd.DataFrame([data])
                elif isinstance(data, list):
                    df = pd.DataFrame(data)
                else:
                    st.warning(f"Skipping file {file.name}: Unsupported JSON structure")
                    continue
            else:  # Excel
                df = pd.read_excel(file)

            all_data.append(df)

        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = clean_on_merge(final_df)
            
        output_path = os.path.join(OUTPUT_DIR, f"1_processed.xlsx")
        final_df.to_excel(output_path, index=False)
        st.success(f"Combined Excel saved: {output_path}")

# Always show output files
st.subheader("Available Output Files")
output_files = sorted(
    [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith(".xlsx")],
    reverse=True
)

if output_files:
    selected_file = st.selectbox("Select file to view", output_files)
    file_path = os.path.join(OUTPUT_DIR, selected_file)

    try:
        df_view = pd.read_excel(file_path)

        # Auto-parse potential date columns
        for col in df_view.columns:
            if df_view[col].dtype == "object":
                try:
                    parsed = pd.to_datetime(df_view[col], errors="coerce")
                    if parsed.notna().sum() > 0:
                        df_view[col] = parsed
                except Exception:
                    pass

        # Remove timezone information from datetime columns for display
        for col in df_view.columns:
            if pd.api.types.is_datetime64_any_dtype(df_view[col]):
                if df_view[col].dt.tz is not None:
                    df_view[col] = df_view[col].dt.tz_localize(None)

        st.dataframe(df_view, use_container_width=True, height=700)

        # Show dashboard below
        show_dashboard(df_view)

    except Exception as e:
        st.error(f"Error reading {selected_file}: {e}")

    # Download button
    with open(file_path, "rb") as f:
        st.download_button(
            label=f"Download {selected_file}",
            data=f,
            file_name=selected_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No Excel output files found yet.")
