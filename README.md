# Under construction! Adding Flask functionality 🚧

## Overview

The US Social Security Administration (SSA) publishes annual lists of baby names used during that year. This program can:

1. return random first name(s) from a random year with options to specify gender (m/f), number of names to generate, and whether to generate a surname
2. retrieve information about a specified name's origin and meaning scraped from NameBerry.com as well as its predicted nationality, age, and gender gathered from the Nationalize.io, Genderize.io, and Agify.io APIs
3. Creates data visualizations to display the changes in a name's popularity throughout a specified range of years

Currently, the only options for gender are male (m) and female (f).
For all of the annual datasets (CSV files ranging all the way to 1880), download 'National data' on the SSA site: https://www.ssa.gov/oact/babynames/limits.html . I have included the files for the years 2000 and 2020 in 'name_files' folder.

For full list of surnames from 2010 Census, download the Excel file on https://www.census.gov/topics/population/genealogy/data/2010_surnames.html . I have included a small sample CSV file for the top 20 surnames but the complete file has 65k+ surnames.

# How to Download and Run Code

In your Terminal, run ' git clone https://github.com/lk101101/Names ' to clone this repo into your directory. Navigate to the new folder called Names. Create a Python environment (i.e. 'python -m venv env', then 'source env/bin/activate') and run 'pip install -r requirements.txt' to download the required packages. Run 'flask run' to start the Flask server and navigate to http://127.0.0.1:5000 in your web browser. 
