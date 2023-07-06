import os
import csv
from csv import reader
import codecs
import random
import matplotlib.pyplot as plt
import argparse
import requests
from bs4 import BeautifulSoup

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
        reader = csv.reader(f)
        # skip first two rows in file
        next(reader)
        next(reader)
        surnames = list(reader)
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
                

# * Gets meaning and origin of a name using information from NameBerry.com
def name_meaning():
    name, gender = input("Enter a name and gender to return its origin and meaning: ").split()
    if (gender.lower() == 'm'):
        gender = "boy"
    else:
        gender = "girl"

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
                    print(row[0] + ", " + row[1])

    else:
        i = i.split()
        if len(i) != 2:
             print("\nERROR: Enter both a name and a gender (either m or f) to save it to your list of favorite names. \n")
             exit()
        name = i[0].capitalize().strip()
        gender = i[1].lower().strip()

        with open(file, "a", newline="\n") as f:
            writer = csv.writer(f)
            writer.writerow([name, gender, "\n"])

        print("Saved!")


options = {
    'p': popularity,
    'r': random_name_generator,
    'm': name_meaning,
    's': fav_names_file
}

def main():
    answer = input("Select an option: r to return a random name, p to return the popularity ranking of a name, m to return details about a name, or s to save a favorite name: ")
    if answer in options:
        options[answer]()
    else:
        print("Invalid choice.\nChoose r for a random name, p for a name's popularity, m for a name's meaning, or s to save your favorite names.")
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
