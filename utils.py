"""Utility functions for processing survey CSV files and responses.

Helper functions to read CSV files, process survey responses, and clean DataFrame results.
"""

import pandas as pd


def process_csv_df(csv_path):
    """Read a CSV file and return a processed DataFrame.

    Parameters:
        csv_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The processed DataFrame with the first row removed.
    """
    df = pd.read_csv(csv_path, index_col=0, header=1)
    df = df[1:]
    return df


def process_responses(df):
    """Process survey responses in a DataFrame and return a summary DataFrame.

    For each column, the function counts responses (splitting comma-separated
    values) and calculates the percentage of each response.

    Parameters:
        df (pd.DataFrame): DataFrame containing survey responses.

    Returns:
        pd.DataFrame: A DataFrame summarizing responses with counts and percentages.
    """
    results = []

    for column in df.columns:
        counts = {}
        # Process each row in the column.
        for _, row in df.iterrows():
            value = row[column]
            if isinstance(value, str):
                responses = value.split(',') if ',' in value else [value]
                for response in responses:
                    response = response.strip()  # Clean up whitespace.
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
    """Clean the split DataFrame by ensuring the question is only shown once per group.

    For each unique question in the 'Question' column, the first row retains
    the question name while subsequent rows have an empty string.

    Parameters:
        df (pd.DataFrame): DataFrame with a 'Question' column.

    Returns:
        pd.DataFrame: A cleaned DataFrame with formatted question groups.
    """
    split_result_rows = []

    # Loop through each unique question.
    for col in df['Question'].unique():
        group = df[df['Question'] == col]
        # Add the first row with the question name.
        first_row = group.iloc[0].copy()
        split_result_rows.append(first_row)
        # Add subsequent rows without repeating the question.
        for idx in range(1, len(group)):
            row = group.iloc[idx].copy()
            row['Question'] = ''  # Clear the question for subsequent rows.
            split_result_rows.append(row)

    return pd.DataFrame(split_result_rows)
