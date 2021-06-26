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
    '''return a BeautifulSoup obect representing the 
       page number page_number.
    '''
    website = BeautifulSoup(html, 'html.parser')
    rslt = requests.get(url+str(page_number)+'/')
    page = BeautifulSoup(rslt.content, 'html.parser')
    return page

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
    for post in (posts):
        string_to_be_cleaned = posts[0].find('div', class_='post-header').contents[1]
        punchline = retrieve_punchline_from_string(string_to_be_cleaned)
        page_corpus.append(punchline)

# Getting the html page
rslt = requests.get('https://www.punchline.fr/?gdsr_sort=thumbs')
html=rslt.content
page = BeautifulSoup(html, 'html.parser')

# Each punchline is associated with a post
# So we'll filter through the div with id begining by 'post-'
pat = re.compile('post-')

# Selecting the tag where the punchlines are located
narrowed = get_siblings(page.body, 'div')[1]

# Selecting the different posts
posts = narrowed.find_all(name='div', id=pat)

# retrieving the string that contains the first punchline
string_to_be_cleaned = posts[0].find('div', class_='post-header').contents[1].get('title')

'''
    Left to do:
        1) Complete retrieve_punchline_from_string
           inside scrape_page
        2) iterate through the different pages
'''

