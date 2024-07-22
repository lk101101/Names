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
<img width="1187" alt="image of webpage to generate random name featuring a completed query and list of random names" src="https://github.com/user-attachments/assets/9a230d4e-0099-4c1b-a45e-0e8b7653f8f5">


Return a specified number of random names with options to limit the gender to male or female and to generate random surnames.

## Get name information
<img width="1166" alt="image of webpage to retrieve name information" src="https://github.com/user-attachments/assets/fb5a18f2-8ac3-42ba-ba43-a1d31028dda8">
<img width="1152" alt="image of completed query for name information about the name Emma Smith" src="https://github.com/user-attachments/assets/79d287af-8373-4471-a41f-60251b9d163a">
<img width="1162" alt="image of predicted nationality, age, and gender of the name Emma Smith" src="https://github.com/user-attachments/assets/8496a4d6-c4b5-4cbc-9c66-347e3421a851">
<img width="1064" alt="image of visualization displaying predicted nationalities on map with countries in different colors" src="https://github.com/user-attachments/assets/dc436ba0-dfb3-463a-a3c6-c40e420bfc3c">




Enter either a first name or a full name (first and last) to gather information about a name from [Nameberry](https://nameberry.com/) and retrieve the name's predicted nationalities, gender, and age using the [Nationalize](https://nationalize.io/documentation), [Genderize](https://genderize.io/documentation), and [Agify](https://agify.io/documentation) APIs. The predicted nationalities are highlighted on a world map.

> note: Nationalize uses last names while the other APIs use first names. If a last name is not provided, the code will use the first name which may lead to inaccurate predictions.

## Create visualizations of a name's popularity
<img width="1155" alt="image of webpage to visualize name popularity" src="https://github.com/user-attachments/assets/fb373101-f5f3-4758-88cb-c37cb3da9dec">
<img width="711" alt="image of scatterplot and heatmap for the popularity of the name Emma" src="https://github.com/user-attachments/assets/1737adcc-7186-45db-8b4f-539073694c76">

Enter a first name, gender, start year, and end year to visualize the popularity (number of babies with that name each year in the given range) with a scatterplot and a heatmap.

# How to Download and Run Code

- In your Terminal, run `git clone https://github.com/lk101101/Names` to clone this repo into your directory
- Navigate to the new folder called Names
- Create a Conda environment from environment.yml file: `conda env create -f environment.yml`, then `conda activate abc`. A requirements.txt file is also provided.
- Download and unzip required datasets: `python gather_data.py`(see 'Data' for more information).
- Run `flask run` to start the Flask server.
- Navigate to `http://127.0.0.1:5000` in your web browser.
