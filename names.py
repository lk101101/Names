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
    Select and return a random surname from the surnames file.

    output:
        string (surname)
    """
    with open("names_files/surnames.csv", encoding='utf-8-sig') as f:
        csv_reader = reader(f)
        # skip first 3 rows in file
        for _ in range(3):
            next(csv_reader)

        total_surnames = list(csv_reader)

        # remove last 3 rows of file
        random_line = random.choice(total_surnames[:-3])
        surname = random_line[0].lower()
        return surname.capitalize()


def random_name(gender="", surname=False):
    """
    Generate and print a random name
    with options to specify gender and add surname(s).

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
    Scrape NameBerry for the origin and meaning
    of the given name and prints the result.

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
        # return f"HTTP Error: {e}"
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
    Use nationalize.io API to predict nationality of a given name.

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

    nationalities_info = []
    for country in nationalities:
        country_code = country.get('country_id')
        probability = country.get('probability')
        if country_code and probability is not None:
            cur_country = pycountry.countries.get(alpha_2=country_code)
            country_name = cur_country.name if cur_country else country_code
            country_info = {
                'country_name': country_name,
                'probability': round(probability * 100, 2)
            }
            # Append the dictionary to the list
            nationalities_info.append(country_info)
    return nationalities_info


def genderize(name):
    """
    Use genderize.io API to predict and print the gender of a given name.

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
    gender_info = (
        f"Predicted gender: {data.get('gender', 'unknown')} - "
        f"probability: {round(data.get('probability', 0) * 100, 2)}%"
    )
    return gender_info


def agify(name):
    """
    Use agify.io API to predict age associated with a given name.

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
        return (
            "HTTP error occurred: "
            f"{e.response.status_code} {e.response.reason}"
        )
    except requests.exceptions.Timeout:
        return "The request to the Agify API timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred (Agify API): {e}"

    data = response.json()
    age = data.get('age', 'unknown')
    return (f"Predicted age: {age}" if age != "unknown"
            else f"Error: No age prediction for name {name}.")


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

# TODO: handle error output from nationalize()


def name_information(name, gender):
    """
    Output a specified name's meaning and
    predicted gender, age, and nationality.

    input:
        name: string
        gender: string (either 'boy' or 'girl')
    output:
        array containing outputs from name meaning and predicted nationalities,
        age, and gender functions
    """

    # format nationalize() output
    nationalize_predictions = nationalize(name)
    nationalize_formatted = []

    if nationalize_predictions == "Error: No nationality data available.":
        nationalize_formatted = nationalize_predictions
    else:
        for entry in nationalize_predictions:
            formatted_string = (
                f"{entry['country_name']} - predicted likelihood: "
                f"{entry['probability'] * 100:.2f}%"
            )
            nationalize_formatted.append(formatted_string)

    return [
        get_name_meaning(name, gender),
        *nationalize_formatted,
        genderize(name),
        agify(name)
    ]
