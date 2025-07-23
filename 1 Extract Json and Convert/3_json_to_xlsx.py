import os
import json
import pandas as pd
from pandas import json_normalize

REMOVE_COLUMNS = {"products", "activityControls"}

def simplify_column_names(columns):
    """Keep only the lowest-level key from dot-separated column names."""
    return [col.split('.')[-1] for col in columns]

def preprocess_json(obj):
    """
    Recursively walk through the object.
    - Convert list of one element to the element itself.
    """
    if isinstance(obj, list):
        if len(obj) == 1:
            return preprocess_json(obj[0])
        return [preprocess_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: preprocess_json(v) for k, v in obj.items()}
    else:
        return obj

def flatten_json_to_dataframe(json_data):
    """Flatten nested JSON into a pandas DataFrame with simplified columns."""
    json_data = preprocess_json(json_data)

    if isinstance(json_data, dict):
        data_to_normalize = [json_data]
    elif isinstance(json_data, list):
        data_to_normalize = json_data
    else:
        raise ValueError("Unsupported JSON format: must be a dict or list")

    df = json_normalize(data_to_normalize)

    # Simplify column names
    df.columns = simplify_column_names(df.columns)

    # Drop unwanted columns if present
    columns_to_drop = [col for col in df.columns if col in REMOVE_COLUMNS]
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    return df

def convert_json_files_in_dir(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.json'):
            base_name = os.path.splitext(filename)[0]
            print(f"Processing: {filename}")

            try:
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)

                df = flatten_json_to_dataframe(data)

                tsv_path = os.path.join(directory, f"{base_name}.tsv")
                # df.to_csv(tsv_path, sep='\t', index=False)

                xlsx_path = os.path.join(directory, f"{base_name}.xlsx")
                df.to_excel(xlsx_path, index=False, engine='openpyxl')

                print(f"Saved: {tsv_path} and {xlsx_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    convert_json_files_in_dir(root)
