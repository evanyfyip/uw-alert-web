"""
Tests for parse_uw_alerts.py
"""
import os
import unittest
import pandas as pd

#pylint: disable=import-error
from parse_uw_alerts.parse_uw_alerts import (
    prompt_gpt,
    generate_ids,
    parse_txt_data,
    clean_gpt_output,
    generate_csv,
    scrape_uw_alerts
)

class TestParseUWAlertsPromptGPT(unittest.TestCase):
    """
    Test methods for prompt_gpt function.
    """
    def test_prompt_list(self):
        """Test for lines being a list"""
        with self.assertRaises(ValueError):
            prompt_gpt('not a line')
    def test_prompt_list_length(self):
        """Test for lines having at least 1 item"""
        with self.assertRaises(ValueError):
            prompt_gpt([])
    def test_prompt_bool(self):
        """Test for return_alert_type being boolean"""
        with self.assertRaises(ValueError):
            prompt_gpt(['October 21, 2019\n', 'UW Alert'],
                       return_alert_type='yes')

class TestParseUWAlertsGenerateIds(unittest.TestCase):
    """
    Test methods for generate_ids function.
    """
    def test_gen_id_filepath(self):
        """Test for string filepath"""
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=1,
                         gpt_table=pd.DataFrame({'Test': [1]}),
                         alert_type='Update')
    def test_gen_id_filepath_csv(self):
        """Test for .csv filepath"""
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "../../data/output.txt")
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=file_path,
                         gpt_table=pd.DataFrame({'Test': [1]}),
                         alert_type='Update')
    def test_gen_id_dataframe(self):
        """Test for Pandas DataFrame input"""
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "../../data/uw_alerts_gpt.csv")
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=file_path,
                         gpt_table=[1],
                         alert_type='Update')
    def test_gen_id_dataframe_len(self):
        """Test for DataFrame of at least 1 row"""
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "../../data/uw_alerts_gpt.csv")
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=file_path,
                         gpt_table=pd.DataFrame(),
                         alert_type='Update')
    def test_gen_id_dataframe_alert_type(self):
        """Test for string alert_type being 'Update' or 'Original'"""
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "../../data/uw_alerts_gpt.csv")
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=file_path,
                         gpt_table=pd.DataFrame({'Test': [1]}),
                         alert_type='Random')
    def test_gen_id_parsing(self):
        """Test for requiring boolean parsing"""
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "../../data/uw_alerts_gpt.csv")
        with self.assertRaises(ValueError):
            generate_ids(uw_alert_file=file_path,
                         gpt_table=pd.DataFrame({'Test': [1]}),
                         alert_type='Update',
                         parsing='yes')

class TestParseUWAlertsGenerateCSV(unittest.TestCase):
    """
    Test methods for generate_csv function.
    """
    def test_gen_csv_filepath(self):
        """Test for string filepath"""
        with self.assertRaises(ValueError):
            generate_csv(out_filepath=1,
                         lines=['1', '2'])
    def test_gen_csv_filepath_csv(self):
        """Test for string .csv filepath"""
        with self.assertRaises(ValueError):
            generate_csv(out_filepath='../data/output.txt',
                         lines=['1', '2'])
    def test_gen_csv_list(self):
        """Test for lines being a list"""
        with self.assertRaises(ValueError):
            generate_csv(out_filepath='../data/uw_alerts_gpt.csv',
                         lines=1)
    def test_gen_csv_list_length(self):
        """Test for lines having at least 1 item"""
        with self.assertRaises(ValueError):
            generate_csv(out_filepath='../data/uw_alerts_gpt.csv',
                         lines=[])

class TestParseUWAlertsParseTxtData(unittest.TestCase):
    """
    Test methods for parse_txt_data function.
    """
    def test_txt_extension(self):
        """Test for requiring .txt input"""
        with self.assertRaises(ValueError):
            parse_txt_data('../data/UW_Alerts_2018_2022.csv',
                           out_filepath='../data/uw_alerts_gpt.csv')
    def test_txt_extension_csv(self):
        """Test for requiring .txt input"""
        with self.assertRaises(ValueError):
            parse_txt_data(filepath='../data/UW_Alerts_2018_2022.txt',
                           out_filepath='../data/uw_alerts_gpt.txt')
    def test_txt_extension_fp_str(self):
        """Test for requiring string input"""
        with self.assertRaises(ValueError):
            parse_txt_data(filepath=1,
                           out_filepath='../data/uw_alerts_gpt.csv')
    def test_txt_extension_out_str(self):
        """Test for requiring string output"""
        with self.assertRaises(ValueError):
            parse_txt_data(filepath='../data/UW_Alerts_2018_2022.txt',
                           out_filepath=1)
    def test_txt_file_start_int(self):
        """Test for requiring integer file_start"""
        with self.assertRaises(ValueError):
            parse_txt_data(filepath='../data/UW_Alerts_2018_2022.txt',
                           out_filepath='../data/uw_alerts_gpt.csv',
                           file_start='1')
    def test_txt_file_start_zero_or_greater(self):
        """Test for requiring file_start >= 0"""
        with self.assertRaises(ValueError):
            parse_txt_data(filepath='../data/UW_Alerts_2018_2022.txt',
                           out_filepath='../data/uw_alerts_gpt.csv',
                           file_start=-1)

class TestParseUWAlertsCleanGPTOutput(unittest.TestCase):
    """
    Test methods for clean_gpt_output function.
    """
    def test_clean_gpt_csv_fp(self):
        """Test for requiring .csv filepath"""
        with self.assertRaises(ValueError):
            clean_gpt_output(gpt_output='test.txt')
    def test_clean_gpt_df(self):
        """Test for requiring Pandas DataFrame input"""
        with self.assertRaises(ValueError):
            clean_gpt_output(gpt_output=[1,2,3])

class TestParseUWAlertsScrapeUWAlerts(unittest.TestCase):
    """
    Test methods for scrape_uw_alerts function.
    """
    def test_scrape_uw_alerts_csv_fp(self):
        """Test for requiring .csv filepath"""
        with self.assertRaises(ValueError):
            scrape_uw_alerts(uw_alert_filepath='../data/uw_alerts_clean.txt')
    def test_scrape_uw_alerts_str_fp(self):
        """Test for requiring string filepath"""
        with self.assertRaises(ValueError):
            scrape_uw_alerts(uw_alert_filepath=1)

if __name__ == '__main__':
    unittest.main()
