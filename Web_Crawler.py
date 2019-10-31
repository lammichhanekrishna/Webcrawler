#Krishna lamichhane
import urllib
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from urllib.request import Request
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import collections
from collections import Counter
import pickle

 #Manual top ten elements
top_ten = ['dictionary' , 'bitcoin' , 'intelligence',
                'news' , 'language' , 'artificial' , 'programming','class','terms' , 'security']
    
sentence_tokens = []
top_3_list =[]
kb = {}

def main():
    getlink("https://www.google.com/search?q=artificial")     
    
    # print("Top 45: \n " , top_3_list)
    # print(top_ten)
    # print(sentence_tokens)



    sentences = []
    print(len(sentence_tokens))

    for word in top_ten:
        for y in sentence_tokens:
            if word in y:
                sentences.append(y)
        if 35 < len(sentences) < 600:            
            kb[word] = list(set(sentences))
        sentences.clear()


    with open('knowledgebase.pickle' ,'wb') as kn:
        pickle.dump(kb , kn)

   


def URLextraction(soup):
    # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if 'artificial' in link_str or 'Artificial' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    #print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str:
                    f.write(link_str + '\n')

        # end of program
        print("links writing")

    #Reading each lines from the urls.txt file
    line_read = open("urls.txt" ,"r")
    line_open = line_read.read().splitlines()
    scrape(line_open) #This calls the scrape function


#This function writes text to files
def scrape(line_open):
    counter =1
    for lines in line_open:
        req = Request(lines,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})    
       
        try:
             html = urllib.request.urlopen(req)
        except:
            pass
        soup = BeautifulSoup(html, "html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)      # list from filter
        temp_str = ' '.join(temp_list)
        address_to_save = "Link"+str(counter)+ ".txt"
        with open(address_to_save , "w+") as f: #Writing data to the files
            print("writing to file", str(counter) , "Success!")
            f.write(temp_str)
        if counter == 15:
            break
        counter += 1


    #Cleaning the text file
    for numbers in range(1,16):
        link_n = "Link"+str(numbers)+".txt"
      
        preprocess(link_n,numbers) ##Returns the cleaned sentences

def preprocess(link_n,numbers):   
    link_op = open(link_n)
    link_read = link_op.read()

    #Remove the punctuation words
    after_punc = re.sub(r'[?!,:@#$%^•&*~▲▼≡©_+`;()\–\n\^\/-\[\]]',' ',link_read.lower())
    after_punc = after_punc.replace('--','')
    after_punc = after_punc.replace('%','')
    after_punc = after_punc.replace('-','')
    after_punc = after_punc.replace('\'\"','')
    after_punc = after_punc.strip()
    after_punc = re.sub(r"\d", "", after_punc)
    tokens = re.sub(' +', ' ', after_punc)

    # Remove stopwords
    # stop_words = set(stopwords.words('english'))
    # tokens = [t for t in after_punc if not t in stop_words]

    #sentence tokenize
    #tokenized_word = word_tokenize(tokens)
    tokens_1 = sent_tokenize(tokens)

   
    with open("Link"+str(numbers)+"clean.txt" , "w+") as wr: #Writing clean data to files
        print("writing cleaned data"+ str(numbers))
        for w in tokens_1:
            wr.write(w +'\n')
            sentence_tokens.append(w)
     
    #passing to a df function
    most_common(tokens,tokens_1)
    

def most_common(after_punc , tokens_1):
    #Further cleaning the text
    stop = set(stopwords.words('english'))
    tokens = word_tokenize(after_punc)
    frequent_words = ['artificial','div',"color yellow",'\t']
    tokens = [t for t in tokens if t not in stop  if t not in frequent_words]
    
    tokens_clean = []
    for w in tokens:
        if len(w) > 3: 
            tokens_clean.append(w)
    
    words = {t:tokens_clean.count(t) for t in set(tokens_clean)}
    word_counts = Counter(words)
   
    top_3 =  word_counts.most_common(3)
   
    top_3_list.extend(top_3)






   
   


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
def getlink(starter_link):
    r = requests.get(starter_link)
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    #Extracting URL
    URLextraction(soup)  
main()