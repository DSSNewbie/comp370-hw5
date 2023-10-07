from pathlib import Path
import pandas as pd
import json

from bokeh.layouts import column
from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource

#[1] = created date
#[5] = complaint type
#[6] = descriptor

loaded_data, complaint_type_uniques, month_list, descriptor_uniques, user_ct, user_desc = None, None, None, None, None, None

plot_dataset = ColumnDataSource(dict(month=[], test=[]))

def get_datafile_path(given_fname):
    return Path(__file__).parents[1] / given_fname #One level above parent folder.

def load_df():
    csv_path = get_datafile_path("data/test_trimmer.csv")
    data_df = pd.read_csv(csv_path)

    return data_df

def get_month_names():
    month_dict = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
  }

    month_list = list(month_dict.values())

    return month_list

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

def update_descriptor_list(event):
    global descriptor_uniques

    user_ct = event.item

    #Update descriptor_uniques by getting new list of uniques from event and loaded_data.
    if user_ct != None:
        descriptor_uniques = get_list_uniques(loaded_data[loaded_data['Complaint Type'].str.contains(user_ct)], 'Descriptor')

def update_count(event):
    global user_desc

    user_desc = event.item
    print(user_desc)
    new_data = {}
    new_data["month"] = month_list
    new_data["test"] = get_count_list(loaded_data, user_ct, user_desc)
    plot_dataset.data = new_data

def get_list_uniques(given_df, given_category):
    unique_list = given_df[given_category].unique()

    return unique_list.tolist()

def main():

    global loaded_data, complaint_type_uniques, month_list, descriptor_uniques, user_ct, user_desc

    #Data prep section.
    month_list = get_month_names()
    loaded_data = load_df()
    complaint_type_uniques = get_list_uniques(loaded_data, 'Complaint Type')
    descriptor_uniques = get_list_uniques(loaded_data, 'Descriptor')

    test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    #Visualization section.
    dropdown = Dropdown(label="Complaint Type", menu=complaint_type_uniques)
    dropdown.on_event("menu_item_click", update_descriptor_list)

    dropdown2 = Dropdown(label="Complaint Cause", menu=descriptor_uniques)
    dropdown2.on_event("menu_item_click", print('button mashed'))

    p = figure(title="title",
               x_axis_label="months",
                y_axis_label="count",
               x_range=month_list
               )

    #Line plot for overall monthly mean.
    p.line(
        x="month",
        y="[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]",
        legend_label="legend",
        width=0.9,
        color="red",
    )

    curdoc().add_root(column(dropdown, dropdown2, p))

main()