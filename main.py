from pathlib import Path
import pandas as pd
import json

#[1] = created date
#[5] = complaint type
#[6] = descriptor

def get_datafile_path(given_fname):
    return Path(__file__).parents[1] / given_fname #One level above parent folder.

def load_df():
    csv_path = get_datafile_path("data/test_trimmer.csv")
    data_df = pd.read_csv(csv_path)

    return data_df

def analyze_df(given_df): #Get data rows where Complaint Type contains Noise.
    #Sort by group according to Month and complaint descriptor. Size function counts the number of rows in each group.
    analyzed_df = given_df.groupby(['Month', 'Descriptor']).size().reset_index(name='Count')

    #Create new df from given_df selected by Complaint Type.
    ct_df = given_df[given_df['Complaint Type'].str.contains('Noise')]
    
    #Sort by group according to Month and Descriptor. Size function counts the number of rows in each group.
    ct_df = ct_df.groupby(['Month', 'Descriptor']).size().reset_index(name='Count')

    #return analyzed_df

def get_count_list(given_df, complaint_type_selection, descriptor_selection):
    count =[]

    #Select rows according to complaint type.
    dummy_df = given_df[given_df['Complaint Type'].str.contains(complaint_type_selection)]

    #Get the count of rows according to the descriptor and month.
    for i in range(1, 13):
        #Select rows according to month.
        count_df = dummy_df[dummy_df['Month'] == i]

        #print the count of rows according to the descriptor_selection.
        count.append(count_df.loc[count_df['Descriptor'] == descriptor_selection].count()['Descriptor'])

    return count

def write_csv(given_df):
    given_df.to_csv('test_analyzer.csv', index=False, header=True)

    print('CSV file created.')

def get_list_uniques(given_df, user_selection):
    unique_list = given_df[user_selection].unique()
    return unique_list

def main():

    loaded_data = load_df()
    #analyzed_data = analyze_df(loaded_data)

    complaint_type_uniques = get_list_uniques(loaded_data, 'Complaint Type')
    descriptor_uniques = get_list_uniques(loaded_data, 'Descriptor')

    print(get_count_list(loaded_data, 'Noise', 'Noise: Loud Music/Daytime (Mark Date And Time) (NN1)'))

main()