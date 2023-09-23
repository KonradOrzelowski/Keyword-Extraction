import unittest
import json
from keyword_extraction import KeywordExtraction
from sofifa_scraping import SofifaScraping
from instagram_posts_scraper import InstagramPostsScraper
from connect_mysql import MySQLConnection
from app_flask import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_find_similar_insta(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    # Create a TestResult object to store the test results
    result = unittest.TestResult()

    # Create a TestSuite object containing the TestFlaskApp class
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlaskApp)

    # Run the tests and store the result in the status variable
    status = suite.run(result)

    # Print the status of the tests
    print("Test Status: ", status.wasSuccessful())

