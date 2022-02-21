from distutils.command.config import config
from importlib.resources import read_text
from os import sep
import boto3
from botocore.config import Config
import pandas as pd
import gzip
import warcio
from warcio.archiveiterator import ArchiveIterator


def download_s3(bucket, filename, new_filename):
    s3 = boto3.client('s3', 
                      aws_access_key_id='', 
                      aws_secret_access_key='', 
                      region_name=''
                      )
    s3.download_file(bucket, filename, new_filename)

def getFilename(url):
    if url.find('/'):
        return url.rsplit('/', 1)[1]

def open_gz(fn):
    with gzip.open(fn) as f:
        cc = pd.read_csv(f, sep=" ")
    return cc

def main():
    download_s3('commoncrawl','crawl-data/CC-MAIN-2022-05/wet.paths.gz','wet.paths.gz')

    cc = open_gz('wet.paths.gz')
    
    filename = cc.iloc[0][0]
    if filename:
        print(f"here: {filename}")
        fn = getFilename(filename)

        download_s3('commoncrawl',filename, fn)

        with open(fn, 'rb') as stream:
            for record in ArchiveIterator(stream):
                #if record.rec_type == 'response':
                print(record.rec_headers.get_header('WARC-Target-URI'))

if __name__ == '__main__':
    main()
