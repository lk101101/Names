import os
from csv import reader, writer
import codecs
import random
import matplotlib.pyplot as plt
import argparse
import requests
from bs4 import BeautifulSoup
import pycountry

# read + return raw data from files
def data_func(filename):
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)
    file_obj = open(full_path, 'r')
    raw_data = file_obj.readlines()
    file_obj.close()
    return raw_data

# if specified name matches a name from the list, return its ranking
def ranking_of_name(name, gender, raw_data):
    for i in raw_data:
        separated = i.split(',')
        if separated[1].lower() == gender.lower() and separated[0] == name:
            return separated[2].strip('\n')
    return 0

# * Parses command line inputs, returns data for inputted name, and creates a visualization
def popularity():
    try:
        name,gender,year = input("Find out how many babies are named a certain name in a specific year. Format as 'name gender (m/f) year (>1880)': ").split()
        name = name.capitalize()
        
        current_file = 'names_files/yob2020.txt'
        past_file = 'names_files/yob%s.txt' % year
    
        if gender.lower() == 'f':
            full_gender = "girls"
        elif gender.lower() == 'm':
            full_gender = "boys"
        else:
            exit()
                    
        cur_raw_data = data_func(current_file)
        past_raw_data = data_func(past_file)
                
        # get ranks from current and specified year
        cur_rank = ranking_of_name(name, gender, cur_raw_data)
        past_rank = ranking_of_name(name, gender, past_raw_data)
        
        print("The {} name {} was used {} times in 2020 and {} times in {}".format(full_gender, name, cur_rank, past_rank, year))

        # ** visualization code **
        years = []
        ranks = []
        # gather the ranks for each year between the specified and current year
        for i in range(int(year), 2021):
            years.append(str(i))
            new_file = 'names_files/yob%s.txt' % str(i)
            new_raw_data = data_func(new_file)
            new_rank = ranking_of_name(name, gender, new_raw_data)

        # if name isn't in file, use 0 as rank
            if (new_rank == None):
                ranks.append(0)
            else:
                ranks.append(int(new_rank))

        viz(years, ranks, name, year)

    except:
        print("\nERROR: Too few inputs or invalid inputs.\nFormat your query as |name gender year|.\nGender must be either m or f. Year must be between 1880 and 2020.\n")


# * Creates line graph to display change in ranking of name over time
def viz(year_list, rank_list, name, year):
    # *change color of line here*
    plt.plot(year_list, rank_list, color = 'deepskyblue', marker = 'o')
    plt.ylabel('Popularity')
    plt.xlabel('Years')
    plt.title('Popularity of Name {} from {} to 2020'.format(name.capitalize(), year))

    # add ranking labels to points on graph
    for x, y in zip(year_list, rank_list):
        plt.annotate(y, (x,y))
    plt.grid(True)
    plt.show()


# ** Option r: random name generator **
"""
Examples of valid inputs:
(blank) -> a random first name of any gender
m / f   -> a random name of specified gender
2       -> 2 random first names of any gender
f s     -> a random first and last name
2 s     -> 2 random last names
f 2     -> 2 random first names of specified gender (female)
f 2 s   -> 2 random first names of specified gender (female) and two random last names
"""
# Parses command line inputs for random name generator and calls specific functions
def random_name_generator():
    rand_input = input("Specify a gender (m/f) and/or number of names to generate (>1) and/or whether to include a random surname (s). Leave blank for a single random name: ")
    parts = rand_input.split(' ')
    length = len(parts)
        
    if parts == ['']:
        random_name(True, False, False, False)
    elif length == 1:
        handle_single_input(parts[0])
    elif length == 2:
        handle_two_inputs(parts[0], parts[1])
    elif length == 3:
        handle_three_inputs(parts[0], parts[1], parts[2])
    else:
        print("\nERROR: You may have provided too many inputs (>3) or one of your inputs is invalid.\nRemember to specify a gender (m/f), use digits to print a certain number of names, or use the letter s to generate a random surname.\n")
        
        
def handle_single_input(input):
    if input == 's':
        sur = random_surname()
        print(sur)
    elif input.isnumeric():
        number = int(input)
        for num in range(0, number):
            random_name(True, False, False, False)
    elif input == 'f' or input == 'm':
        random_name(True, True, input, False)
    else:
        print("\nERROR: You provided a single invalid input.\nRemember to specify a gender (m/f), use digits to specify the number of names, or use the letter s to generate a random surname.\n")
        
def handle_two_inputs(input1, input2):
    if input1.isnumeric() and input2 == 's':
        number = int(input1)
        for num in range(number):
            sur = random_surname()
            print(sur)
    elif input1 == 'f' or input1 == 'm':
        gender = input1
        if input2.isnumeric():
            number = int(input2)
            for num in range(0, number):
                random_name(True, True, gender, False)
        elif input2 == 's':
            random_name(True, True, gender, True)
        else:
            print("\nERROR: You specified gender (m/f) but your second input is invalid.\nInput a digit x (>1) to generate x number of names or s to generate a random surname.\n")
    else:
        print("\nERROR: You provided at least one invalid input.\nRemember to specify a gender (m/f), use digits to specify the number of names, or use the letter s to generate a random surname.\n")

def handle_three_inputs(input1, input2, input3):
    if input3 == 's':
        gender = input1
        number = int(input2)
        for num in range(0, number):
            random_name(True, True, gender, True)
    else:
        print("\nERROR: You may have provided too many inputs (>3) or one of your inputs is invalid.\nRemember to specify a gender (m/f), use digits to print a certain number of names, or use the letter s to generate a random surname.\n")


