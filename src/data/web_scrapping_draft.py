''' draft that will become make_data'''

from bs4 import BeautifulSoup
from numpy import array
import requests
import re

# Helper functions
def get_contents_names(node):
    for elmt in node.contents:
        print(elmt.name)

def get_siblings_names(node):
    for elmt in node.siblings:
        print(elmt.name)

def get_siblings(node, tag):
    return node.find_all(tag, recursive=False)

def get_page(page_number, url):
    '''return a BeautifulSoup object representing the 
       page number page_number.
    '''
    #website = BeautifulSoup(html, 'html.parser')
    rslt = requests.get(url+'page/'+str(page_number)+'/')
    page = BeautifulSoup(rslt.content, 'html.parser')
    return page

def nb_of_pages(url):
    page_one = get_page(1, url)
    nb_of_pages = page_one.find('div', class_='wp-pagenavi').text[12:15]
    return int(nb_of_pages)

def scrape_page(page):
    '''return a list of punchlines scraped on a specific page.
       (use the code below)
    '''
    def retrieve_punchline_from_string(string):
        # locate "«" and "»"
        begining = string.find('«')
        end = string.find('»')
        # return all caracters located between "«" and "»"
        return string[begining+1:end]


    pat = re.compile('post-')
    # Selecting the tag where the punchlines are located
    narrowed = get_siblings(page.body, 'div')[1]

    # Selecting the different posts
    posts = narrowed.find_all(name='div', id=pat)

    # retrieving the strings that contains the individual punchlines
    page_corpus=[]
    nb_of_posts = len(posts)
    for i in range(nb_of_posts):
        post = posts[i]
        string_to_be_cleaned = post.find('div', class_='post-header').contents[1].get('title')
        if type(string_to_be_cleaned) == type(None):
            string_to_be_cleaned = post.find('div', class_='post-header').contents[2].string
        punchline = retrieve_punchline_from_string(string_to_be_cleaned)
        page_corpus.append(punchline)
    
    return page_corpus

# Getting the html page
url = 'https://www.punchline.fr/'

# Building the corpus
nb_pages = nb_of_pages(url)
corpus = []
for i in range(1, nb_pages+1):
    page = get_page(i,url)
    punchlines_in_this_page = scrape_page(page)
    corpus.extend(punchlines_in_this_page)
