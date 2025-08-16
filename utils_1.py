import os
import pandas as pd
from datetime import timedelta

import warnings
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

# Time offset (5 hours, 30 minutes)
# YouTube Timestamps are in +00:00
TIME_OFFSET = timedelta(hours=5, minutes=30)

def parse_date_columns(df):
        # # Optional: parse date columns
        # for col in df.columns:
        #     if df[col].dtype == "object":
        #         try:
        #             parsed = pd.to_datetime(df[col], errors="coerce")
        #             if parsed.notna().sum() > 0:
        #                 df[col] = parsed
        #         except Exception:
        #             pass

        # # Remove timezone information from datetime columns before saving to Excel
        # for col in df.columns:
        #     if pd.api.types.is_datetime64_any_dtype(df[col]):
        #         if df[col].dt.tz is not None:
        #             df[col] = df[col].dt.tz_localize(None)
        
        return df

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

def clean_on_merge(df, search=False):
    df = parse_date_columns(df)
    df = clean_dataframe(df)
    df = format_dataframe(df, search)
    return df