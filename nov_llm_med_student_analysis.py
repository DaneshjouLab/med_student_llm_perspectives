"""Module for processing medical student LLM survey analysis.

"""

from utils import process_csv_df, process_responses, clean_split_df


def drop_unused_columns(df):
    """Drop columns that are not needed for further analysis."""
    cols_to_drop = [
        'End Date',
        'Recipient Email',
        'Distribution Channel',
        'Response Type',
        'IP Address',
        'Duration (in seconds)',
        'External Data Reference',
        'Location Latitude',
        'Location Longitude',
        'Response Type',
        'Progress',
        'Response ID',
        'Recorded Date',
        'Recipient Last Name',
        'Recipient First Name',
        'List of Countries',
        "What is your gender? - Prefer to self-describe - Text",
        "How would you describe your race? - Other - Text",
        (
            "DESCRIPTION: You are invited to participate in a research study evaluating "
            "medical students' perspectives and usage of AI-based language models in "
            "practice. You will be asked to answer questions about if you have used AI "
            "large language models in practice, which AI large language models you have used, "
            "how you have used AI large language models, and information about your medical "
            "school. All survey responses are captured anonymously.\n\nTIME INVOLVEMENT: "
            "Your participation will take approximately 15 minutes.\n\nRISKS AND BENEFITS: "
            "The risks associated with this study are no foreseeable risks associated with "
            "completing this survey. We cannot and do not guarantee or promise that you will "
            "receive any benefits from completing this survey. However, by completing this survey, "
            "you will be contributing to our understanding of how medical students are using "
            "large language models in medical school and clinical settings. Your decision whether "
            "or not to participate in this study will not affect your academic performance.\n\n"
            "PAYMENTS: You will not receive any payment for completing this survey.\n\n"
            "PARTICIPANT'S RIGHTS: If you have read this form and have decided to participate in this "
            "project, please understand your participation is voluntary and you have the right to withdraw "
            "your consent or discontinue participation at any time without penalty or loss of benefits to "
            "which you are otherwise entitled. The alternative is not to participate. You have the right to "
            "refuse to answer particular questions. The results of this research study may be presented at "
            "scientific or professional meetings or published in scientific journals. Your individual "
            "privacy will be maintained in all published and written data resulting from the study. All survey "
            "responses will be recorded anonymously.\n\nCONTACT INFORMATION:\nQuestions? Please contact Dr. Jenna Lester "
            "at 415-353-7800. If you have questions or concerns about your rights as a research participant, you can "
            "call the UCSF Institutional Review Board at 415-476-1814.\n\nPlease print a copy of this page for your "
            "records.\n\nIf you agree to participate in this research, please click on the \"Agree\" button."
        ),
    ]
    return df.drop(columns=cols_to_drop)


def filter_medical_students(df):
    """Return only rows where the respondent is a medical student."""
    return df[df['Are you a medical student?'] == 'Yes']


def drop_text_columns(df):
    """Drop columns that contain text answers, keeping only selection-based answers."""
    text_cols = [
        'Do you have any concerns about AI-based language models? (Check all that apply) - Other - Text',
        'Which of the following large language models have you used? (Check all that apply) - Other - Text',
        'What have you used AI-based language models for? (Check all that apply) - Other - Text',
        'Are you currently in the pre-clinical or clinical portion of your medical school? - Other - Text'
    ]
    df.drop(columns=text_cols, inplace=True)
    return df


def filter_completed(df):
    """Return only rows where the survey was finished."""
    return df.loc[df['Finished'] == 'True']


def rename_response_values(df):
    """Rename specific response values for clarity."""
    mask = (
        df["How accurate did you find AI-based language models?"]
        == "Neither accurate nor inaccurate (a number of mistakes, but still useable)"
    )
    df.loc[mask, "How accurate did you find AI-based language models?"] = (
        "Neither accurate nor inaccurate"
    )
    return df


def process_and_export(df, cols, filename):
    """Process responses, clean the resulting dataframe, and export to CSV."""
    processed = process_responses(df[cols])
    cleaned = clean_split_df(processed)
    cleaned.to_csv(filename, encoding='utf-8', index=False)


def main():
    """Process survey data and export cleaned CSV files."""
    # Read and clean CSV data
    raw_df = process_csv_df("Medical Students' Use of LLMs_November 18, 2024_21.00.csv")
    df_clean = drop_unused_columns(raw_df)
    df_med = filter_medical_students(df_clean)
    df_med = drop_text_columns(df_med)

    # Filter completed responses
    df_completed = filter_completed(df_med)
    df_completed = rename_response_values(df_completed)

    # Export complete survey responses
    df_completed.to_csv(
        "nov_patient_llm_use_df_clean_complete.csv", encoding='utf-8', index=False
    )

    # Define columns of interest
    opinion_cols = [
        'Have you used a large language model (e.g., ChatGPT, Doximity GPT, '
        'Google Bard, GPT-4, Bing Chat)?',
        'How often are you using AI-based language models?',
        'How likely are you to use AI-based language models in the future?',
        'In a single output given to you by an AI-based language model, on average '
        'how many edits have you needed to make?',
        'How do you think AI-based language models are impacting your learning?',
        'Which of the following large language models have you used? (Check all that apply) - Selected Choice',
        'How accurate did you find AI-based language models?'
    ]
    demo_cols = [
        'What type of community is your medical school in?',
        'Is your medical school in the U.S. / a U.S. territory?',
        'Are you currently in the pre-clinical or clinical portion of your medical school? - Selected Choice',
        'What is your gender? - Selected Choice',
        'Are you of Spanish, Hispanic, or Latino origin?',
        'How would you describe your race? - Selected Choice'
    ]

    # Process and export opinion data
    process_and_export(
        df_completed, opinion_cols, "LLM_opinions_data_split_Nov_comp.csv"
    )
    process_and_export(
        df_med, opinion_cols, "LLM_opinions_data_split_Nov_non_comp.csv"
    )

    # Process and export demographic data
    process_and_export(
        df_completed, demo_cols, "LLM_perspectives_data_split_Nov.csv"
    )
    process_and_export(
        df_med, demo_cols, "LLM_perspectives_data_split_non_comp_Nov.csv"
    )


if __name__ == "__main__":
    main()
