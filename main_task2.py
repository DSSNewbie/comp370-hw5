import random
from pathlib import Path
import pandas as pd
import math

from bokeh.layouts import column
from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource

def get_datafile_path(given_fname):
    return Path(__file__).parents[1] / given_fname #One level above parent folder.

def load_df():
    csv_path = get_datafile_path("data/rodent_cleaned.csv")
    data_df = pd.read_csv(csv_path)

    return data_df

def get_list_uniques(given_df, given_category):
    unique_list = given_df[given_category].unique()

    return unique_list.tolist()

def get_count_dict(given_df, given_list):
    location_count = {}

    for location in given_list:
        location_count[location] = given_df['Location Type'].value_counts()[location]

    #Sort dictionary by value in descending order.
    location_count = dict(sorted(location_count.items(), key=lambda item: item[1], reverse=True))

    return location_count

def main():
    #Data prep section.
    loaded_data = load_df()
    location_uniques = get_list_uniques(loaded_data, 'Location Type')
    location_count_dict = get_count_dict(loaded_data, location_uniques)

    location_sorted_list = list(location_count_dict.keys())
    #Replace all spaces in list with new line.
    for i in range(len(location_sorted_list)):
        location_sorted_list[i] = location_sorted_list[i].replace(" ", "\n")

    location_count_list = list(location_count_dict.values())

    #Visualization section.
    p = figure(x_range=location_sorted_list, width=1000, height=500, title="NYC Location Types by Rodent Incident Report Counts", x_axis_label="Location Type", y_axis_label="Rodent Incident Report Count")

    p.vbar(
        x=location_sorted_list,
        top=location_count_list,
        width=0.9,
        color="blue",
    )

    curdoc().add_root(column(p))

main()