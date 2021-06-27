import os
import csv

class NameReader():
    def __init__(self, filename, name):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.full_path = os.path.join(self.base_path, filename)
        self.file_obj = open(self.full_path, 'r')
        self.raw_data = self.file_obj.readlines()
        self.file_obj.close()

        self.name = name

    # iterate through list
    # if specified name matches a name from the list, return its ranking
    def ranking_of_name(self):
        for i in self.raw_data[1:]:
            separated = i.split(',')
            if separated[0].lower() == self.name.lower():
                return separated[2].strip('\n')

def main():
    name, year = input("Find out how many babies are named a certain name in a specific year. Format as 'name year': ").split()

    current_file = 'yob2020.txt'
    past_file = 'yob' + year + '.txt'
    
    # create instances of NameReader class

    current_name = NameReader(current_file, name)
    past_name = NameReader(past_file, name)
    # get ranks from current and specified year
    cur_rank = current_name.ranking_of_name()
    past_rank = past_name.ranking_of_name()

    print("The name {} was used {} times in 2020 and {} times in {}".format(name.upper(), cur_rank, past_rank, year))
    
if __name__ == '__main__':
    main()