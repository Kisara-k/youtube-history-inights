import os
import pandas as pd
import ast

def clean_and_aggregate(input_dir, file_name, get_year_counts=True):

    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(input_dir, 'watch-history-aggregated.xlsx')

    if not os.path.isfile(input_path):
        print(f"File not found: {input_path}")
        return

    # Read the data
    df = pd.read_excel(input_path, engine='openpyxl')
    
    # Check if aggregate file exists
    
    if os.path.isfile(output_path):
        # Read existing aggregated data
        existing_agg = pd.read_excel(output_path, engine='openpyxl')
        
        # Safely convert string representation of time_list back to set
        existing_agg['time_list'] = existing_agg['time_list'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        
        # Get all unique timestamps from existing data
        existing_times = set()
        for times in existing_agg['time_list']:
            existing_times.update(times)
        
        # Filter df to only include rows with new timestamps
        df = df[~df['time'].isin(existing_times)]
        
        if len(df) == 0:
            print("\nNo new entries found to update. Aggregate file remains unchanged.\n")
            return
        
        # Create mapping of titleUrl to header from existing aggregate
        header_mapping = existing_agg.set_index('titleUrl')['header'].to_dict()
        mask = df['titleUrl'].isin(header_mapping.keys())
        df.loc[mask, 'header'] = df.loc[mask, 'titleUrl'].map(header_mapping)
        
        # Prepare existing data for merging by exploding time_list
        existing_data = existing_agg.explode('time_list').rename(columns={'time_list': 'time'})
        existing_data = existing_data[['titleUrl', 'title', 'time', 'header']]  # Keep only necessary columns
        
        # Combine with existing data for re-aggregation
        df = pd.concat([existing_data, df], ignore_index=True)

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
    if get_year_counts:
        df['year'] = df['time'].str[2:4]  # extract last 2 digits of year
        year_counts = df.pivot_table(index='titleUrl', columns='year', values='time', aggfunc='count').fillna(0).astype(int)
        year_counts.columns = [str(y).zfill(2) for y in year_counts.columns]  # e.g. '21', '22'

    grouped = grouped.merge(year_counts, on='titleUrl', how='left')
    
    grouped.sort_values(by='first_time', ascending=False, inplace=True)
    
    # Save output
    grouped.to_excel(output_path, index=False, engine='openpyxl')

    print(f"\nAggregated {len(grouped)} rows into: {output_path}\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_and_aggregate(script_dir, "watch-history-joined.xlsx")
