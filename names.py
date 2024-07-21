"""
Use baby name data from the government, name websites, and APIs.
Allows users to discover the popularity of a selected name,
generate random names (both first and last names), and
retrieve information about name meanings and
predicted gender, age, and nationality.
"""
import os
from csv import reader
import random
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import pycountry
import pandas as pd


def load_yearly_data(year, name, gender):
    """
    Load data for a specific year, name, and gender from the names dataset.

    input:
        year: int
        name: string
        gender: string

    ouput:
        number of births associated with given name and gender for that year;
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
    Return the number of occurrences of a given name
    for each year within a given range.

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
    Select random surname from the surnames file.

    output:
        string (surname)
    """
    with open("names_files/surnames.csv", encoding='utf-8-sig') as f:
        csv_reader = reader(f)
        # skip first 3 rows in file
        for _ in range(3):
            next(csv_reader)

        total_surnames = list(csv_reader)

        # ignore last 3 rows of file
        random_line = random.choice(total_surnames[:-3])
        surname = random_line[0].lower()
        return surname.capitalize()


def random_name(gender="", surname=False):
    """
    Generate random name with options to 
    specify gender and generate random surname.

    input:
        gender: string ('m' or 'f'); default empty string ""
        surname: boolean; default False
    output:
        string: random first and/or last name(s)
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
    full_name = name_details[0]

    if surname:
        sur = random_surname()
        full_name += f" {sur}"

    return full_name


def get_name_meaning(name, gender):
    """
    Scrape NameBerry for the origin and meaning
    of the given name.

    input:
        name: string
        gender: string, 'boy' or 'girl'
    output:
        string containing scraped name meaning or error message
    """
    name = name.capitalize()
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64)' +
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
            + ' Chrome/56.0.2924.76 Safari/537.36'
    }

    try:
        r = requests.get("https://nameberry.com/b/" + gender + '-baby-name-' +
                         name, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.HTTPError:
        return f"Error: No information found on NameBerry for {name}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request: {e}"

    soup = BeautifulSoup(r.text, 'html.parser')
    meaning = soup.find_all('div', {"class": "t-copy"})

    meaning_text = (
        '\n'.join(
            sentence.get_text(strip=True) for sentence in meaning
        )
        if meaning
        else f'Error: No information available for {name}.'
    )
    return meaning_text


def nationalize(name):
    """
    Use nationalize.io API to predict nationality of a given name (recommended to use last names).

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
        return f"An error occurred (Nationalize API): {e}"

    nationalities = response.json().get('country', [])
    if not nationalities:
        return "Error: No nationality data available."
    return nationalities


def get_country_codes(nationalities):
    """
    Format Nationalize API results to contain full country names.

    input:
        nationalities: list of dictionary containing results from Nationalize API 
    output:
        list containing results converted from country code to country name (i.e. AU -> Australia)
    """

    nationalities_info = []
    for country in nationalities:
        country_code = country.get('country_id')
        probability = country.get('probability')
        if country_code and probability is not None:
            cur_country = pycountry.countries.get(alpha_2=country_code)
            country_name = cur_country.name if cur_country else country_code
            country_info = {
                'country_name': country_name,
                'probability': probability
            }
            # Append dictionary to list
            nationalities_info.append(country_info)
    return nationalities_info


def get_formatted_nationality(last_name):
    """
    Predict nationality using the nationalize() function and 
    format the output to display on user interface.

    input:
        last_name: string
    output:
        list containing formatted nationality predictions or error message
    """
    nationalize_output = nationalize(last_name)

    # check if output is error
    if not isinstance(nationalize_output, list):
        return [(nationalize_output,)]

    # reformat data to be readable strings
    nationalize_predictions = get_country_codes(nationalize_output)
    nationalize_tuples = [
        (entry['country_name'], round(entry['probability'] * 100, 2))
        for entry in nationalize_predictions]

    return nationalize_tuples


def genderize(name):
    """
    Use genderize.io API to predict the gender of a given name.

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
        return f"An error occurred (Genderize API): {e}"

    data = response.json()
    gender = data.get('gender', 'unknown')
    probability = data.get('probability', 0) * 100

    return (gender, round(probability, 2))


def agify(name):
    """
    Use agify.io API to predict age of a given name.

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
        return f"HTTP error occurred: {e}"
    except requests.exceptions.Timeout:
        return "The request to the Agify API timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred (Agify API): {e}"

    data = response.json()
    age = data.get('age', 'unknown')

    return age


def spotify_track(name):
    """
    Retrieve data for first track that matches a given name on Spotify.
    Example: 'Rhiannon' -> 'Rhiannon' by Fleetwood Mac

    input:
        name: string
    output: 
        dictionary of strings (track name, artist name, Spotify URL)
    """

    # ** Add client credentials here **
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'

    token_url = "https://accounts.spotify.com/api/token"

    # Make POST request to retrieve access token to Spotify API
    try:
        response = requests.post(token_url,
                                 data={"grant_type": "client_credentials"},
                                 auth=HTTPBasicAuth(client_id, client_secret), timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while requesting token: {e}"

    token = response.json().get('access_token')

    if not token:
        return "Error: Unable to retrieve access token from Spotify API."

    # Make GET request for first track that matches name
    search_url = "https://api.spotify.com/v1/search"
    search_headers = {
        "Authorization": f"Bearer {token}"
    }
    search_params = {
        "q": name,
        "type": "track",
        "limit": 1
    }

    try:
        search_response = requests.get(
            search_url, headers=search_headers, params=search_params, timeout=10)
        search_response.raise_for_status()
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred during search: {e}"

    search_results = search_response.json()

    # Get track name, artist, and Spotify URL from the search results
    items = search_results['tracks']['items'][0]

    track_data = {
        "track_name": items['name'],
        "artist_name": items['artists'][0]['name'],
        "spotify_url": items['external_urls']['spotify']
    }

    return track_data


def split_full_name(name):
    """ 
    Split full name into first and last names if 2 names are entered;
    otherwise, both names will be set to the first name

    input:
        name: string
    output:
        tuple of strings (first and/or last names)
    """
    name_parts = name.split()
    first_name = name_parts[0].strip()

    # set last name to first if only 1 name provided
    last_name = name_parts[1].strip() if len(name_parts) > 1 else first_name

    return first_name, last_name
