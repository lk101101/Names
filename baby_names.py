import os
import csv
import random
import matplotlib.pyplot as plt
import argparse
from bs4 import BeautifulSoup
import requests


class NameReader():
    def __init__(self, filename, name, gender):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, filename)
        self.file_obj = open(self.full_path, 'r')
        self.raw_data = self.file_obj.readlines()
        self.file_obj.close()

        self.name = name
        self.gender = gender

    # iterate through list
    # if specified name matches a name from the list, return its ranking
    def ranking_of_name(self):
        for i in self.raw_data:
            separated = i.split(',')
            if separated[1].lower() == self.gender.lower() and separated[0] == self.name:
                return separated[2].strip('\n')
        return 0

def popularity():
    name,gender, year = input("Find out how many babies are named a certain name in a specific year. Format as 'name gender (m/f) year': ").split()
    name = name.capitalize()

    current_file = 'yob2020.txt'
    past_file = 'yob%s.txt' % year

    full_gender = "girls'" if gender.lower() == 'f' else "boys'" 
    
    # create instances of NameReader class
    current_name = NameReader(current_file, name, gender)
    past_name = NameReader(past_file, name, gender)
    
    # get ranks from current and specified year
    cur_rank = current_name.ranking_of_name()
    past_rank = past_name.ranking_of_name()

    print("The {} name {} was used {} times in 2020 and {} times in {}".format(full_gender, name, cur_rank, past_rank, year))

    # visualization code
    years = []
    ranks = []
    # gather the ranks for each year between the specified and current year
    for i in range(int(year), 2021):
        years.append(str(i))
        new_file = 'yob%s.txt' % str(i)
        new_name = NameReader(new_file, name, gender)
        new_rank = new_name.ranking_of_name()

    # if name isn't in file, use 0 as rank
        if (new_rank == None):
            ranks.append(0)
        else:
            ranks.append(int(new_rank))

    viz(years, ranks, name, year)

# create line graph to display change in ranking of name over time
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
def random_name_generator():
    rand_input = input("Specify a gender (m/f), number of names to generate or leave blank: ")

    # if rand_input = empty, nothing specified
    if not rand_input:
        random_gen()
    else:
        rand_input = rand_input.split(' ')
         
        # both gender and number are specified
        if (len(rand_input) == 2):
            gender = rand_input[0]
            number = int(rand_input[1])
            for num in range(0, number):
                random_gen_gender(gender)
            
        # only gender is specified
        elif (rand_input[0] == 'f' or rand_input[0] == 'm'):
            gender = rand_input[0]
            random_gen_gender(gender)
            
        # only number is specified
        else:
            number = int(rand_input[0])
            for num in range(0, int(number)):
                random_gen()


def random_gen():
    # get random year + file
    year = random.randrange(1880, 2020)
    year = str(year)
    file_name = 'yob%s.txt' % year

    # get random line and split into separate words
    line = random.choice(open(file_name).readlines())
    line = line.split(',')

    # print line[2] for number of babies named this name
    print(year + ": " + line[1] + " " + line[0])

def random_gen_gender(gender):
    # get random year + file
    year = random.randrange(1880, 2020)
    year = str(year)
    file_name = 'yob%s.txt' % year

    found = False

    # loop until random name matches specified gender
    while not found:
        # get random line and split into separate words
        line = random.choice(open(file_name).readlines())
        line = line.split(',')
        if line[1].lower() == gender.lower():
            found = True
            # print line[2] for number of babies named this name
            print(year + ": " + line[1] + " " + line[0])
        else:
            found = False

def main():
    answer = input("Select an option: r to return a random name, p to return the popularity ranking of a name, or m to return details about a name: ")

    if answer.lower() == 'p':
        popularity()

    elif answer.lower() == 'r':
        random_name_generator()

    elif answer.lower() == 'm':
        # meaning / history of name
        name = input("Enter a name to return its origin and meaning: ")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        r = requests.get("https://babynames.com/name/" + name, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        print("\n")
        print("** Info about the Name {} from BabyNames.com **".format(name.capitalize()))
        # get origin and meaning
        get_origin = soup.find_all('div', {"class":"name-meaning"})
        origin = get_origin[1].text
        print(origin.strip() + '\n')

        line_breaks = soup.find_all('br')        
        for x in line_breaks:
            x.replaceWith('')

        meaning_class = soup.find('div', {"class": "stats"})
        full_meaning = meaning_class.get_text().split(". ")

        # splice list to not include lists 'people who like the name x also like', etc.
        for meaning in full_meaning[: -1]:
            meaning = meaning.strip('\n')
            if meaning:
               sentence = meaning.strip('\n')
               sentence = sentence.strip()               
               print(sentence)
               # delete the newline below to print everything in one chunk of text
               print("\n")
    
    else:
        print("Invalid choice. Choose r for a random name, p for a name's popularity, or m for a name's meaning.")
    
if __name__ == '__main__':
    main()