import boto3
import glob, os
import json
import csv
from flatten_json import flatten
import pandas as pd

def open_json(file_path):
    with open(file_path) as f:
        jf = json.load(f)
    return jf

def get_those_files(target_path):
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".json"):
                #Get file path
                file_path = os.path.join(root, file)

                #Get filename
                filename = file.split(".")

                #Helper function to open json
                jf = open_json(file_path)

                #Flatten json so that it can be converted to csv
                flat_jf = flatten(jf)

                #Convert data to pandas dataframe and export to csv
                jf_df = pd.DataFrame(flat_jf, index=[0])
                jf_df.to_csv(f'./data/{filename[0]}.csv')  

def main():
    get_those_files("./data")

if __name__ == '__main__':
    main()
