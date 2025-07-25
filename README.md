# YouTube History Insights

A Python toolkit for extracting, cleaning, and analyzing your YouTube watch history from Google Takeout exports.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Script Details](#script-details)
- [Outputs](#outputs)
- [Troubleshooting](#troubleshooting)
- [License & Disclaimer](#license--disclaimer)

---

## Overview

This project provides a streamlined workflow to process your YouTube history data exported from Google Takeout. It automates file organization, data cleaning, aggregation, and analysis, enabling you to gain insights into your viewing habits.

---

## Features

- **Automated File Processing:** Batch handling of multiple history files.
- **Data Cleaning:** Removes ads, empty entries, and irrelevant data.
- **Aggregation:** Combines duplicate videos, tracks viewing frequency, and analyzes by year.
- **Timezone Conversion:** Converts UTC timestamps to your local time.
- **Incremental Updates:** Efficiently processes only new data.
- **Flexible Output:** Generates individual and combined Excel files for analysis.

---

## Project Structure

```
youtube-history-inights/
├── 1 Extract Json and Convert/
│   ├── 1_add_prefix.py
│   ├── 2_copy_history.py
│   ├── 3_json_to_xlsx.py
│   ├── 4_merge_xlsx.py
│   └── 5_aggregate.py
└── README.md
```

---

## Setup

1. **Install Dependencies**

   ```bash
   pip install pandas openpyxl
   ```

2. **Export Your Data**

   - Download your YouTube history from [Google Takeout](https://takeout.google.com).
   - Extract the archive and place the folders in the project directory.

---

## Usage

Run the following scripts in order from the `1 Extract Json and Convert` directory:

```bash
python 1_add_prefix.py
python 2_copy_history.py
python 3_json_to_xlsx.py
python 4_merge_xlsx.py
python 5_aggregate.py
```

---

## Script Details

### 1. Add Prefixes (`1_add_prefix.py`)

Adds directory-based prefixes to files for easier identification and prevents duplicate prefixing.

### 2. Copy History Files (`2_copy_history.py`)

Finds all `history.json` files in subdirectories and copies them to the root, handling naming conflicts.

### 3. Convert JSON to Excel (`3_json_to_xlsx.py`)

Flattens and cleans JSON files, then exports them to Excel format for further processing.

### 4. Merge and Clean Excel Files (`4_merge_xlsx.py`)

Combines multiple Excel files, applies data cleaning, and converts timestamps to local time. Outputs combined watch and search history files.

- **Timezone:** Adjust `TIME_OFFSET` in the script for your local timezone.

### 5. Aggregate Data (`5_aggregate.py`)

Aggregates watch history by video, tracking frequency, first/last view, and yearly breakdown. Supports incremental updates for new data.

---

## Outputs

- `watch-history-joined.xlsx`: Combined, cleaned watch history.
- `search-history-joined.xlsx`: Combined, cleaned search history.
- `watch-history-aggregated.xlsx`: Aggregated insights (frequency, time range, yearly stats).

---

## Troubleshooting

- **File Not Found:** Ensure all history files are extracted and placed correctly.
- **Large Files:** Process in batches or increase system memory.
- **Encoding Issues:** Use UTF-8 encoding for all files.

---

## License & Disclaimer

This project is open source for personal use. Please comply with YouTube's Terms of Service and privacy policies. Use only with your own data.

---

- Converts music.youtube.com to www.youtube.com
- Applies timezone offset to timestamps
- Handles both watch-history and search-history

**Output Files**:

- `watch-history-joined.xlsx`
- `search-history-joined.xlsx`

### 5. Data Aggregation (`5_aggregate.py`)

**Purpose**: Creates comprehensive viewing insights by aggregating video data.

**Key Features**:

- **Smart Deduplication**: Combines multiple views of the same video
- **Frequency Tracking**: Counts how many times each video was watched
- **Time Range Analysis**: Tracks first and last view times
- **Yearly Breakdown**: Shows viewing patterns by year
- **Incremental Updates**: Only processes new data on subsequent runs
- **Header Classification**: Distinguishes between YouTube and YouTube Music

**Output Columns**:

- `titleUrl`: Unique video identifier
- `title`: Video title
- `first_time`: First time watched
- `last_time`: Most recent view
- `frequency`: Total number of views
- `header`: Platform (YouTube/YouTube Music)
- `time_list`: Set of all viewing timestamps
- Year columns (e.g., `21`, `22`, `23`): Views per year

## Output Files

### Primary Outputs

- **`watch-history-joined.xlsx`**: Combined raw watch history
- **`watch-history-aggregated.xlsx`**: Aggregated insights with viewing statistics
- **`search-history-joined.xlsx`**: Combined search history

### Intermediate Files

- Individual Excel files for each JSON input
- Temporary processing files (automatically cleaned)

## Advanced Usage

### Timezone Configuration

Modify the `TIME_OFFSET` in `4_merge_xlsx.py`:

```python
# For different timezones
TIME_OFFSET = timedelta(hours=8)  # UTC+8
TIME_OFFSET = timedelta(hours=-5) # UTC-5 (EST)
```

### Processing Only New Data

The aggregation script automatically detects existing data and processes only new entries, making it efficient for regular updates.

### Custom Filtering

Modify the cleaning functions in `4_merge_xlsx.py` to add custom filters:

```python
# Add custom filtering logic
df = df[~df['title'].str.contains('specific_pattern', na=False)]
```

## Data Analysis Ideas

With the generated Excel files, you can analyze:

- **Viewing Patterns**: Most watched videos and channels
- **Time Analysis**: Viewing habits by time of day/year
- **Content Preferences**: Music vs. regular videos
- **Binge Watching**: Videos watched multiple times
- **Historical Trends**: How your preferences changed over time

## Troubleshooting

### Common Issues

1. **File Not Found Errors**

   - Ensure all history.json files are properly extracted
   - Check that directory structure matches expected format

2. **Memory Issues with Large Files**

   - Process files in smaller batches
   - Consider increasing available RAM

3. **Encoding Issues**
   - Ensure files are UTF-8 encoded
   - Check for special characters in file names

### Performance Tips

- Run scripts on SSD storage for faster I/O
- Close other Excel applications before processing
- For very large datasets, consider processing in chunks

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the toolkit.

## License

This project is open source. Please respect YouTube's Terms of Service when using this tool with your own data.
