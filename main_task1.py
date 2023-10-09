import random
from pathlib import Path
import pandas as pd
import math

from bokeh.layouts import column
from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource

# [1] = created date
# [5] = complaint type
# [6] = descriptor

loaded_data, complaint_type_uniques, month_list, descriptor_uniques, user_ct, user_desc = None, None, None, None, None, None

#plot_dataset = ColumnDataSource(dict(month=[], count=[]))

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

def get_count_list(given_df, descriptor_selection):
    count =[]

    if descriptor_selection == '':
        #Get the count of rows according to the descriptor and month.
        for i in range(1, 13):
            #Get the number of rows for each month that matches the descriptor_selection.
            count_df = given_df[(given_df['Month'] == i)]

            #Append count of rows to count list.
            if len(count_df) == 0:
                count.append(0)
            else:
                count.append(math.log(len(count_df)))
                #count.append(len(count_df))

    else:
        #Get the count of rows according to the descriptor and month.
        for i in range(1, 13):
            #Get the number of rows for each month that matches the descriptor_selection.
            count_df = given_df[(given_df['Month'] == i) & (given_df['Descriptor'] == descriptor_selection)]

            #Append count of rows to count list.
            if len(count_df) == 0:
                count.append(0)
            else:
                count.append(math.log(len(count_df)))
                #count.append(len(count_df))

    #Get highest value in count list and divide by its lowest value.
    max_count = max(count)
    for i in range(len(count)):
        count[i] = count[i] / max_count


    return count

def update_count(event):

    new_data = {}
    new_data['month'] = month_list
    new_data['count'] = get_count_list(loaded_data, event.item)

    #Update the plot_dataset.
    plot_dataset.data = new_data

def get_list_uniques(given_df, given_category):
    unique_list = given_df[given_category].unique()

    return unique_list.tolist()

def main():

    global loaded_data, complaint_type_uniques, month_list, descriptor_uniques

    #Data prep section.
    month_list = get_month_names()
    loaded_data = load_df()
    complaint_type_uniques = get_list_uniques(loaded_data, 'Complaint Type')
    descriptor_uniques = get_list_uniques(loaded_data, 'Descriptor')

    #Visualization section.
    dropdown = Dropdown(label="Complaint Causes", menu=descriptor_uniques)
    dropdown.on_event("menu_item_click", update_count)

    p = figure(title="Magnitude-Adjusted Natural Log of Complaint Cause Counts by Month",
                x_axis_label="Month of 2020",
                y_axis_label="Natural log of Complaints (ln max value / ln monthly value)",
                x_range=month_list,
                width=1400,
               )

    color = ["red", "blue", "green", "orange", "purple", "black"]

    total_complaints = get_count_list(loaded_data, '')

    # Line plot for overall monthly mean.
    # p.line(
    #     x="month",
    #     y="count",
    #     source=plot_dataset,
    #     legend_label="legend",
    #     width=0.9,
    #     color="red",
    # )

    p.line(
        x=month_list,
        y=total_complaints,
        legend_label='Total # of Noise Complaints',
        width=1.1,
        color="red",
    )

    ignored = ['']

    for complaint_cause in descriptor_uniques:
        #Get the length of the dataframe that matches the complaint_cause.
        temp_df = loaded_data[loaded_data['Descriptor'] == complaint_cause].copy()
        length = int(len(temp_df))
        bool_length = (length >= 500)
        if(bool_length):
            print(complaint_cause)
            p.line(
                x=month_list,
                y=get_count_list(loaded_data, complaint_cause),
                legend_label=complaint_cause,
                width=0.9,
                color=random.choice(color)
            )


    curdoc().add_root(column(dropdown, p))

main()