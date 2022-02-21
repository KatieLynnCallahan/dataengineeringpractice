import requests, zipfile, io
from requests.exceptions import HTTPError
import os

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

def makeFolder(path):
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print("Folder already created") 

def getFilename(url):
    if url.find('/'):
        return url.rsplit('/', 1)[1]

def main():
    makeFolder('downloads')
    for url in download_uris:
        try:
            response = requests.get(url)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            filename = getFilename(url)
            print(filename)
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall("/downloads")
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')


if __name__ == '__main__':
    main()
