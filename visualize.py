import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
import re
import datetime
import os


# Path to the FERC project, has to be in the same directory as this repository
ferc_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "FERC_DOC_TRAIL", "FERC", "download_folder")

# Path to the current project
base_folder = os.path.dirname(os.path.abspath(__file__))

# Create the exhibits folder if it doesn't exist already
exhibits_folder = os.path.join(base_folder, "exhibits")
if os.path.exists(exhibits_folder):
    pass
else:
    os.mkdir(exhibits_folder)

# Path to FERC log file
# data_path = os.path.join(ferc_folder, "log.csv")
data_path = os.path.join("~/Downloads/", "log.csv")

# Read the log file
raw_data = pd.read_csv(data_path)

# Convert date column to date format
raw_data['document_date'] = pd.to_datetime(raw_data['document_date'])

# Make the list of accession numbers listed as "children" and
# drop those accessions from the log
child_accessions = [", ".join(pew) for pew in raw_data["document_child_list"].str.findall("(\d{3,}-\d{3,})\s") if type(pew) is list]
child_accessions = [accession_list.strip() for accession_string in child_accessions for accession_list in accession_string.split(",")]
for pattern in child_accessions:
    raw_data = raw_data[~raw_data["accession_number"].str.contains(pat=pattern)]


# Define the graph plotting functions
# Aggregate the number of observations by date (by year/ year+month)
# Takes regular dataframe as argument
def plot_docs(data_in, agg_period):

    # Create a copy of DataFrame
    data = pd.DataFrame.copy(data_in)
    # Convert date column to date format
    data['document_date'] = pd.to_datetime(data['document_date'])

    # Define plot colors
    keycolor = "#232626"
    barcolor = "#bc9195"

    # Define min and max date for date range in the subtitle
    date_start = data['document_date'].min().strftime('%B %d, %Y')
    date_end = data['document_date'].max().strftime('%B %d, %Y')

    # Monthly arguments for plotting
    if agg_period == "month":
        # Title part that reflects what aggregation is used
        title_label = "Monthly"
        # Convert date to year-month
        data.document_date = data.document_date.map(lambda x: x.strftime('%Y-%m'))
        # Row count grouped by date
        plot_data = data.groupby(['document_date']).size().reset_index(name='counts')
        # Months to be plotted
        objects = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%b'))
        # Years for those months as separate list
        objects_years = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%Y'))
        # Append each January with the corresponding year so that months stay
        # clean. Plot the year text only when the new year starts
        for ind, val in enumerate(objects):
            if val == "Jan":
                objects[ind] = val + "\n" + objects_years[ind]

    # Annual arguments for plotting
    elif agg_period == "year":
        # Title part that reflects what aggregation is used
        title_label = "Annual"
        # Convert date to years
        data.document_date = data.document_date.map(lambda x: x.strftime('%Y'))
        # Row count grouped by date
        plot_data = data.groupby(['document_date']).size().reset_index(name='counts')
        # Years to be plotted
        objects = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%Y'))



    # Create the xticks
    x_pos = np.arange(len(objects))
    # The height of columns
    doc_counts = plot_data['counts']
    # Plot axes
    matplotlib.rc('axes', edgecolor = keycolor)
    # Plot figure
    fig = plt.figure(figsize=(14,5))
    # Plot the column graph
    plt.bar(x_pos, doc_counts, align='center', color = barcolor,
                    alpha=1, zorder = 3)
    # Plot X ticks
    plt.xticks(x_pos, objects, color = keycolor)
    # Plot Y ticks
    plt.yticks(color = keycolor)

    # Y axis label
    plt.ylabel('Number of document accessions per %s' % (agg_period), color = keycolor,
                fontsize=12)

    # Graph title
    plt.suptitle('Millenium Pipeline Documents, %s total' % (title_label), y = 1.05,
                                    fontsize=18, color = keycolor,
                                    horizontalalignment = "right")

    # Graph subtitle
    plt.title('All document accessions provided by FERC library from %s to %s.' %
                                    (date_start , date_end),
                                    y = 1.05, fontsize=14, color = keycolor,
                                    loc = "left")
    # Plot the semi-transparent grid
    plt.gca().yaxis.grid(True, linewidth=1, alpha = 0.2, zorder=0)

    # Path to save the graph
    image_path = os.path.join(exhibits_folder, agg_period + ".png")

    # Save the graph
    plt.savefig(filename = image_path, transparent = False,
                    format = "png", dpi = 300, bbox_inches='tight')
    # plt.show()


# Plot and save graphs for year-month aggregation and for monthly aggregation
plot_docs(data_in = raw_data, agg_period = "month")
plot_docs(data_in = raw_data, agg_period = "year")

