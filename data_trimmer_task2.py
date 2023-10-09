from pathlib import Path
import pandas as pd
import json

#[5] = Complaint Type
#[6] = Descriptor
#[7] = Location Type

def get_datafile_path(given_fname):
    return Path(__file__).parents[1] / given_fname #One level above parent folder.

def load_df():
    csv_path = get_datafile_path("data/rodent_raw.csv")
    data_df = pd.read_csv(csv_path, header=None, usecols=[5, 6, 7])

    #Rename columns headers as appropriate.
    data_df = data_df.rename(columns={5: 'Complaint Type', 6: 'Descriptor', 7: 'Location Type'})

    return data_df

def clean_df(given_df): #Get data rows where Complaint Type contains Noise.

    #Drop rows where Complaint Type or Created Date is empty.
    cleaned_df = given_df.dropna(subset=['Complaint Type', 'Descriptor', 'Location Type'])

    #Remove rows where Complaint Type is 'Food Establishment'. Reason: Rodent/Insect/Trash descriptor is vague.
    cleaned_df = cleaned_df[cleaned_df['Complaint Type'] != 'Food Establishment']

    #Remove rows where Location Type is 'Commercial Building'. Reason: vague/unuseful.
    cleaned_df = cleaned_df[cleaned_df['Location Type'] != 'Commercial Building']

    #Remove rows where Location Type is 'Other' or 'Other (Explain Below)'.
    cleaned_df = cleaned_df[cleaned_df['Location Type'] != 'Other']
    cleaned_df = cleaned_df[cleaned_df['Location Type'] != 'Other (Explain Below)']

    #Replace values in Location Type column matching 'x' with 'y'.
    cleaned_df['Location Type'] = cleaned_df['Location Type'].replace('Cafeteria - Public School', 'School')
    cleaned_df['Location Type'] = cleaned_df['Location Type'].replace('School/Pre-School', 'School')
    cleaned_df['Location Type'] = cleaned_df['Location Type'].replace('3+ Family Apartment Building', '3+ Family Apt. Building')

    #Get list of unique values in Location Type column.
    location_types = cleaned_df['Location Type'].unique()

    #Get count of rows where Location Type is 'School'.
    school_count = cleaned_df['Location Type'].value_counts()['School']
    print('Number of rows where Location Type is School: ' + str(school_count))

    #Remove rows where row counts of values in Location Type column are less than 100.
    for location_type in location_types:
        if cleaned_df['Location Type'].value_counts()[location_type] < 100:
            print('Removing rows where Location Type is ' + location_type + '.' + str(cleaned_df['Location Type'].value_counts()[location_type]))
            cleaned_df = cleaned_df[cleaned_df['Location Type'] != location_type]

    return cleaned_df

def write_csv(given_df):
    given_df.to_csv('rodent_cleaned.csv', index=False, header=True)
    print('CSV file created.')

def main():
    loaded_data = load_df()
    clean_data = clean_df(loaded_data)
    print(clean_data)
    write_csv(clean_data)

if __name__ == '__main__':
    main()