"""
Functions to parse UW Alerts text data and extract 
key incident information in a tabular format.
"""
import io
import time
import string
import re
from datetime import datetime
import pandas as pd
import openai
from transformers import GPT2Tokenizer
from scraper import scrape_uw_alerts

def prompt_gpt(lines):
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
    """
    if not isinstance(lines, list):
        raise ValueError("lines must be a list")
    if len(lines) < 1:
        raise ValueError("lines must be at least length 1")
    gpt_task = ('Extract a markdown table with the columns Date, Report Time,'
                ' Incident Time, Incident Address, Incident Category, and'
                ' Incident Summary from the following alert message\n'
                'Text: """')
    alert_chunk = '\n'.join(lines)
    gpt_prompt = '\n'.join([gpt_task, alert_chunk])
    gpt_prompt += '"""'
    print(gpt_prompt)
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    n_tokens = len(tokenizer(gpt_prompt)['input_ids'])
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=gpt_prompt,
        max_tokens=4097-n_tokens)
    print(response['choices'][0]['text'])
    gpt_table = pd.read_table(
        io.StringIO(response['choices'][0]['text']), sep='|', \
            skipinitialspace=True, header=0, index_col=False)
    gpt_table.rename(columns=lambda x: x.strip(), inplace=True)
    gpt_table = gpt_table.iloc[1:]
    column_names = ['Date', 'Report Time', 'Incident Time', 
                    'Incident Address', 'Incident Category',
                    'Incident Summary']
    gpt_table = gpt_table.loc[:, column_names]
    for column in column_names:
        gpt_table[column] = gpt_table[column].str.strip()
    time.sleep(10)
    return gpt_table

def parse_txt_data(filepath, out_filepath):
    """
    Arguments:
        filepath - path to .txt file containing historial UW Alerts blogposts.
        out_filepath - path to .csv file storing GPT output.
    Returns:
        A Pandas dataframe where each row is a blogpost, and there are
        columns containing the post date, post time, incident time, location,
        incident category, the summarized UW Alert message.
    Exceptions:
        filepath must be a string with .txt extension.
        out_filepath must be a string with .csv extension.
        Invalid inputs throw ValueError exceptions.
    """
    if not isinstance(filepath, str):
        raise ValueError("filepath must be a string")
    if re.search(r'\.txt$', filepath) is None:
        raise ValueError("filepath must have a .txt extension")
    if not isinstance(out_filepath, str):
        raise ValueError("filepath must be a string")
    if re.search(r'\.csv$', out_filepath) is None:
        raise ValueError("filepath must have a .csv extension")

    with open(filepath, encoding='UTF-8') as file:
        lines = file.readlines()
        alert_chunk_start = None
        alert_chunk_end = None
        start = 0
        for i, line in enumerate(lines[start:]):
            if i + start == len(lines) - 1:
                print((alert_chunk_start+start, i+start))
                table = prompt_gpt(lines[(alert_chunk_start+start):(i+start)])
                clean_data = pd.read_csv(out_filepath, index_col=False)
                clean_data = pd.concat([clean_data, table], ignore_index=True)
                print(list(clean_data.columns))
                clean_data.to_csv(out_filepath, index=False)
            date_check = re.match(r'^[A-z]+\s\d{1,2},\s\d{4}\n$', line)
            if date_check:
                if alert_chunk_start is None:
                    alert_chunk_start = i
                else:
                    alert_chunk_end = i - 1
                    print((alert_chunk_start+start, alert_chunk_end+start))
                    table = prompt_gpt(
                        lines[(alert_chunk_start+start):(alert_chunk_end+start)])
                    clean_data = pd.read_csv(out_filepath, index_col=False)
                    clean_data = pd.concat(
                        [clean_data, table], ignore_index=True)
                    print(list(clean_data.columns))
                    clean_data.to_csv(out_filepath, index=False)
                    alert_chunk_start = i
    return clean_data

def clean_date(date_string):
    """
    Arguments:
        date_string - string containing date.
    Returns:
        a tuple (year, month, day).
    Exceptions:
        date_string must be a string.
        ValueError will be thrown otherwise.
    """
    if not isinstance(date_string, str):
        raise ValueError("date_string must be a string")
    
    date_abbr = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 
                 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 
                 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    if re.search('\d{2}/\d{2}/\d{4}', date_string):
        date_object = datetime.strptime(date_string, '%m/%d/%Y')
        return (date_object.year, date_object.month, date_object.day)
    else:
        for month, month_number in date_abbr.items():
            if re.search(month, date_string, re.IGNORECASE):
                month_num = month_number
                break
        year = re.search('\d{4}$', date_string)
        if year:
            year = int(year.group(0))
        else:
            year = None
        day = re.sub('\d{4}$|[A-z]', '', date_string)
        day = ''.join(['' if c in string.punctuation else c for c in day])
        day = int(day.strip())
        return (year, month_num, day)

def clean_gpt_output(gpt_output='./data/uw_alerts_gpt.csv'):
    """
    Arguments:
        gpt_output - either a filepath to csv file or Pandas DataFrame.
    Returns:
        A Pandas DataFrame with cleaned columns.
    Exceptions:
        gpt_output must be a filepath with .csv extension or
        a Pandas DataFrame.
        ValueError will be thrown otherwise.
    """
    if not isinstance(gpt_output, str):
       if not isinstance(gpt_output, pd.DataFrame):
           raise ValueError(
               "gpt_output must be a filepath or Pandas DataFrame")
       else:
           gpt_data = gpt_output.copy()
    else:
        if not re.search('.csv$', gpt_output):
            raise ValueError("gpt_output must be a .csv filepath")
        else:
            gpt_data = pd.read_csv(gpt_output, index_col=False)
        
    ymd = [clean_date(date) for date in gpt_data['Date'].values]
    gpt_data['Year'] = [date[0] for date in ymd]
    gpt_data['Month'] = [date[1] for date in ymd]
    gpt_data['Day'] = [date[2] for date in ymd]
    gpt_data[['Year']] = gpt_data[['Year']].fillna(method='ffill')
    gpt_data['Date'] = pd.to_datetime(dict(year=gpt_data.Year,
                                           month=gpt_data.Month,
                                           day=gpt_data.Day))
    gpt_data['Date'] = gpt_data['Date'].dt.date
    gpt_data['Report Time'] = gpt_data['Report Time'].str.upper()
    gpt_data['Incident Time'] = gpt_data['Incident Time'].str.upper()
    gpt_data['Report Time'] = gpt_data['Report Time'].str.replace(
        '\.|\s+', '', regex=True)
    gpt_data['Incident Time'] = gpt_data['Incident Time'].str.replace(
        '\.|\s+', '', regex=True)
    print(gpt_data['Report Time'].values)
     
if __name__ == "__main__":
    OPENAI_API_KEY =  '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'
    FILEPATH = './data/UW_Alerts_2018_2022.txt'
    OUT_FILEPATH = './data/uw_alerts_gpt.csv'
    openai.api_key = OPENAI_API_KEY
    # parse_txt_data(FILEPATH, OUT_FILEPATH)
    # scraped_data = scrape_uw_alerts()
    # for content in scraped_data:
    #     print(content.text)
    clean_gpt_output()
