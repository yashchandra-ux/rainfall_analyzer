"""
Automated test cases for rainfall_analyzer.py
Author: Yash Chandra

Run:
    python -m unittest discover -s testcases -p "test_*.py"
"""

import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import pandas as pd

# Allow importing the application when tests run from the repository root.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import rainfall_analyzer as app


class RainfallAnalyzerTestCases(unittest.TestCase):
    """Test cases for Yash Chandra's Rainfall Data Analyzer."""

    def setUp(self):
        self.df = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Rainfall_mm": [100.0, 250.0, 150.0, 300.0],
        })

    def create_csv(self, content):
        temp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", newline=""
        )
        temp.write(content)
        temp.close()
        self.addCleanup(os.unlink, temp.name)
        return temp.name

    def capture_output(self, function, *args, **kwargs):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            function(*args, **kwargs)
        return output.getvalue()

    def test_tc01_load_valid_csv(self):
        path = self.create_csv(
            "Month,Rainfall_mm\nJan,100\nFeb,250\nMar,150\n"
        )

        df = app.load_data(path)

        self.assertEqual(len(df), 3)
        self.assertEqual(df["Month"].tolist(), ["Jan", "Feb", "Mar"])
        self.assertEqual(df["Rainfall_mm"].tolist(), [100.0, 250.0, 150.0])

    def test_tc02_skip_missing_values(self):
        path = self.create_csv(
            "Month,Rainfall_mm\nJan,100\nFeb,\n,150\nMar,200\n"
        )

        output = self.capture_output(app.load_data, path)

        self.assertIn("Row 2 skipped: missing value.", output)
        self.assertIn("Row 3 skipped: missing value.", output)

    def test_tc03_skip_invalid_rainfall(self):
        path = self.create_csv(
            "Month,Rainfall_mm\nJan,100\nFeb,abc\nMar,200\n"
        )

        output = self.capture_output(app.load_data, path)

        self.assertIn("Row 2 skipped: invalid Rainfall 'abc'.", output)

    def test_tc04_skip_negative_rainfall(self):
        path = self.create_csv(
            "Month,Rainfall_mm\nJan,100\nFeb,-50\nMar,200\n"
        )

        output = self.capture_output(app.load_data, path)

        self.assertIn("Row 2 skipped: Rainfall cannot be negative.", output)

    def test_tc05_missing_file(self):
        output = self.capture_output(
            app.load_data, "missing_rainfall_file.csv"
        )

        self.assertIn("not found", output)

    def test_tc06_empty_file(self):
        path = self.create_csv("")

        df = app.load_data(path)

        self.assertIsNone(df)

    def test_tc07_statistics_output(self):
        output = self.capture_output(app.statistics, self.df)

        self.assertIn("Total: 800 mm", output)
        self.assertIn("Mean: 200.00", output)
        self.assertIn("Max: Apr (300)", output)
        self.assertIn("Min: Jan (100)", output)
        self.assertIn("Std Dev: 77.46", output)
        self.assertIn("Heavy rainfall months: Feb, Apr", output)

    def test_tc08_no_heavy_rainfall(self):
        df = pd.DataFrame({
            "Month": ["Jan", "Feb"],
            "Rainfall_mm": [100.0, 150.0],
        })

        output = self.capture_output(app.statistics, df)

        self.assertIn("No month above 200 mm", output)

    def test_tc09_compare_and_plot(self):
        with patch.object(app.plt, "show"):
            output = self.capture_output(app.compare_and_plot, self.df)

        self.assertIn("Above average (200.00)", output)
        self.assertIn("Feb (250)", output)
        self.assertIn("Apr (300)", output)
        self.assertIn("Below average", output)
        self.assertIn("Jan (100)", output)
        self.assertIn("Mar (150)", output)
        self.assertIn("Bar chart 'Monthly Rainfall' displayed", output)

    def test_tc10_trend_plot(self):
        with patch.object(app.plt, "show"):
            output = self.capture_output(app.trend_plot, self.df)

        self.assertIn("Line chart 'Rainfall Trend' displayed", output)

    def test_tc11_main_exit_option(self):
        with patch.object(app, "load_data", return_value=self.df), \
             patch("builtins.input", return_value="5"):
            output = self.capture_output(app.main)

        self.assertIn("Choose option:", output)

    def test_tc12_main_invalid_option(self):
        with patch.object(app, "load_data", return_value=self.df), \
             patch("builtins.input", side_effect=["6", "5"]):
            output = self.capture_output(app.main)

        self.assertIn("Invalid option.", output)

    def test_tc13_main_statistics_option(self):
        with patch.object(app, "load_data", return_value=self.df), \
             patch("builtins.input", side_effect=["1", "5"]):
            output = self.capture_output(app.main)

        self.assertIn("Total: 800 mm", output)

    def test_tc14_main_heavy_rainfall_option(self):
        with patch.object(app, "load_data", return_value=self.df), \
             patch("builtins.input", side_effect=["2", "5"]):
            output = self.capture_output(app.main)

        self.assertIn("Heavy rainfall months: Feb, Apr", output)

    def test_tc15_main_no_valid_data(self):
        empty_df = pd.DataFrame(columns=["Month", "Rainfall_mm"])

        with patch.object(app, "load_data", return_value=empty_df):
            output = self.capture_output(app.main)

        self.assertIn("No valid data to analyse.", output)


if __name__ == "__main__":
    unittest.main()
