import pandas as pd
import numpy as np
import functools as ft

def process_csv_df(csv):
    df = pd.read_csv(csv, index_col=0, header=1)
    df = df[1:]
    return df

def process_responses(df):
    results = []
    
    for column in df.columns:
        counts = {}
        # Process each row in the column
        for _, row in df.iterrows():
            value = row[column]
            if isinstance(value, str):
                responses = value.split(',') if ',' in value else [value]
                for response in responses:
                    response = response.strip()  # Clean up whitespace
                    counts[response] = counts.get(response, 0) + 1
        
        total_responses = sum(counts.values())
        
        for response, count in counts.items():
            percentage = (count / total_responses) * 100
            results.append({
                'Question': column,
                'Response': response,
                'Count': count,
                'Total Responses': total_responses,
                'Percentage': f"{percentage:.2f}%"
            })
    
    return pd.DataFrame(results)

def clean_split_df(df):
    split_result_rows = []

    # Loop through each unique question
    for col in df['Question'].unique():
        group = df[df['Question'] == col]
        
        # Add the first row with the question name
        first_row = group.iloc[0].copy()
        split_result_rows.append(first_row)
        
        # Add subsequent rows without repeating the question
        for idx in range(1, len(group)):
            row = group.iloc[idx].copy()
            row['Question'] = ''  # Clear the column name for subsequent rows
            split_result_rows.append(row)

    # Create a new DataFrame from the processed rows
    split_result_df = pd.DataFrame(split_result_rows)
    return split_result_df
