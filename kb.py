

import pickle
from random import randrange


def main():

    knowledge_base = rd("knowledgebase.pickle")
    print(knowledge_base)
    flag = 'good'

    while flag is not '1':
        print("Available Keywords: ")
        print('{:13}'.format('dictionary') + '{:13}'.format('bitcoin'))
        print('{:13}'.format('intelligence') + '{:13}'.format('news'))
        print('{:13}'.format('language') + '{:13}'.format('artificial'))
        print('{:13}'.format('programming') + '{:13}'.format('class'))
        print('{:13}'.format('terms') + '{:13}'.format('security'))
        keyword = input("Enter your Search keyword or Enter 1 to exit: ")

        if keyword is '1': 
            break

        if keyword in knowledge_base:
            index = randrange(len(knowledge_base.get(keyword)))
            print('\n'+ list(knowledge_base.get(keyword))[index] + '\n')


def rd(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return new_dict


main() 