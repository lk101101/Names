This program can:

1. return random first name(s) from random years with options to specify gender (m/f), number of names to generate, and whether to generate a surname.
2. retrieve information about a specified name's origin and meaning scraped from NameBerry.com as well as its predicted nationality, age, and gender gathered from the Nationalize.io, Genderize.io, and Agify.io APIs
3. create data visualizations to display the changes in a name's popularity throughout a specified range of years

## Data

The gather_data.py file downloads and scrapes the following data:

Social Security Adminstration (SSA) [annual name data](https://www.ssa.gov/oact/babynames/limits.html) from 1880 to the previous year under 'National data'
> more information about the [data qualifications](https://www.ssa.gov/oact/babynames/background.html) 

SSA [number of SS card holders by year of birth and sex](https://www.ssa.gov/oact/babynames/numberUSbirths.html)
> note: not currently used in code but may be used in the future to visualize the relative popularity of names over time

US Census Bureau [Top 1000 surnames](https://www.census.gov/topics/population/genealogy/data/2010_surnames.html)

# Overview
<img width="653" alt="Screenshot 2024-07-07 at 12 03 51 AM" src="https://github.com/lk101101/Names/assets/55768135/4676ff10-2f3e-446c-bcd4-37f6dce78512">

## Generating random names
<img width="1163" alt="Screenshot 2024-07-07 at 12 05 07 AM" src="https://github.com/lk101101/Names/assets/55768135/3c810ff6-c03d-4ef2-b544-136a8f710074">

This feature returns a specified number of random names with options to limit the gender to male or female and generate random surnames. 

## Get name information
TODO


## Create visualizations of a name's popularity
TODO


# How to Download and Run Code

- In your Terminal, run `git clone https://github.com/lk101101/Names` to clone this repo into your directory
- Navigate to the new folder called Names
- Create a Python environment (i.e. `python -m venv env`, then `source env/bin/activate`)
- Download required packages: `pip install -r requirements.txt`
- Download and unzip required datasets: `python gather_data.py`(see 'Data'). The `names_files` folder contains a small sample of the data.
- Run `flask run` to start the Flask server.
- Navigate to `http://127.0.0.1:5000` in your web browser.
