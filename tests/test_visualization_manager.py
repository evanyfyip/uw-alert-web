"""
Tests for visualization_manager.py
"""
import unittest
# from click import get_current_context
from datetime import datetime, timedelta
import geopandas as gpd
import pandas as pd
import pandas.testing as pdt
import numpy as np
from visualization_manager.visualization_manager \
    import filter_geodf, get_folium_map, get_urgent_incidents

class TestGetUrgentAlerts(unittest.TestCase):
    """
    Tests get_urgent_alerts method in
    visualization_manager.py.
    """

    # Smoke test
    def test_smoke(self):
        """
        Smoke test for get_urgent_alerts function
        """
        flag = True
        try:
            alerts_df = pd.read_csv('data/uw_alerts_clean.csv')
            get_urgent_incidents(alerts_df, time_frame=4)
        except ValueError:
            flag = False
        self.assertTrue(flag)

    # One shot tests
    def test_time_frame_cutoff(self):
        """
        get_urgent incidents should filter the
        incidents dataframe based on whether the
        date and report time was within the timeframe of 
        4 hours before the current time.
        """
        today = datetime.today()
        two_days_ago = today - timedelta(days=2)
        cols = ["Alert ID", "Incident ID", "Date", "Report Time", "Keep"]
        data = [["1", "1", two_days_ago.strftime('%m/%d/%Y'),
                    two_days_ago.strftime("%H:%M"), False],
                ["2", "2", today.strftime('%m/%d/%Y'), today.strftime("%H:%M"), True],
                ["3", "2", (today - timedelta(hours=3)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=3)).strftime("%H:%M"), True],
                ["4", "2", (today - timedelta(hours=5)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=5)).strftime("%H:%M"), True],
                ["5", "2", (today - timedelta(hours=6)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=6)).strftime("%H:%M"), True],
                ["6", "4", (today - timedelta(hours=10)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=10)).strftime("%H:%M"), False]]
        test_data = pd.DataFrame(data, columns=cols)
        expected = test_data[test_data['Keep']]
        result = get_urgent_incidents(alerts_df=test_data, time_frame=4)
        pdt.assert_frame_equal(expected, result)

    def test_missing_report_times(self):
        """
        get_urgent incidents should filter based
        on report time and date first, but if there
        is no report time, it should take any incidents
        that occured that day."""
        today = datetime.today()
        two_days_ago = today - timedelta(days=2)
        cols = ["Alert ID", "Incident ID", "Date", "Report Time", "Keep"]
        data = [["1", "1", two_days_ago.strftime('%m/%d/%Y'),
                    two_days_ago.strftime("%H:%M"), False],
                ["2", "2", today.strftime('%m/%d/%Y'), today.strftime("%H:%M"), True],
                ["3", "2", (today - timedelta(hours=3)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=3)).strftime("%H:%M"), True],
                ["4", "2", (today - timedelta(hours=5)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=5)).strftime("%H:%M"), True],
                ["5", "2", (today - timedelta(hours=6)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=6)).strftime("%H:%M"), True],
                ["6", "4", today.strftime('%m/%d/%Y'), None, True]]
        test_data = pd.DataFrame(data, columns=cols)
        expected = test_data[test_data['Keep']]
        result = get_urgent_incidents(alerts_df=test_data, time_frame=4)
        pdt.assert_frame_equal(expected, result)

    def test_no_urgent_incidents(self):
        """
        Tests the case where all incidents are
        outside of the timeframe, so get_urgent_incidents
        should return no incidents.
        """
        today = datetime.today()
        two_days_ago = today - timedelta(days=2)
        cols = ["Alert ID", "Incident ID", "Date", "Report Time", "Keep"]
        data = [["1", "1", two_days_ago.strftime('%m/%d/%Y'),
                    two_days_ago.strftime("%H:%M"), False],
                ["2", "2", (today - timedelta(hours=5)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=5)).strftime("%H:%M"), False],
                ["3", "3", (today - timedelta(hours=6)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=6)).strftime("%H:%M"), False],
                ["4", "4", (today - timedelta(hours=10)).strftime('%m/%d/%Y'),
                    (today - timedelta(hours=10)).strftime("%H:%M"), False]]
        test_data = pd.DataFrame(data, columns=cols)
        expected = test_data[test_data['Keep']]
        result = get_urgent_incidents(alerts_df=test_data, time_frame=4)
        pdt.assert_frame_equal(expected, result)

    # Edge cases
    def test_dataframe_schema(self):
        """
        Testing get_urgent_incidents, raising
        ValueError if essential columns are missing.
        """
        cols = ['Alert ID', 'Incident ID', 'Date']
        data = [['1', '2', '3/4/23']]
        test_data = pd.DataFrame(data, columns=cols)
        with self.assertRaises(ValueError):
            get_urgent_incidents(alerts_df=test_data, time_frame=4)

