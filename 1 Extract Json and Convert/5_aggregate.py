import os
import pandas as pd

def clean_and_aggregate(input_path):
    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        return

    df = pd.read_excel(input_path, engine='openpyxl')

    # 1. Replace "//music." with "//www." in title and titleUrl
    df['title'] = df['title'].str.replace('//music.', '//www.', regex=False)
    df['titleUrl'] = df['titleUrl'].str.replace('//music.', '//www.', regex=False)

    # 2. Drop rows where name is "From Google Ads"
    df = df[df['name'] != 'From Google Ads']

    # 3. Remove starting "Watched " from title
    df['title'] = df['title'].str.removeprefix('Watched ')

    # 4. Convert time column to datetime
    df['time'] = pd.to_datetime(df['time'].str.slice(0, 19), format='%Y-%m-%dT%H:%M:%S', errors='coerce')

    # 5. Aggregate by titleUrl
    grouped = df.groupby('titleUrl').agg({
        'title': 'first',
        'time': ['min', 'max', 'count'],
        'header': lambda x: (
            'YouTube Music' if 'YouTube Music' in x.values
            else x.mode().iloc[0] if not x.mode().empty
            else None
        )
    }).reset_index()

    # Flatten multi-level columns
    grouped.columns = ['titleUrl', 'title', 'time', 'last_time', 'frequency', 'header']
    
    grouped.sort_values(by='time', ascending=False, inplace=True)
    for col in ['time', 'last_time']:
        grouped[col] = grouped[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Save output
    output_path = os.path.splitext(input_path)[0] + '-aggregated.xlsx'
    grouped.to_excel(output_path, index=False, engine='openpyxl')

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_and_aggregate(os.path.join(script_dir, "watch-history-joined.xlsx"))
