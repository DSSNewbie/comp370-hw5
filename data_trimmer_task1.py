from pathlib import Path
import pandas as pd
import json

#[1] = created date
#[5] = complaint type
#[6] = descriptor

def get_datafile_path(given_fname):
    return Path(__file__).parents[1] / given_fname #One level above parent folder.

def load_df():
    csv_path = get_datafile_path("data/nyc_2020_raw.csv")
    data_df = pd.read_csv(csv_path, header=None, usecols=[1, 5, 6])

    #Rename columns headers as appropriate.
    data_df = data_df.rename(columns={1: 'Created Date', 5: 'Complaint Type', 6: 'Descriptor'})

    return data_df

def clean_df(given_df): #Get data rows where Complaint Type contains Noise.

    #Drop rows where Complaint Type or Created Date is empty.
    cleaned_df = given_df.dropna(subset=['Complaint Type', 'Created Date', 'Descriptor'])

    #Convert the Created Date to the month's numeric value only.
    cleaned_df['Created Date'] = pd.to_datetime(cleaned_df['Created Date']).dt.month

    #Rename the Created Date column to Month.
    cleaned_df = cleaned_df.rename(columns={'Created Date': 'Month'})

    #Select only rows where the Complaint Type contains 'Noise'.
    cleaned_df = cleaned_df[cleaned_df['Complaint Type'].str.contains('Noise')]

    return cleaned_df

def write_csv(given_df):
    given_df.to_csv('test_trimmer.csv', index=False, header=True)

    print('CSV file created.')

def main():

    #print(get_datafile_path('test'))
    loaded_data = load_df()
    clean_data = clean_df(loaded_data)
    write_csv(clean_data)

if __name__ == '__main__':
    main()