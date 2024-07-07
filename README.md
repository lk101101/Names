## Overview

This program can:

1. return random first name(s) from random years with options to specify gender (m/f), number of names to generate, and whether to generate a surname.
2. retrieve information about a specified name's origin and meaning scraped from NameBerry.com as well as its predicted nationality, age, and gender gathered from the Nationalize.io, Genderize.io, and Agify.io APIs
3. create data visualizations to display the changes in a name's popularity throughout a specified range of years

## Data

The gather_data.py file downloads and scrapes the following data:

Social Security Adminstration (SSA) annual name data from 1880 - previous year ('National data'): https://www.ssa.gov/oact/babynames/limits.html

SSA number of SS card holders by year of birth and sex (not currently used in code): https://www.ssa.gov/oact/babynames/numberUSbirths.html

US Census Bureau Top 1000 surnames: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html

# How to Download and Run Code

- In your Terminal, run ' git clone https://github.com/lk101101/Names ' to clone this repo into your directory.
- Navigate to the new folder called Names.
- Create a Python environment (i.e. 'python -m venv env', then 'source env/bin/activate') and run 'pip install -r requirements.txt' to download the required packages.
- Run 'python gather_data.py' to download the required datasets (see 'Data'). The names_files folder contains a small sample of the data.
- Run 'flask run' to start the Flask server and navigate to http://127.0.0.1:5000 in your web browser.
