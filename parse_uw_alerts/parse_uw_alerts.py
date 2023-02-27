"""
Functions to parse UW Alerts text data and extract 
key incident information in a tabular format.
"""
import io
import time
import re
import pandas as pd
import openai
from transformers import GPT2Tokenizer
import googlemaps
# from scraper import scrape_uw_alerts

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

    gpt_task = ('Extract a markdown table with the columns Date (mm/dd/yyyy),'
                ' Report Time (hh:mm AM/PM), Incident Time (hh:mm AM/PM),'
                ' Nearest Intersection to Incident, Incident Category, and'
                ' Incident Summary from the following alert message.\n'
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
    gpt_table.drop(list(
        gpt_table.filter(regex = 'Unnamed')), axis = 1, inplace = True)
    column_names = ['Date', 'Report Time', 'Incident Time',
                    'Nearest Intersection to Incident', 
                    'Incident Category', 'Incident Summary']
    gpt_table.columns = column_names
    gpt_table = gpt_table.iloc[1:]
    gpt_table = gpt_table.loc[:, column_names]
    for column in column_names:
        gpt_table[column] = gpt_table[column].astype(str).str.strip()
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
        start = 326
        for i, line in enumerate(lines[start:]):
            if i + start == len(lines) - 1:
                print((alert_chunk_start+start, i+start))
                table = prompt_gpt(lines[(alert_chunk_start+start):(i+start)])
                clean_data = pd.read_csv(out_filepath, index_col=False)
                clean_data = pd.concat([clean_data, table], ignore_index=True)
                clean_data.to_csv(out_filepath, index=False)
            date_check = re.match(r'^[A-z]+\s\d{1,2},\s\d{4}\n$', line)
            if date_check:
                if alert_chunk_start is None:
                    alert_chunk_start = i
                else:
                    alert_chunk_end = i
                    print((alert_chunk_start+start, alert_chunk_end+start))
                    table = prompt_gpt(
                        lines[(alert_chunk_start+start):(alert_chunk_end+start)])
                    clean_data = pd.read_csv(out_filepath, index_col=False)
                    clean_data = pd.concat(
                        [clean_data, table], ignore_index=True)
                    clean_data.to_csv(out_filepath, index=False)
                    alert_chunk_start = i
    return clean_data

def clean_gpt_output(gpt_output='./data/uw_alerts_gpt.csv',
                     gmaps_client=None):
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
        gpt_data = gpt_output.copy()
    else:
        if not re.search('.csv$', gpt_output):
            raise ValueError("gpt_output must be a .csv filepath")
        gpt_data = pd.read_csv(gpt_output, index_col=False)

    gpt_data['Date'] = pd.to_datetime(gpt_data['Date'],
                                      infer_datetime_format=True)
    gpt_data['Date'] = gpt_data['Date'].dt.date
    gpt_data['Report Time'] = gpt_data['Report Time'].str.upper()
    gpt_data['Incident Time'] = gpt_data['Incident Time'].str.upper()
    gpt_data['Report Time'] = gpt_data['Report Time'].str.replace(
        r'\.|-|UNKNOWN', '', regex=True)
    gpt_data['Incident Time'] = gpt_data['Incident Time'].str.replace(
        r'\.|-|UNKNOWN', '', regex=True)
    gpt_data[['Nearest Intersection to Incident']] = gpt_data[
        ['Nearest Intersection to Incident']].fillna('')
    geocode_results = [gmaps_client.geocode(
        ''.join([address, ', University District, Seattle WA'])
        ) for address in gpt_data['Nearest Intersection to Incident']]
    gpt_data['Google Address'] = [
        result[0]['formatted_address'] for result in geocode_results]
    gpt_data['geometry'] = [
        result[0]['geometry'] for result in geocode_results]
    return gpt_data

if __name__ == "__main__":
    OPENAI_API_KEY =  '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'
    GOOGLE_MAPS_API_KEY = 'AIzaSyCJ3lSOMFCV5NHsBAcyzM6wSP3reSu0qy4'
    FILEPATH = './data/UW_Alerts_2018_2022.txt'
    OUT_FILEPATH = './data/uw_alerts_gpt.csv'
    CLEAN_FILEPATH = './data/uw_alerts_clean.csv'
    openai.api_key = OPENAI_API_KEY
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    # parse_txt_data(FILEPATH, OUT_FILEPATH)
    # scraped_data = scrape_uw_alerts()
    # for content in scraped_data:
    #     print(content.text)
    gpt_clean = clean_gpt_output(gmaps_client=gmaps)
    gpt_clean.to_csv(CLEAN_FILEPATH, index=False)
