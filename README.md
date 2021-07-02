## Overview
The US Social Security Administration (SSA) publishes annual lists of baby names used during that year. This program can:
1. process the data from the most recent dataset (2020) and the dataset from specified year
2. print number of babies named with specified name in specified year and current year
3. display a line graph visualizing the change in popularity from specified year to current year (choice 'p')
4. return a random name from a random year (choice 'r') with options to specify gender (m/f) and number of names to generate
5. print information about a given name from BabyNames.com (choice 'm')

Currently, the only options for gender are male (m) and female (f) so retrieving data for gender neutral names would require two searches.
For all of the annual datasets (ranging all the way to 1880), download 'National data' on the SSA site:  https://www.ssa.gov/oact/babynames/limits.html

## Choice r: return a random word
"Specify a gender (m/f) and/or number of names to generate (>1) and/or whether to include a random surname (s). Leave blank for a single random name"
Note: inputs must be in order gender, number, surname even if not all parameters are included. More examples in code./
Input: f\
Output: 2010: F Emma

## Choice p: return the popularity ranking of a name
"Enter as name gender (m/f) year"\
Input: emma f 2010\
Output: The girls' name Emma was used 15581 times in 2020 and 17351 times in 2010

<img width="1149" alt="example_graph" src="https://user-images.githubusercontent.com/55768135/123728282-027b6280-d861-11eb-8a3b-0a50c28ecad2.png">

## Choice m: return information about a name
"Enter a name to return its origin and meaning"\
Input: emma\
Output: info scraped from BabyNames.com


## TO DO
Planning to implement options to generate full names including last names.
