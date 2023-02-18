"""
Tests for parse_uw_alerts.py
"""
import unittest
from parse_uw_alerts.parse_uw_alerts import (
    prompt_gpt,
    parse_txt_data
)

class TestParseUWAlersts(unittest.TestCase):
    """
    Test methods for parse_uw_alerts.py.
    """
    def test_txt_extension(self):
        """Test for requiring .txt input"""
        filepath = './data/UW_Alerts_2018_2022.csv'
        with self.assertRaises(ValueError):
            parse_txt_data(filepath)
    def test_empty_lines(self):
        """Test for when lines is empty"""
        lines = []
        with self.assertRaises(ValueError):
            prompt_gpt(lines, 1, 2)
    def test_alert_start(self):
        """Test for invalid alert start"""
        lines = ['First line\n', 'Second line\n']
        with self.assertRaises(ValueError):
            prompt_gpt(lines, -1, 2)
    def test_alert_end(self):
        """Test for invalid alert end"""
        lines = ['First line\n', 'Second line\n']
        with self.assertRaises(ValueError):
            prompt_gpt(lines, 0, 3)

if __name__ == '__main__':
    unittest.main()
