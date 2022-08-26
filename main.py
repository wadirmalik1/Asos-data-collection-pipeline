from importlib.resources import path
import web_scraper

asos_scraper = web_scraper.Scraper()
path, clothes_list = asos_scraper.run_scraper()
print("clothes added to list")
asos_scraper.save_to_file(path, clothes_list)
print("data saved to file")