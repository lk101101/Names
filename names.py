"""
This module works with baby name data from the US Census, baby name websites, and APIs.
Allows users to discover the popularity of a selected name,
generate random names (both first and last names), and
retrieve information about name meanings and predicted gender, age, and nationality. 
"""
import os
from csv import reader
import random
import requests
from bs4 import BeautifulSoup
import pycountry
import pandas as pd


def load_yearly_data(year, name, gender):
    """
    Loads data for a specific year, name, and gender from the baby names dataset.

    input:
        year: int
        name: string
        gender: string

    ouput:
        the number of births associated with the given name and gender for that year;
            0 if name isn't found
    """
    file_name = f'names_files/yob{year}.txt'
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                n, g, births = line.strip().split(',')
                if n.lower() == name.lower() and g.lower() == gender.lower():
                    return int(births)
    except FileNotFoundError:
        print(f"Data for the year {year} is not available.")
    return 0


def popularity(name, gender, start_year, end_year):
    """
    Returns the number of occurrences of a given name for each year within a given range.

    input: 
        name: string
        gender: string - 'm' for male or 'f' for female
        start_year: int
        end_year: int

    ouput:
        Pandas DataFrame
    """
    data = {'Year': [], 'Births': []}

    for year in range(start_year, end_year + 1):
        data['Year'].append(year)
        data['Births'].append(load_yearly_data(year, name, gender))

    return pd.DataFrame(data)


def random_surname():
    """
    Selects and returns a random surname from the surnames file.

    output:
        string (surname)
    """
    with open("names_files/2010CensusSurnames.csv", encoding='utf-8-sig') as f:
        csv_reader = reader(f)
        # skip first two rows in file
        # TODO: can use itertools to skip rows
        next(csv_reader)
        next(csv_reader)
        surnames = list(csv_reader)
        random_line = random.choice(surnames)
        sur = random_line[0].lower()
        return sur.capitalize()


def random_name(gender="", surname=False):
    """
    Generates and prints a random name with options to specify gender and add surname(s).

    input:
        gender: string ('m' or 'f'); default empty string ""
        surname: boolean; default False
    output:
        string: random first and/or last name
    """
    year = str(random.randrange(1880, 2020))
    file_name = f'names_files/yob{year}.txt'

    with open(file_name, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    if gender:
        lines = [line for line in lines if line.split(
            ',')[1].lower() == gender.lower()]

    cur_line = random.choice(lines)
    name_details = cur_line.strip().split(',')
    first_name = name_details[0]

    if surname:
        sur = random_surname()  # Assuming you have a random_surname function
        first_name += f" {sur}"

    return first_name


def get_name_meaning(name, gender):
    """
    Scrapes NameBerry for the origin and meaning of the given name and prints the result.

    input:
        name: string
        gender: string, 'boy' or 'girl'
    output:
        string containing scraped name meaning or error message
    """
    name = name.capitalize()
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
            + ' Chrome/56.0.2924.76 Safari/537.36'
    }

    try:
        r = requests.get("https://nameberry.com/b/" + gender + '-baby-name-' +
                         name, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.HTTPError:
        # return f"HTTP Error: {e}"
        return f"Error: No information found on NameBerry for {name}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request: {e}"

    soup = BeautifulSoup(r.text, 'html.parser')
    meaning = soup.find_all('div', {"class": "t-copy"})

    meaning_text = '\n'.join(sentence.get_text(
        strip=True) for sentence in meaning) if meaning else f'No information available for {name}.'
    return meaning_text


def nationalize(name):
    """
    Uses nationalize.io API to predict and print the nationality of a given name.

    input:
        name: string
    output:
        string containing predicted nationalities or error message
    """
    try:
        response = requests.get(
            f"https://api.nationalize.io?name={name}", timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request to the Nationalize API timed out."
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request to the Nationalize API: {e}"

    nationalities = response.json().get('country', [])
    if not nationalities:
        return "No nationality data available."

    country_strings = []
    for country in nationalities:
        country_code = country.get('country_id')
        probability = country.get('probability')
        if country_code and probability is not None:
            cur_country = pycountry.countries.get(alpha_2=country_code)
            country_name = cur_country.name if cur_country else country_code
            prob_string = f"{
                country_name} - probability: {round(probability * 100, 2)}%"
            country_strings.append(prob_string)

    return 'Predicted nationality:'.join(country_strings)


def genderize(name):
    """
    Uses genderize.io API to predict and print the gender of a given name.

    input:
        name: string
    output:
        string containing predicted gender or error message
    """

    try:
        response = requests.get(
            f"https://api.genderize.io?name={name}", timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request to the Genderize API timed out."
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request to the Genderize API: {e}"

    data = response.json()
    gender_info = f"Predicted gender: {data.get('gender', 'unknown')} - probability: {
        round(data.get('probability', 0) * 100, 2)}%"

    return gender_info


def agify(name):
    """
    Uses agify.io API to predict and print the age associated with a given name.

    input:
        name: string 
    output:
        string containing predicted age or error message
    """
    try:
        response = requests.get(
            f"https://api.agify.io?name={name}", timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e.response.status_code} {e.response.reason}"
    except requests.exceptions.Timeout:
        return "The request to the Agify API timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request to the Agify API: {e}"

    data = response.json()
    age = data.get('age', 'unknown')
    return f"Predicted age: {age}" if age != "unknown" else f"No age prediction for name {name}."


def name_information(name, gender):
    """
    Outputs a specified name's meaning and predicted gender, age, and nationality.

    input:
        name: string
        gender: string (either 'boy' or 'girl')
    output:
        array containing outputs from name meaning and predicted nationalities,
        age, and gender functions
    """
    return [
        name.capitalize(),
        get_name_meaning(name, gender),
        *nationalize(name).split('\n'),
        genderize(name),
        agify(name)
    ]