class TestFilterGeoDF(unittest.TestCase):
    """
    Tests methods for filter_geodf function
    in visualization_manager.py
    """
    # Smoke tests
    def test_smoke(self):
        """
        Smoke test for filter_geodf
        """
        flag = True
        try:
            gdf = gpd.read_file('data/SeattleGISData/udistrict_streets.geojson')
            filter_geodf(gdf, lat=10.0, lon=15)
        except ValueError:
            flag = False
        self.assertTrue(flag)

    # One shot tests
    def test_coord_on_street1(self):
        """
        One shot test for coordinates on 
        42nd street between 9th and Roosevelt
        """
        point = [47.657489, -122.318281]
        gdf = gpd.read_file('data/SeattleGISData/udistrict_streets.geojson')
        test_gdf = filter_geodf(gdf, lat=point[0], lon=point[1])
        self.assertEqual(len(test_gdf), 1)
        self.assertEqual(test_gdf['UNITDESC'].iloc[0],
            "NE 42ND ST BETWEEN 9TH AVE NE AND ROOSEVELT S WAY NE")

    def test_coord_on_street2(self):
        """
        One shot test for coordinates on 
        8th Ave between 43rd and 45th
        """
        point = [47.660443, -122.319788]
        gdf = gpd.read_file('data/SeattleGISData/udistrict_streets.geojson')
        test_gdf = filter_geodf(gdf, lat=point[0], lon=point[1])
        self.assertEqual(len(test_gdf), 1)
        self.assertEqual(test_gdf['UNITDESC'].iloc[0],
            "8TH AVE NE BETWEEN NE 43RD ST AND NE 45TH W ST")

    def test_intersection(self):
        """
        One shot test for 45th and Brooklyn
        intersection. Should return dataframe with 4 streets
        """
        point = [47.66131221275655, -122.31431884850726]
        gdf = gpd.read_file('data/SeattleGISData/udistrict_streets.geojson')
        test_gdf = filter_geodf(gdf, lat=point[0], lon=point[1])

        streets = ['NE 45TH ST BETWEEN 12TH AVE NE AND BROOKLYN AVE NE',
                   'BROOKLYN AVE NE BETWEEN NE 45TH ST AND NE 47TH ST',
                   'BROOKLYN AVE NE BETWEEN NE 43RD ST AND NE 45TH ST',
                   'NE 45TH ST BETWEEN BROOKLYN AVE NE AND UNIVERSITY WAY NE']
        test_streets = list(test_gdf['UNITDESC'])
        self.assertEqual(len(test_gdf), 4)
        for street in test_streets:
            self.assertTrue(street in streets)

    # Edge case tests
    def test_gdf_input_type(self):
        """
        Edge case test to check that gdf is a geopandas
        dataframe
        """
        test_cases = ["String", {}, np.array([3, 2, 2]), 34]
        for gdf in test_cases:
            with self.assertRaises(TypeError):
                filter_geodf(gdf, lat=33.2, lon=22.1)

    def test_valid_lon_lat(self):
        """
        Edge case test to check that invalid longitude, latitude
        values raise a ValueError
        """
        test_cases = [[-90.4, -130], [22, 190], [-180, -200]]
        gdf = gpd.read_file('data/SeattleGISData/udistrict_streets.geojson')
        for point in test_cases:
            with self.assertRaises(ValueError):
                filter_geodf(gdf, lat=point[0], lon=point[1])

class TestGetFoliumMap(unittest.TestCase):
    """
    Tests methods for get_folium_map function
    in visualization_manager.py
    """
    # Smoke tests
    def test_smoke(self):
        """
        Smoke test for get_folium_map
        """
        alert_coords = [[47.663082, -122.310859], [47.658377, -122.317777]]
        alert_messages = ["Police looking for man with handgun on 47th St. near 16th Ave. Secure doors, avoid area if possible.",
                        "Shooting reported near 42nd Ave NE/Roosevelt at 12:46pm. Shooter fled in white vehicle."]
        map = get_folium_map(alert_coords, alert_messages)
        self.assertTrue(True)

    # TODO: Make one-shot tests

    # Edge case tests
    def test_alert_coords_type(self):
        """
        Edge case test to check that alert_coords is a list
        """
        test_cases = ["String", {}, np.array([3, 2, 2]), 34]
        alert_messages = ["One", "Two"]
        for test in test_cases:
            with self.assertRaises(ValueError):
                get_folium_map(test, alert_messages)

    def test_alert_coords_type(self):
        """
        Edge case test to check that the coords in alert_coords are numbers
        """
        test_cases = ["String", {}, np.array([3, 2, 2])]
        alert_messages = ["One", "Two"]
        for test in test_cases:
            alert_coords = [[test, -122.310859], [47.658377, -122.317777]]
            with self.assertRaises(ValueError):
                get_folium_map(alert_coords, alert_messages)

    def test_alert_messages_type(self):
        """
        Edge case test to check that alert_messages is a list
        """
        alert_coords = [[47.663082, -122.310859], [47.658377, -122.317777]]
        test_cases = ["String", {}, np.array([3, 2, 2]), 34]
        for test in test_cases:
            with self.assertRaises(ValueError):
                get_folium_map(alert_coords, test)
 
    def test_alert_messages_length(self):
        """
        Edge case test to check that alert_messages is a list
        """
        alert_coords = [[47.663082, -122.310859], [47.658377, -122.317777]]
        test_cases = [["One"], ["One", "Two", "Three"]]
        for test in test_cases:
            with self.assertRaises(ValueError):
                get_folium_map(alert_coords, test)

    def test_alert_messages_element_type(self):
        """
        Edge case test to check that the elements in alert_messages are strings
        """
        alert_coords = [[47.663082, -122.310859]]
        test_cases = [{}, np.array([3, 2, 2]), 34]
        for test in test_cases:
            with self.assertRaises(ValueError):
                get_folium_map(alert_coords, [test])


if __name__ == '__main__':
    unittest.main()
