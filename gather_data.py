"""
Gathers and saves locally 
- annual name datasets, 
- top 100 surnames file, and 
- number of Social Security card holders each year.
"""

import zipfile
import os
from csv import writer
import requests
from bs4 import BeautifulSoup
import pandas as pd


def download_zip_files():
    """
    Download and unzip name files from SSA. 
    """
    url = "https://www.ssa.gov/oact/babynames/names.zip"
    zip_file_path = 'names.zip'
    extract_file_path = 'names_files'

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request: {e}"

    os.makedirs(extract_file_path, exist_ok=True)

    with open(zip_file_path, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_file_path)

    os.remove(zip_file_path)


def download_surnames():
    """
    Download top 1000 surnames from US Census.
    """

    url = "https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top1000.xlsx"

    file_path = "surnames.xlsx"
    output_dir = 'names_files'
    output_file = 'surnames.csv'
    output_path = os.path.join(output_dir, output_file)

    os.makedirs(output_dir, exist_ok=True)

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.exceptions.Timeout:
        return "The request timed out."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the request: {e}"

    with open(file_path, 'wb') as f:
        f.write(r.content)

    df = pd.read_excel(file_path)
    df.to_csv(output_path, index=False)
    os.remove(file_path)


def scrape_ssa():
    """
    Scraps SSA website for data about 
    'Number of Social Security card holders 
    born in the U. S. by year of birth and sex.'
    """

    url = 'https://www.ssa.gov/oact/babynames/numberUSbirths.html'

    output_file = "names_files/ssa_counts.csv"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table")

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(['Year of Birth', 'Male', 'Female', 'Total'])

        for row in table.find_all('tr'):
            columns = row.find_all(['td'])
            if columns:
                year = columns[0].text.strip(',')
                male = columns[1].text.replace(',', '').strip()
                female = columns[2].text.replace(',', '').strip()
                total = columns[3].text.replace(',', '').strip()
                csv_writer.writerow([year, male, female, total])


def main():
    """
    Main function.
    """

    download_zip_files()
    download_surnames()
    # ** Uncomment to download number of Social Security card holders by year and gender
    # scrape_ssa()


if __name__ == "__main__":
    main()
