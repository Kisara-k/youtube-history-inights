import os
import pandas as pd

def clean_and_aggregate(input_path):
    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        return

    df = pd.read_excel(input_path, engine='openpyxl')

    # 1. Aggregate by titleUrl
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
    grouped.columns = ['titleUrl', 'title', 'first_time', 'last_time', 'frequency', 'header']
    
    grouped.sort_values(by='first_time', ascending=False, inplace=True)
    
    # Save output
    output_path = os.path.splitext(input_path)[0] + '-aggregated.xlsx'
    grouped.to_excel(output_path, index=False, engine='openpyxl')

    print(f"\nAggregated {len(grouped)} rows into: {output_path}\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_and_aggregate(os.path.join(script_dir, "watch-history-joined.xlsx"))
