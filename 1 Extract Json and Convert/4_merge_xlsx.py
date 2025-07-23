import os
import pandas as pd

def combine_xlsx_files_to_one(directory, type, output_suffix='joined'):
    output_file = os.path.join(directory, f'{type}-{output_suffix}.xlsx')
    all_dfs = []

    for filename in os.listdir(directory):
        if filename.lower().endswith(f'{type}.xlsx') and filename != os.path.basename(output_file):
            filepath = os.path.join(directory, filename)
            if not os.path.isfile(filepath):
                continue
            print(f"Reading: {filename}")
            try:
                df = pd.read_excel(filepath, engine='openpyxl')
                all_dfs.append(df)
            except Exception as e:
                print(f"Skipping {filename} due to error: {e}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)

        if 'time' in combined_df.columns:
            combined_df.sort_values(by='time', ascending=False, inplace=True)
    
        combined_df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\nCombined {len(all_dfs)} files into: {output_file}\n")
    else:
        print("No valid .xlsx files found to combine.")

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    combine_xlsx_files_to_one(root, 'watch-history')
    combine_xlsx_files_to_one(root, 'search-history')
