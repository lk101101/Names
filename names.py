"""
This module works with baby name data from the US Census, baby name websites, and APIs.
It allows users to discover the popularity of a selected name,
generate random names (both first and last names),
retrieve information about name meanings, predicted gender, age, and nationality,
and create and build a list of favorite names.
"""
import os
from csv import reader
import random
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pycountry


def return_raw_data(filename):
    """
    Reads and returns the raw data from the provided file.

    input:
        filename: string of the filename of the file containing name data.
    ouput:
        list of strings for each line from the file.
    """

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)

    with open(full_path, 'r', encoding='utf-8-sig') as file_obj:
        raw_data = file_obj.readlines()
    return raw_data


def number_of_births(name, gender, raw_data):
    """
    Finds and returns the number of babies named a given name for a specified gender within the raw data.

    input:
        name: string, name to check the ranking of.
        gender: string, 'm' for male or 'f' for female.
        raw_data: list of strings, raw data from the names data file.
    output:
        string - the ranking of the given name if found; otherwise, returns 0.
    """
    for i in raw_data:
        separated = i.split(',')
        if separated[1].lower() == gender.lower() and separated[0] == name:
            return separated[2].strip('\n')
    return 0


# TODO: split into helper functions
def popularity(name, gender, year):
    """
    Parses user input, returns data for the inputted name, 
    and creates a visualization of the name's popularity.
    The user is prompted to enter a name, gender, and a year in the following format: 'name gender year'.
    """
    current_file = 'names_files/yob2020.txt'
    past_file = f'names_files/yob{year}.txt'

    if gender.lower() == 'f':
        full_gender = "girls"
    elif gender.lower() == 'm':
        full_gender = "boys"
    else:
        # TODO: better handle this case
        exit()

    cur_raw_data = return_raw_data(current_file)
    past_raw_data = return_raw_data(past_file)

    # get ranks from current and specified year
    cur_rank = number_of_births(name, gender, cur_raw_data)
    past_rank = number_of_births(name, gender, past_raw_data)

    print(
        f"The {full_gender} name {name} was used {cur_rank} times in 2020"
        f" and {past_rank} times in {year}")

    # ** visualization code **
    years = []
    ranks = []
    # gather the ranks for each year between the specified and current year
    # TODO - refactor to be more efficient
    # TODO - more efficient way to read in CSV files?
    for i in range(int(year), 2021):
        years.append(str(i))
        new_file = f'names_files/yob{str(i)}.txt'
        new_raw_data = return_raw_data(new_file)
        new_rank = number_of_births(name, gender, new_raw_data)

    # if name isn't in file, use 0 as rank
    # TODO: handle differently?
        if (new_rank is None):
            ranks.append(0)
        else:
            ranks.append(int(new_rank))

    viz(years, ranks, name, year)

# TODO: make visualization module


def viz(year_list, rank_list, name, year):
    # *change color of line here*
    plt.plot(year_list, rank_list, color='deepskyblue', marker='o')
    plt.ylabel('Popularity')
    plt.xlabel('Years')
    plt.title(f'Popularity of Name {name.capitalize()} from {year} to 2020')

    # add ranking labels to points on graph
    for x, y in zip(year_list, rank_list):
        plt.annotate(y, (x, y))
    plt.grid(True)
    plt.show()


def random_surname():
    """
    Selects and returns a random surname from the surnames file.

    Output:
        string (surname)
    """
    with open("2010CensusSurnames.csv", encoding='utf-8-sig') as f:
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
        return f"{first_name} {sur}"

    return first_name


def get_name_meaning(name, gender):
    """
    Scrapes NameBerry for the origin and meaning of the given name and prints the result.

    input:
        name: string.
        gender: string, 'boy' or 'girl'.
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
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
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
        name: string.
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
            country_name = pycountry.countries.get(alpha_2=country_code).name if pycountry.countries.get(
                alpha_2=country_code) else country_code
            prob_string = f"{
                country_name} - probability: {round(probability * 100, 2)}%"
            country_strings.append(prob_string)

    return 'Predicted nationality:'.join(country_strings)


def genderize(name):
    """
    Uses genderize.io API to predict and print the gender of a given name.

    input:
        name: string.
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
        name: A string. 
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
    """
    return [
        name.capitalize(),
        get_name_meaning(name, gender),
        *nationalize(name).split('\n'),
        genderize(name),
        agify(name)
    ]


options = {
    'p': popularity,
    'm': name_information,
}


def main():
    """
    Main function to retrieve input from user and execute the corresponding functions. 
    """

    done = False
    while (not done):
        answer = input("Select an option: r to return a random name, p to return the popularity ranking of a name,"
                       " m to return details about a name, s to save a favorite name, or f to exit: ")
        if answer in options:
            options[answer]()
        elif answer == 'f':
            done = True
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()