# * Gets a random surname from the surname CSV file
def random_surname():
    with open("2010CensusSurnames.csv") as f:
        csv_reader = reader(f)
        # skip first two rows in file
        next(csv_reader)
        next(csv_reader)
        surnames = list(csv_reader)
        random_line = random.choice(surnames)
        sur = random_line[0].lower()
        return sur.capitalize()

# * Gets random name (+ surname if specified), specified gender
def random_name(first_name, specified_gender, gender, surname):
    # get random year + file
    year = random.randrange(1880, 2020)
    year = str(year)
    file_name = 'names_files/yob%s.txt' % year
    
    found = False
    
    first_name_list = random.choice(open(file_name).readlines())
    
    if (first_name):
        while not found:
            # split line into separate words
            line = first_name_list.split(',')
            
            if (specified_gender):
                if line[1].lower() == gender.lower():
                    found = True
                    # note: print line[2] for number of babies named this name
                    result = year + ": " + line[1] + " " + line[0]

                    if (surname):
                        sur = random_surname()
                        result += " " + sur
                    print(result)
                # if gender doesn't match, generate new random name
                else:
                    first_name_list = random.choice(open(file_name).readlines())
            
            # no gender provided
            else:
                found = True
                result = year + ": " + line[1] + " " + line[0]
                
                if (surname):
                    sur = random_surname()
                    result += " " + sur
                print(result)

# * Scrapes Name Berry for name's origin and meaning
def get_name_meaning(name, gender):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    r = requests.get("https://nameberry.com/babyname/" + name + "/" + gender, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    print("** {} **".format(name.capitalize()))

    meaning = soup.find_all('div', {"class":"t-copy"})

    if not meaning:
       print("There is no information about {} on NameBerry.com.".format(name.capitalize()))

    else:
        for sentence in meaning:
            print(sentence.text)

# Calls nationalize.io API to return predicted nationality of a name
def nationalize(name):
    response = requests.get(f"https://api.nationalize.io?name={name}")
    if response.status_code == 200:
        print('\n** Predicted nationality **')
        data = response.json()
        for country in data['country']:
            countryID = country['country_id']
            try:
                full_country_name = pycountry.countries.get(alpha_2=countryID)
                countryID = full_country_name.name
            except:
                print('Error: Invalid country code')
            print('Country: {} | Probability: {}%'.format(countryID, round(country['probability'] * 100)))
    else:
        print("\nError: Failed to retrieve data from the Nationalize API")

# Calls genderize.io API to return predicted gender of a name
def genderize(name):
    response = requests.get(f"https://api.genderize.io?name={name}")
    if response.status_code == 200:
        print('\n** Predicted gender **')
        data = response.json()
        print('Gender: {} | Probability: {}%'.format(data['gender'], round(data['probability'] * 100)))
    else:
        print("\nError: Failed to retrieve data from the Genderize API")

# Calls agify.io API to return predicted age of a name
def agify(name):
    response = requests.get(f"https://api.agify.io?name={name}")
    if response.status_code == 200:
        print('\n** Predicted age **')
        data = response.json()
        print("Age: {}".format(data['age']))
        print('\n')
    else:
        print("\nError: Failed to retrieve data from the Agify API")

# * Outputs a name's meaning and predicted gender, age, and nationality
def name_information():
    try:
        name, gender = input("Enter a name and gender (f or m) to return its origin, meaning, and predicted gender, age, and nationality: ").split()
        if (gender.lower() == 'm'):
            gender = "boy"
        else:
            gender = "girl"

        get_name_meaning(name, gender)
        nationalize(name)
        genderize(name)
        agify(name)
    except:
        print("Error: Remember to input both a name and a gender.")

# * Saves favorite names in csv file or prints list of favorite names
def fav_names_file():
    file = "Fav_Names.csv"
    i = input("Enter a name in format 'name gender' to save it or enter 'print' to return your favorite names so far: ")
    if i.lower() == 'print':
        # check if csv file is empty
        if os.stat(file).st_size == 0:
            print("\nERROR: Favorite name file is empty. Add names to print from file.\n")
        else:
            # use encoding part to remove BOM from start of first row element
            with open(file, "r", encoding='utf-8-sig') as f:
                csv_reader = reader(f)
                for row in csv_reader:
                    # avoid printing empty rows
                    if row:
                        print(row[0] + ", " + row[1])

    else:
        i = i.split()
        if len(i) != 2:
             print("\nERROR: Enter both a name and a gender (either m or f) to save it to your list of favorite names. \n")
             exit()
        name = i[0].capitalize().strip()
        gender = i[1].lower().strip()
        
        print(name + " " + gender)

        with open(file, "a") as f:
            # if not at beginning of a line -> avoid overwriting existing rows
            if f.tell() > 0:
                f.write("\n")
            csv_writer = writer(f)
            csv_writer.writerow([name, gender])

        print("Saved!")


options = {
    'p': popularity,
    'r': random_name_generator,
    'm': name_information,
    's': fav_names_file
}

def main():
    done = False;
    while (not done):
        answer = input("Select an option: r to return a random name, p to return the popularity ranking of a name, m to return details about a name, s to save a favorite name, or f to exit: ")
        if answer in options:
            options[answer]()
        elif answer == 'f':
            done = True
        else:
            print("Invalid choice.\nChoose r for a random name, p for a name's popularity, m for a name's meaning, or s to save your favorite names.")

if __name__ == '__main__':
    main()
