import unittest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from article_utils import find_allsides_metadata

class TestFindAllSidesMetadata(unittest.TestCase):

    def setUp(self):
        self.mock_df = pd.DataFrame({
            "news_source": ["Fox News", "CNN", "BBC"],
            "screen_name": ["Fox", "CNN", "BBC"],
            "rating": ["right", "left", "center"],
            "confidence_level": ["High", "Medium", "High"],
            "perc_agree": [0.85, 0.75, 0.9],
            "type": ["News Media", "News Media", "News Media"],
            "url": ["https://allsides.com/fox", "https://allsides.com/cnn", "https://allsides.com/bbc"]
        })

        self.mock_df["news_source_clean"] = self.mock_df["news_source"].str.lower().str.strip()
        self.mock_df["screen_name_clean"] = self.mock_df["screen_name"].str.lower().str.strip()

    def test_find_existing_source(self):
        result = find_allsides_metadata("Fox", self.mock_df)
        self.assertEqual(result["rating"], "right")
        self.assertEqual(result["confidence"], "High")
        self.assertEqual(result["perc_agree"], "85.0%")
        self.assertEqual(result["allsides_url"], "https://allsides.com/fox")

    def test_find_nonexistent_source(self):
        result = find_allsides_metadata("Bruh news", self.mock_df)
        self.assertEqual(result["rating"], "Unknown")
        self.assertIsNone(result["allsides_url"])

if __name__ == "__main__":
    unittest.main()
