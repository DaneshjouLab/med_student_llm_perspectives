import pandas as pd
from utils import process_csv_df, process_responses, clean_split_df


def main():
    nov_llm_use_df = process_csv_df("Medical Students' Use of LLMs_November 18, 2024_21.00.csv")

    ##Dropping columns that will not be used/reference for future code
    nov_llm_cols_drop = ['End Date', 'Recipient Email', 'Distribution Channel', 'Response Type', 'IP Address', 
                        'Duration (in seconds)', 'External Data Reference','Location Latitude', 'Location Longitude', 
                        'Response Type', 'Progress', 'Response ID', 'Recorded Date', 'Recipient Last Name', 'Recipient First Name', 
                        'List of Countries', 'What is your gender? - Prefer to self-describe - Text','How would you describe your race? - Other - Text', 
                '''DESCRIPTION: You are invited to participate in a research study evaluating medical students' perspectives and usage of AI-based language models in practice. You will be asked to answer questions about if you have used AI large language models in practice, which AI large language models you have used, how you have used AI large language models, and information about your medical school. All survey responses are captured anonymously.\n\nTIME INVOLVEMENT: Your participation will take approximately 15 minutes.\n\nRISKS AND BENEFITS: The risks associated with this study are no foreseeable risks associated with completing this survey. We cannot and do not guarantee or promise that you will receive any benefits from completing this survey. However, by completing this survey, you will be contributing to our understanding of how medical students are using large language models in medical school and clinical settings. Your decision whether or not to participate in this study will not affect your academic performance.\n\nPAYMENTS: You will not receive any payment for completing this survey.\n\nPARTICIPANT'S RIGHTS: If you have read this form and have decided to participate in this project, please understand your participation is voluntary and you have the right to withdraw your consent or discontinue participation at any time without penalty or loss of benefits to which you are otherwise entitled. The alternative is not to participate. You have the right to refuse to answer particular questions. The results of this research study may be presented at scientific or professional meetings or published in scientific journals. Your individual privacy will be maintained in all published and written data resulting from the study. All survey responses will be recorded anonymously.\n\nCONTACT INFORMATION:\nQuestions? Please contact Dr. Jenna Lester at 415-353-7800. If you have questions or concerns about your rights as a research participant, you can call the UCSF Institutional Review Board at 415-476-1814.\n\nPlease print a copy of this page for your records.\n\nIf you agree to participate in this research, please click on the "Agree" button.'''

                        ]

    nov_llm_use_df_clean = dec_llm_use_df.drop(columns=nov_llm_cols_drop)


    ##Verifying total number of people in the survey -- 118
    nov_llm_use_df_clean_118 = nov_llm_use_df_clean[nov_llm_use_df_clean['Are you a medical student?'] == 'Yes']


    ##Dropping second group of columns that include other text answers (keeping only columns that are selection based answers)
    sec_col_grp_drop = ['Do you have any concerns about AI-based language models? (Check all that apply) - Other - Text',  
                        'Which of the following large language models have you used? (Check all that apply) - Other - Text', 
                        'What have you used AI-based language models for? (Check all that apply) - Other - Text',
                        'Are you currently in the pre-clinical or clinical portion of your medical school? - Other - Text'
                        ]

    nov_llm_use_df_clean_118.drop(columns=sec_col_grp_drop)

    ##Checking / filtering for those who have completed survey

    nov_llm_use_df_clean_118_comp= nov_llm_use_df_clean_118.loc[nov_llm_use_df_clean_118['Finished'] == 'True']
    ##The suffix comp includes only "completed" survey responses in df. Non-comp includes non-complete survey responses

    # len(nov_llm_use_df_clean_118_comp)
    ##This shows how many people are in the completed survey df - 86 people have completed survey

    ##Exporting results of only those who have completed survey
    nov_llm_use_df_clean_118_comp.to_csv("nov_patient_llm_use_df_clean_complete.csv", encoding='utf-8', index=False)


    ## Renaming neither accurate nor inaccurate response
    mask = nov_llm_use_df_clean_118_comp["How accurate did you find AI-based language models?"] == "Neither accurate nor inaccurate (a number of mistakes, but still useable)"
    nov_llm_use_df_clean_118_comp.loc[mask, "How accurate did you find AI-based language models?"] = "Neither accurate nor inaccurate"

    opinion_cols_of_interest = [ 
        'Have you used a large language model (e.g., ChatGPT, Doximity GPT, Google Bard, GPT-4, Bing Chat)?',
        'How often are you using AI-based language models?',
        'How likely are you to use AI-based language models in the future?',
        'In a single output given to you by an AI-based language model, on average how many edits have you needed to make?',
        'How do you think AI-based language models are impacting your learning?',
        'Which of the following large language models have you used? (Check all that apply) - Selected Choice',
        'How accurate did you find AI-based language models?',
    ]

    demo_cols_of_interest = [ 'What type of community is your medical school in?', 
                            'Is your medical school in the U.S. / a U.S. territory?',
                            'Are you currently in the pre-clinical or clinical portion of your medical school? - Selected Choice',          
                            'What is your gender? - Selected Choice', 'Are you of Spanish, Hispanic, or Latino origin?',
                            'How would you describe your race? - Selected Choice'
                                        ]


    ##Creating smaller analysis dfs based on relevant columns (demographic based columns)
    demographics_nov_llm_use_df_clean_118_comp = nov_llm_use_df_clean_118_comp[demo_cols_of_interest]
    demographics_nov_llm_use_df_clean_118 = nov_llm_use_df_clean_118[demo_cols_of_interest]

    ##Creating smaller analysis dfs based on relevant columns (opinion based columns)
    op_nov_llm_use_df_clean_118_comp = nov_llm_use_df_clean_118_comp[opinion_cols_of_interest]
    op_nov_llm_use_df_clean_118_non_comp = nov_llm_use_df_clean_118[opinion_cols_of_interest]


    # Process the DataFrame
    # demographics_nov_clean_118_split_result_df = process_responses(demographics_nov_llm_use_df_clean_118)

    ##Process opinions on LLMs responses (both complete and incomplete survey responses)
    op_nov_comp_split_result_df = process_responses(op_nov_llm_use_df_clean_118_comp)
    op_nov_non_comp_split_result_df = process_responses(op_nov_llm_use_df_clean_118_non_comp)

    #Process demographics on LLMs responses (both complete and incomplete survey responses)
    demo_nov_comp_split_result_df = process_responses(demographics_nov_llm_use_df_clean_118_comp)
    demo_nov_non_comp_split_result_df = process_responses(demographics_nov_llm_use_df_clean_118)
    # perspective_nov_llm_use_df_clean_118_comp_split_result_df = process_responses(perspective_nov_llm_use_df_clean_118_comp)


    #Formatting opionion LLM dfs for neatness
    clean_opinion_non_comp = clean_split_df(op_nov_non_comp_split_result_df)
    clean_opinion = clean_split_df(op_nov_comp_split_result_df)


    clean_demo = clean_split_df(demo_nov_comp_split_result_df)
    clean_demo_non_comp = clean_split_df(demo_nov_non_comp_split_result_df)

    
    clean_demo_non_comp.to_csv("LLM_perspectives_data_split_non_comp_Nov.csv", encoding='utf-8', index=False)

    clean_demo.to_csv("LLM_perspectives_data_split_Nov.csv", encoding='utf-8', index=False)

    clean_opinion.to_csv("LLM_opinions_data_split_Nov_comp.csv", encoding='utf-8', index=False)

    clean_opinion_non_comp.to_csv("LLM_opinions_data_split_Nov_non_comp.csv", encoding='utf-8', index=False)

if __name__ == "__main__":
    main()













