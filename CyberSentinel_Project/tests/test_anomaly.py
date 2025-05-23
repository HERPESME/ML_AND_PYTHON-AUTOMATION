# tests/test_anomaly_detector.py

import unittest
import pandas as pd
from src.anomaly_detection.models import AutoencoderModel


class TestAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.df_with_outliers = pd.DataFrame(
            {"price": [100, 101, 99, 98, 300, 102, 101, 103, 500, 104]}
        )
        self.detector = AutoencoderModel(window=3, z_threshold=2.0)

    def test_anomalies_are_detected(self):
        result_df = self.detector.detect(self.df_with_outliers)
        self.assertIn(
            "anomaly", result_df.columns, "Output should contain 'anomaly' column"
        )
        num_anomalies = result_df["anomaly"].sum()
        self.assertGreater(num_anomalies, 0, "Should detect at least one anomaly")

    def test_no_anomalies_in_clean_data(self):
        clean_df = pd.DataFrame({"price": [100, 101, 102, 103, 104, 105]})
        result_df = self.detector.detect(clean_df)
        self.assertEqual(result_df["anomaly"].sum(), 0, "Should detect no anomalies")


if __name__ == "__main__":
    unittest.main()