# Create filenames that would correspond to each date format
for date_format in ["%Y-%m", "%Y", "%b"]:
    if date_format == "%Y-%m":
        subheader = "year_month"
    elif date_format == "%Y":
        subheader = "annual"
    elif date_format == "%b":
        subheader = "month_pseudoseasonal"
    # Copy the dataset
    table_data = raw_data.copy()
    # Convert date column to date format
    table_data.document_date = table_data.document_date.map(lambda x: x.strftime(date_format))
    # Enforce uniform formatting for organizations
    table_data['correspondent_author_organization'] = table_data['correspondent_author_organization'].map(lambda x: x.title())
    # Change some organizations name duplicates to common format
    table_data = table_data.replace({"correspondent_author_organization" : {"New York State Department Of Environmental Conservation" :
                                                            "New York State Department Of Environmental Conversation",
                                                        "Millennium Pipeline Company L.L.C." :
                                                        "Millennium Pipeline Company, L.L.C.",
                                                    "New York, State Of" :
                                                    "New York State",
                                                "State Of New York" :
                                                "New York State",
                                                "Energy Projects, Office Of" :
                                                "Office Of Energy Projects",
                                                "Njr Energy Services Company" :
                                                "NJR Energy Services Company"}})
    # Capitalize FERC
    table_data["correspondent_author_organization"] = table_data["correspondent_author_organization"].map(lambda x: x.replace("Ferc", "FERC"))
    # Capitalize and punctuate LLC
    table_data["correspondent_author_organization"] = table_data["correspondent_author_organization"].map(lambda x: x.replace("Llc", "L.L.C."))
    # Group by date and organization and count rows
    table_data = table_data.groupby(['document_date', "correspondent_author_organization"]).agg("size").reset_index(name='counts')
    # Pivot table
    table_data = table_data.pivot_table(index='correspondent_author_organization', columns='document_date', values='counts')
    # table_data = table_data.fillna(0)
    # Create the total column
    table_data["Total"] = table_data.sum(1)
    # Sort by total
    table_data = table_data.sort_values("Total", ascending = False)
    # Create a column-wise sum row
    column_total = table_data.sum(0)
    column_total.name = "\t\t\tTotal"
    # Append the row to data frame
    table_data = table_data.append(column_total)

    # Define the order for month columns (no year) to avoid alphabetic order
    if date_format == "%b":
        months = {datetime.datetime(2000,i,1).strftime("%b"): i for i in range(1, 13)}
        months = list(pd.DataFrame.from_dict(months, orient = "index").index)
        months.append("Total")
        table_data = table_data[months]

    # Write the table

    exhibits_author_folder = os.path.join(exhibits_folder, "author_org")
    if os.path.exists(exhibits_author_folder):
        pass
    else:
        os.mkdir(exhibits_author_folder)


    table_data.to_csv(os.path.join(exhibits_author_folder, subheader + "_aggregate.csv"))



for date_format in ["%Y-%m", "%Y", "%b"]:
    if date_format == "%Y-%m":
        subheader = "year_month"
    elif date_format == "%Y":
        subheader = "annual"
    elif date_format == "%b":
        subheader = "month_pseudoseasonal"
    # Copy the dataset
    table_data = raw_data.copy()
    # Convert date column to date format
    table_data.document_date = table_data.document_date.map(lambda x: x.strftime(date_format))
    # Drop rows with NA's
    table_data = table_data[~table_data['correspondent_recipient_organization'].isnull()]
    # Enforce uniform formatting for organizations
    table_data['correspondent_recipient_organization'] = table_data['correspondent_recipient_organization'].map(lambda x: x.title())
    # Change some organizations name duplicates to common format
    table_data = table_data.replace({"correspondent_recipient_organization" : {"New York State Department Of Environmental Conservation" :
                                                            "New York State Department Of Environmental Conversation",
                                                        "Millennium Pipeline Company L.L.C." :
                                                        "Millennium Pipeline Company, L.L.C.",
                                                    "New York, State Of" :
                                                    "New York State",
                                                "State Of New York" :
                                                "New York State",
                                                "Energy Projects, Office Of" :
                                                "Office Of Energy Projects",
                                                "Njr Energy Services Company" :
                                                "NJR Energy Services Company"}})
    # Capitalize FERC
    table_data["correspondent_recipient_organization"] = table_data["correspondent_recipient_organization"].map(lambda x: x.replace("Ferc", "FERC"))
    # Capitalize and punctuate LLC
    table_data["correspondent_recipient_organization"] = table_data["correspondent_recipient_organization"].map(lambda x: x.replace("Llc", "L.L.C."))
    # Group by date and organization and count rows
    table_data = table_data.groupby(['document_date', "correspondent_recipient_organization"]).agg("size").reset_index(name='counts')
    # Pivot table
    table_data = table_data.pivot_table(index='correspondent_recipient_organization', columns='document_date', values='counts')
    # table_data = table_data.fillna(0)
    # Create the total column
    table_data["Total"] = table_data.sum(1)
    # Sort by total
    table_data = table_data.sort_values("Total", ascending = False)
    # Create a column-wise sum row
    column_total = table_data.sum(0)
    column_total.name = "\t\t\tTotal"
    # Append the row to data frame
    table_data = table_data.append(column_total)

    # Define the order for month columns (no year) to avoid alphabetic order
    if date_format == "%b":
        months = {datetime.datetime(2000,i,1).strftime("%b"): i for i in range(1, 13)}
        months = list(pd.DataFrame.from_dict(months, orient = "index").index)
        months.append("Total")
        table_data = table_data[months]

    exhibits_recipient_folder = os.path.join(exhibits_folder, "recipient_org")
    if os.path.exists(exhibits_recipient_folder):
        pass
    else:
        os.mkdir(exhibits_recipient_folder)

    # Write the table
    table_data.to_csv(os.path.join(exhibits_recipient_folder, subheader + "_aggregate.csv"))
