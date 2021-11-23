import os
import csv
from csv import reader
import codecs
import random
import matplotlib.pyplot as plt
import argparse
from bs4 import BeautifulSoup
import requests

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

        current_file = 'yob2020.txt'
        past_file = 'yob%s.txt' % year

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
            new_file = 'yob%s.txt' % str(i)
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
# TO DO: implement better command line handling

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
    surname = False
    first_name = False
    specified_gender = False
    gender = 'x'
    
    # ** nothing specified
    if not rand_input:
        first_name = True
        random_name(first_name, specified_gender, gender, surname)
    else:
        rand_input = rand_input.split(' ')
        length = len(rand_input)

        # ** all 3 inputs provided - gender, number and surname
        if length == 3 and rand_input[2] == 's':
            gender = rand_input[0]
            number = int(rand_input[1])
            surname = True
            specified_gender = True
            first_name = True
            for num in range(0, number):
                random_name(first_name, specified_gender, gender, surname)

        # ** 2 inputs provided
        # determine if number + surname, gender + surname, or gender + number
        elif length == 2:
            first = rand_input[0]
            second = rand_input[1]

            # number and surname
            if (first.isnumeric() and second == 's'):
                number = int(first)
                surname = True
                for num in range(0, number):
                    sur = random_surname()
                    print(sur)

            # gender specified
            elif (first == 'f' or first == 'm'):
                gender = first
                first_name = True
                specified_gender = True
                # gender and number
                if (second.isnumeric()):
                    number = int(second)
                    for num in range(0, number):
                        # random_specific_gender(gender, surname)
                        random_name(first_name, specified_gender, gender, surname)
                # gender and surname
                elif (second == 's'):
                    surname = True
                    specified_gender = True
                    random_name(first_name, specified_gender, gender, surname)
                # ERROR: gender is specified, but invalid second input
                else:
                    print("\nERROR: You specified gender (m/f) but your second input is invalid.\nInput a digit x (>1) to generate x number of names or s to generate a random surname.\n")
            # ERROR
            else:
                print("\nERROR: You provided at least one invalid input.\nRemember to specify a gender (m/f), use digits to print a certain number of names, or use the letter s to generate a random surname.\n")

        # ** one input
        elif length == 1:
            first = rand_input[0]
            # gender
            if (first == 'f' or first == 'm'):
                first_name = True
                specified_gender = True
                random_name(first_name, specified_gender, first, surname)
            # number
            elif first.isnumeric():
                first_name = True
                number = int(first)
                for num in range(0, number):
                    random_name(first_name, specified_gender, gender, surname)
            # surname
            elif (first == 's'):
                surname = True
                sur = random_surname()
                print(sur)
            # ERROR
            else:
                print("\nERROR: You provided a single invalid input.\nRemember to specify a gender (m/f), use digits to print a certain number of names, or use the letter s to generate a random surname.\n")
        else:
            print("\nERROR: You may have provided too many inputs (>3) or one of your inputs is invalid.\nRemember to specify a gender (m/f), use digits to print a certain number of names, or use the letter s to generate a random surname.\n")


# * Gets a random surname from the surname CSV file
def random_surname():
    with open("2010CensusSurnames.csv") as f:
        reader = csv.reader(f)
        surnames = list(reader)
        random_line = random.choice(surnames)
        sur = random_line[0].lower()
        return sur.capitalize()


# * Gets random name (+ surname if specified), specified gender
def random_name(first_name, specified_gender, gender, surname):
    # get random year + file
    year = random.randrange(1880, 2020)
    year = str(year)
    file_name = 'yob%s.txt' % year

    found = False
    
    # make array of 10 random names and iterate until name that matches gender (if specified) is found
    first_name_list = random.choices(open(file_name).readlines(), k = 10)
    
    i = 0;

    # return first name
    if (first_name):
        while not found:
            # split line into separate words
            line = first_name_list[i].split(',');
            
            if (specified_gender):
                if line[1].lower() == gender.lower():
                    found = True
                    # note: print line[2] for number of babies named this name
                    result = year + ": " + line[1] + " " + line[0]

                    if (surname):
                        sur = random_surname()
                        result += " " + sur
                    print(result)
                # if gender doesn't match, iterate to next name in array
                else:
                    found = False
                    i += 1
            
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



def main():
    answer = input("Select an option: r to return a random name, p to return the popularity ranking of a name, m to return details about a name, or s to save a favorite name: ")
    if answer.lower() == 'p':
        popularity()
    elif answer.lower() == 'r':
        random_name_generator()
    elif answer.lower() == 'm':
        name_meaning()
    elif answer.lower() == 's':
        fav_names_file()
    else:
        print("Invalid choice.\nChoose r for a random name, p for a name's popularity, m for a name's meaning, or s to save or print favorite names.")

if __name__ == '__main__':
    main()
