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
<img width="653" alt="image of homepage containing page links to generate names, retrieve name information, and visualize a name's popularity" src="https://github.com/lk101101/Names/assets/55768135/4676ff10-2f3e-446c-bcd4-37f6dce78512">

## Generating random names
<img width="1163" alt="image of webpage to generate random name featuring a completed query and list of random names" src="https://github.com/lk101101/Names/assets/55768135/3c810ff6-c03d-4ef2-b544-136a8f710074">

Return a specified number of random names with options to limit the gender to male or female and to generate random surnames. 

## Get name information
<img width="979" alt="image of webpage to retrieve name information featuring a completed query for Emma Smith and a paragraph about the name Emma" src="https://github.com/lk101101/Names/assets/55768135/14d0f553-86d6-4d35-9db0-05d09bad510d">
<img width="1022" alt="image of webpage to retrieve name information featuring list of predictions of the name's nationality, age, and gender along with a world map" src="https://github.com/lk101101/Names/assets/55768135/6622f554-a44a-4cf4-9e10-422c2e353340">

Enter either a first name or a full name (first and last) to gather information about a name from [Nameberry](https://nameberry.com/) and retrieve the name's predicted nationalities, gender, and age using the [Nationalize](https://nationalize.io/documentation), [Genderize](https://genderize.io/documentation), and [Agify](https://agify.io/documentation) APIs. The predicted nationalities are highlighted on a world map.
> note: Nationalize uses last names while the other APIs use first names. If a last name is not provided, the code will use the first name which may lead to inaccurate predictions.

## Create visualizations of a name's popularity
<img width="703" alt="image of webpage to visualize name popularity featuring a scatterplot and a heatmap" src="https://github.com/lk101101/Names/assets/55768135/19a6fbcd-1e75-4d98-a234-1b2a44070b2e">

Enter a first name, gender, start year, and end year to visualize the popularity (number of babies with that name each year in the given range) with a scatterplot and a heatmap. 


# How to Download and Run Code

- In your Terminal, run `git clone https://github.com/lk101101/Names` to clone this repo into your directory
- Navigate to the new folder called Names
- Create a Python environment (i.e. `python -m venv env`, then `source env/bin/activate`)
- Download required packages: `pip install -r requirements.txt`
- Download and unzip required datasets: `python gather_data.py`(see 'Data'). The `names_files` folder contains a small sample of the data.
- Run `flask run` to start the Flask server.
- Navigate to `http://127.0.0.1:5000` in your web browser.
