from web_scraper import scraper
import unittest

class web_scraperTestCase(unittest.TestCase):

    def test_get_links(self):
        self.assertEqual(len(scraper.clothes), 72)

    def test_create_id(self):
        self.assertEqual(len(scraper.id_list), 72)

    def test_get_data(self):
        self.assertEqual(len(scraper.price_list), len(scraper.colour_list), len(scraper.description_list))

    def test_create_dict(self):
        self.assertIsInstance(scraper.id_dict, dict)