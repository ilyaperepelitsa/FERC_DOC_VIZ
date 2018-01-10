import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import numpy as np

raw_data = pd.read_csv("~/quant/FERC/FERC/download_folder/log.csv")
data1.info()
data1['document_date'] = pd.to_datetime(data1['document_date'])
data1.document_date = data1.document_date.map(lambda x: x.strftime('%Y-%m'))
# data1.document_date = data1.document_date.map(lambda x: x.strftime('%Y'))
# data1.document_date = data1.document_date.map(lambda x: x.strftime('%m'))

# data1.info()

data1.groupby(['document_date', "correspondent_author_organization"]).size().reset_index(name='counts')
plot_data = data1.groupby(['document_date']).size().reset_index(name='counts')
plot_data
pd.to_datetime(df['time'])
# y = [3, 10, 7, 5, 3, 4.5, 6, 8.1]
# N = len(y)
# x = range(N)
# plot_data[['document_date']] = plot_data[['document_date']].astype(int)
plot_data[['counts']] = plot_data[['counts']].astype(float)
plot_data.info()
import datetime
datetime.datetime.strptime(raw_data['document_date'].min(), "%m/%d/%Y")
raw_data['document_date'].min()

def plot_docs(data_in, agg_period):

    data = pd.DataFrame.copy(data_in)
    data['document_date'] = pd.to_datetime(data['document_date'])

    keycolor = "#232626"
    barcolor = "#bc9195"

    date_start = data['document_date'].min().strftime('%B %d, %Y')
    date_end = data['document_date'].max().strftime('%B %d, %Y')

    if agg_period == "month":

        title_label = "Monthly"

        data.document_date = data.document_date.map(lambda x: x.strftime('%Y-%m'))
        plot_data = data.groupby(['document_date']).size().reset_index(name='counts')

        objects = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%b'))
        objects_years = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%Y'))

        for ind, val in enumerate(objects):
            if val == "Jan":
                objects[ind] = val + "\n" + objects_years[ind]

    elif agg_period == "year":

        title_label = "Annual"

        data.document_date = data.document_date.map(lambda x: x.strftime('%Y'))
        plot_data = data.groupby(['document_date']).size().reset_index(name='counts')

        objects = pd.to_datetime(plot_data['document_date']).map(lambda x: x.strftime('%Y'))




    y_pos = np.arange(len(objects))
    doc_counts = plot_data['counts']

    matplotlib.rc('axes', edgecolor = keycolor)
    # matplotlib.axis.XAxis.grid(color="r", linestyle="-", linewidth=2)
    #
    # fig, ax = plt.subplots()
    # matplotlib.axes.Axes.grid(color='r', linestyle='-', linewidth=2)
    fig = plt.figure(figsize=(14,5))
    plt.bar(y_pos, doc_counts, align='center', color = barcolor,
                    alpha=1, zorder = 3)
    plt.xticks(y_pos, objects, color = keycolor)
    plt.yticks(color = keycolor)
    # print(plt.yticks())
    # plt.xticks([3], [333])
    plt.ylabel('Number of document accessions per %s' % (agg_period), color = keycolor)
    # plt.title('Millenium Pipeline Documents')
    plt.suptitle('Millenium Pipeline Documents, %s total' % (title_label), y = 1.05, x = 0.2,
                                    fontsize=18, color = keycolor)
    plt.title('All document accessions provided by FERC library from %s to %s.' %
                                    (date_start , date_end),
                                    x = 0.4, y = 1.05, fontsize=14, color = keycolor)
    # plt.yaxis.grid()
    plt.gca().yaxis.grid(True, linewidth=1, alpha = 0.2, zorder=0)
    # ax.yaxis.grid(True)
    # plt.autoscale(enable=True, axis='both', tight=None)

    plt.show()


plot_docs(data_in = raw_data, agg_period = "month")
plot_docs(data_in = raw_data, agg_period = "year")

for ind, val in enumerate(objects):
    if val == "Jan":
        print(val)
        # val = val + "\n" + "pew"

objects

width = 1/1.5
plt.bar(plot_data['document_date'], plot_data['counts'], width, color="blue")
plt.show()
data = pd.read_csv("~/Downloads/h1b_kaggle.csv")
data.info()
data.head()



data['crawled'] = pd.to_datetime(data['crawled'])
n_bins = 20
plt.hist(x = data['crawled'], bins=n_bins)
data.groupby([data['crawled'].dt.year, data['crawled'].dt.month]).count().plot(kind="bar")
plt.show()


df2 = data.loc[:,["spam_score", "crawled"]]
df2

df2.crawled = df2.crawled.map(lambda x: x.strftime('%Y-%m'))
df2.info()

df2.groupby(['crawled']).size().reset_index(name='counts')

bygroup_treatment = data.groupby(['YEAR'])
bygroup_treatment["YEAR"].agg([len])
