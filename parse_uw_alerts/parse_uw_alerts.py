"""
Function to parse UW Alerts text data and extract 
key incident information in a tabular format.
"""
import io
import time
import re
import pandas as pd
import openai
# from transformers import GPT2Tokenizer

def prompt_gpt(lines, alert_start, alert_end):
    """
    Arguments:
        lines - lines of text from .readlines output.
        alert_start - start row of a UW alert mesage chunk.
        alert_end - end row of a UW alert mesage chunk.
    Returns:
        A Pandas dataframe containing a structured 
        table from the UW alert message chunk.
    Exceptions:
        lines must be a list of length at least 1.
        alert_start/end must be integers >= 0.
        alert_end must not exceed length of lines.
    """
    if len(lines) < 1:
        raise ValueError("lines must be at least length 1")
    if alert_start < 0 or alert_end < 0:
        raise ValueError("alert_start/end must be 0 or greater")
    if alert_end > len(lines):
        raise ValueError(
            "alert_end cannot be greater than the length of lines")
    print((alert_start, alert_end))
    gpt_task = ('Extract a table with date, report time, incident'
                ' time, location, incident category, and summarized'
                ' alert message from the alert messages below.\n'
                'Text: """')
    alert_chunk = '\n'.join(lines[alert_start:alert_end])
    gpt_prompt = ''.join([gpt_task, alert_chunk])
    gpt_prompt += '\n"""'
    # tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    # n_tokens = len(tokenizer(gpt_prompt)['input_ids'])
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=gpt_prompt,
        temperature=0,
        max_tokens=3200)
    gpt_lines = io.StringIO(response['choices'][0]['text']).readlines()
    for i, line in enumerate(gpt_lines):
        if line.startswith('Date'):
            start_line = i
    gpt_output = ''.join(gpt_lines[start_line:])
    time.sleep(10)
    return pd.read_table(io.StringIO(gpt_output), sep='|')

def parse_txt_data(filepath):
    """
    Arguments:
        filepath - path to .txt file containing historial UW Alerts blogposts.
    Returns:
        A Pandas dataframe where each row is a blogpost, and there are
        columns containing the post date, post time, incident time, location,
        incident category, the summarized UW Alert message.
    Exceptions:
        filepath must be a string with .txt extension.
        Invalid inputs throw ValueError exceptions.
    """
    if not isinstance(filepath, str):
        raise ValueError("filepath must be a string")
    if re.search(r'\.txt$', filepath) is None:
        raise ValueError("filepath must have a .txt extension")

    clean_data = None
    with open(filepath, encoding='UTF-8') as file:
        lines = file.readlines()
        alert_chunk_start = None
        alert_chunk_end = None
        for i, line in enumerate(lines):
            if i == len(lines) - 1:
                table = prompt_gpt(lines, alert_chunk_start, i)
                clean_data = pd.concat([clean_data, table], ignore_index=True)
            date_check = re.search(r'^[A-z]+\s\d{1,2},\s\d{4}\n$', line)
            if date_check:
                if alert_chunk_start is None:
                    alert_chunk_start = i
                else:
                    alert_chunk_end = i
                    table = prompt_gpt(
                        lines, alert_chunk_start, alert_chunk_end)
                    clean_data = pd.concat(
                        [clean_data, table], ignore_index=True)
                    alert_chunk_start = i
    return clean_data

if __name__ == "__main__":
    OPENAI_API_KEY =  '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'
    FILEPATH = './data/UW_Alerts_2018_2022.txt'
    OUT_FILEPATH = './data/uw_alerts_clean.csv'
    openai.api_key = OPENAI_API_KEY
    text_dataframe = parse_txt_data(FILEPATH)
    text_dataframe.to_csv(OUT_FILEPATH, index=False)
