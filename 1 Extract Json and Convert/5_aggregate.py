import os
from tkinter import X
import pandas as pd

def clean_and_aggregate(input_dir, file_name):
    input_path = os.path.join(input_dir, file_name)
    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        return

    df = pd.read_excel(input_path, engine='openpyxl')

    # 1. Aggregate by titleUrl
    grouped = df.groupby('titleUrl').agg({
        'title': 'first',
        'time': ['min', 'max', lambda x : len(set(x)), lambda x: set(x)],
        'header': lambda x: (
            'YouTube Music' if 'YouTube Music' in x.values
            else x.mode().iloc[0] if not x.mode().empty
            else None
        )
    }).reset_index()

    # Flatten multi-level columns
    grouped.columns = ['titleUrl', 'title', 'first_time', 'last_time', 'frequency', 'time_list', 'header']

    # Get the year counts from the original df
    df['year'] = df['time'].str[2:4]  # extract last 2 digits of year
    year_counts = df.pivot_table(index='titleUrl', columns='year', values='time', aggfunc='count').fillna(0).astype(int)
    year_counts.columns = [str(y).zfill(2) for y in year_counts.columns]  # e.g. '21', '22'

    grouped = grouped.merge(year_counts, on='titleUrl', how='left')
    
    grouped.sort_values(by='first_time', ascending=False, inplace=True)
    
    # Save output
    # output_path = os.path.splitext(input_path)[0] + '-aggregated.xlsx'
    output_path = os.path.join(input_dir, 'watch-history-aggregated.xlsx')
    grouped.to_excel(output_path, index=False, engine='openpyxl')

    print(f"\nAggregated {len(grouped)} rows into: {output_path}\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_and_aggregate(script_dir, "watch-history-joined.xlsx")
