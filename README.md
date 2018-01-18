# FERC Document Trail Visualization
#### Grant Project funded by the Fund for Multimedia Documentation
#### of Engaged Learning, The New School.
#### Project supervisor: Stephen Metts

## General Information

The purpose of this project is to visualize the document trail scraped from
the Federal Energy Regulatory Commission's
([FERC](https://elibrary.ferc.gov/idmws/search/fercgensearch.asp)) library.

This project is installed along with **FERC_DOC_TRAIL** repository - it uses
**FERC_DOC_TRAIL**'s output and relies on full execution of all steps of
**FERC_DOC_TRAIL**.

## Installation

Clone the repository the regular way of cd'ing into a directory of choice and
issuing the regular git clone command. This repository has to be cloned to the
same directory as **FERC_DOC_TRAIL**, as seen on the picture:

![directory image](https://i.imgur.com/l27RBwP.png "directory image")


```
cd Users/username
git clone https://github.com/ilyaperepelitsa/FERC_DOC_VIZ.git
cd FERC_DOC_VIZ
```

This visualization and analysis project relies on several Python libraries:
* [Matplotlib](https://matplotlib.org/index.html) for graphing data. Type the following
to install:
```
python3 -mpip install matplotlib
```

* [Pandas](https://pandas.pydata.org) for tabular data analysis. Type the following
to install:
```
pip3 install pandas
```

* [Numpy](http://www.numpy.org) for basic scientific computing. Type the following
to install:
```
pip3 install matplotlib
```

## Setup
This project has been optimized to filter and analyze the data gathered for **CP16-17**
docket. It replaces certain actors' names (there are typos and alternative ways of
writing that were found for some actors, i.e. LLC/L.L.C. etc.) and adjusts
other minor details. We will provide instructions on how to modify this file in the
future, however currently it satisfies only the needs of monitoring **CP16-17**.
You have already navigated into the directory in the previous section.


## Launch
To run the script you need to issue the following command in the terminal:

```
python3 visualize.py
```

## Assets created
The script creates a folder called **exhibits** within itself. It saves two
graphs in this directory and creates folders for tables. Currently tables include
pivot tables of total counts of document accessions by two fields:
* Author Organization
* Recipient Organization

It groups the observations by organizations and a date which is represented in following formats:
* Month-Year
* Year
* Month (to explore potential seasonal trends, i.e. whether there have been more
  accessions towards the end of the year)
