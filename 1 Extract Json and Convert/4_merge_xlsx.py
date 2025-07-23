import os
import pandas as pd
from datetime import timedelta

import warnings
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

# Time offset (5 hours, 30 minutes)
# YouTube Timestamps are in +00:00
TIME_OFFSET = timedelta(hours=5, minutes=30)

def clean_dataframe(df):

    # 1. Remove rows where 'name' or 'name.1' contains "Google Ads"
    for col in ['name', 'name.1']:
        if col in df.columns:
            df = df[~df[col].str.contains('Google Ads', na=False)]

    # 2. Remove rows where 'titleUrl' is empty or null
    df = df[df['titleUrl'].notna() & (df['titleUrl'].str.strip() != '')]

    # 3. Remove rows where 'titleUrl' contains 'www.google.com'
    df = df[~df['titleUrl'].str.contains('www.google.com', na=False)]

    # 4. Drop 'subtitles' and 'name.1' if both exist and are fully empty
    empty_cols = []
    for col in ['subtitles', 'name.1', 'description']:
        if col in df.columns and df[col].isna().all():
            empty_cols.append(col)
    if empty_cols:
        df.drop(columns=empty_cols, inplace=True)
    
    return df

def format_dataframe(df, search=False):
    
    # 1. Replace "//music." with "//www." in title and titleUrl
    df['title'] = df['title'].str.replace('//music.', '//www.', regex=False)
    df['titleUrl'] = df['titleUrl'].str.replace('//music.', '//www.', regex=False)

    # 2. Drop rows where name is "From Google Ads"
    df = df[df['name'] != 'From Google Ads']

    # 3. Remove starting "Watched " from title
    df['title'] = df['title'].str.removeprefix('Watched ')

    if search:
        df['title'] = df['title'].str.removeprefix('Searched for ')
        df.drop(columns=[col for col in ['titleUrl', 'name', 'description'] if col in df.columns], inplace=True)

    # 4. Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'].str.slice(0, 19), format='%Y-%m-%dT%H:%M:%S', errors='coerce') + TIME_OFFSET
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df

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

        if type == 'watch-history':
            combined_df = clean_dataframe(combined_df)
        combined_df = format_dataframe(combined_df, search=(type == 'search-history'))
        combined_df.sort_values(by='time', ascending=False, inplace=True)
    
        combined_df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\nCombined {len(all_dfs)} files into: {output_file}\n")
    else:
        print("No valid .xlsx files found to combine.")

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    combine_xlsx_files_to_one(root, 'watch-history')
    combine_xlsx_files_to_one(root, 'search-history')
