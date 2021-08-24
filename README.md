# Try it out on Replit: https://replit.com/@lk101/Names#main.py

## Overview
The US Social Security Administration (SSA) publishes annual lists of baby names used during that year. This program can:
1. process the data from the most recent SSA dataset (2020) and the dataset from specified year (choice 'p')
2. print number of babies named with specified name in specified year and current year (choice 'p')
3. display a line graph visualizing the change in popularity from specified year to current year (choice 'p')
4. return a random first and/or last name from a random year (choice 'r') with options to specify gender (m/f) and number of names to generate
5. print information about a given name from BabyNames.com (choice 'm')
6. save favorite names to CSV file and print all names from file (choice 's')

Currently, the only options for gender are male (m) and female (f) so retrieving data for gender neutral names would require two searches.
For all of the annual datasets (ranging all the way to 1880), download 'National data' on the SSA site:  https://www.ssa.gov/oact/babynames/limits.html

For full list of surnames from 2010 Census, download the Excel file on https://www.census.gov/topics/population/genealogy/data/2010_surnames.html . I have included a small sample CSV file for the top 20 surnames but the complete file has 65k+ surnames.

# Examples

## Choice r: return random names
"Specify a gender (m/f) and/or number of names to generate (>1) and/or whether to include a random surname (s). Leave blank for a single random name"\
Note: inputs must be in the order |gender, number, surname| even if not all parameters are included. See more examples in the code.

Input: f\
Output: 2010: F Emma

Input: f s\
Output: 2010: F Emma Smith

Input: s\
Output: Smith

## Choice p: return the popularity ranking of a name
"Enter as name gender (m/f) year"\
Input: emma f 2010\
Output: The girls' name Emma was used 15581 times in 2020 and 17351 times in 2010

<img width="1149" alt="example_graph" src="https://user-images.githubusercontent.com/55768135/123728282-027b6280-d861-11eb-8a3b-0a50c28ecad2.png">

## Choice m: return information about a name
"Enter a name to return its origin and meaning"\
Input: emma\
Output: info scraped from BabyNames.com webpage for the name Emma

## Choice s: save favorite names to CSV file and print all names
"Enter a name in format 'name gender'py to save it or enter 'print' to return your favorite names so far"\
Input (save name): emma f\
Output: Saved!

Input (print names): print\
Output: Emma, f

Note: This feature uses the CSV file 'Fav_Names.csv'

# How to Download and Run Code
In your Terminal, navigate to your preferred directory. Next, type or copy and paste ' git clone https://github.com/lk101101/Names ' to clone this repo into your directory. Navigate to the new folder, named Names. Enter ' python baby_names.py ' to run the code. 

## TO DO
* implement better command line argument handling
* allow for more search criteria such as name length, initial, certain level of popularity, etc.
* web scraping BabyNames.com is a bit messy, so replace with another baby name website
