from importlib.resources import path
import web_scraper
import pandas as pd
from sqlalchemy import create_engine

RDS_PASSWORD = 'afgangalo12'
RDS_HOST = 'asos-scraper.c4xuwbscrnlq.us-east-2.rds.amazonaws.com'
RDS_PORT = '5432'

asos_scraper = web_scraper.Scraper()
path, clothes_list = asos_scraper.run_scraper()
print("clothes added to list")
asos_scraper.save_to_file(path, clothes_list)
print("data saved to file")

print("connecting to the database")
engine = create_engine(f'postgresql+psycopg2://postgres:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/paddle')
old_clothes_list = pd.read_sql_table('clothes_list', engine)
# Compare both tables and drop the duplicates
merged_dfs = pd.concat([old_clothes_list, clothes_list])
merged_dfs = merged_dfs.drop_duplicates(keep=False)
merged_dfs.to_sql('clothes_list', engine, if_exists='append', index=False)