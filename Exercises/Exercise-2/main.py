import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import csv
import io
from requests.exceptions import HTTPError
import numpy as np




def main():
    try:
        url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        text = '2022-02-07 14:03'
        obj = soup.find(lambda tag: tag.name=='td' and text in tag.text)

        all_urls = []
        rows = soup.find_all('tr')
        for row in rows:
            row_url = row.find('td')
            tag = row.find(lambda tag: tag.name=='td' and text in tag.text)
            if tag and row_url:
                all_urls.append(row_url.get_text())

        csv = all_urls[0]
        csv_page = url+csv
        csv_page1 = requests.get(csv_page)
        con = csv_page1.content

        df = pd.read_csv(io.StringIO(con.decode('utf-8')))
        highest = df.loc[df.HourlyDryBulbTemperature==max(df.HourlyDryBulbTemperature)]
        max_val = max(df.HourlyDryBulbTemperature)
        print(f"Max_Val: {max_val}")
        print(highest.head())
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


if __name__ == '__main__':
    main()
