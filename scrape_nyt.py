# header

# imports
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
# import numpy as np
# import pandas as pd
# import time
import sys

# url definition
url = "https://www.nytimes.com/news-event/coronavirus"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all('article')

number_of_articles = 4

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in range(0, number_of_articles):
        
    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n].find('h2').find('a')['href']:  
        continue
    
    # Getting the link of the article
    link = coverpage_news[n].find('h2').find('a')['href']

    link = "https://nytimes.com{}".format(link)
    list_links.append(link)
    
    # Getting the title
    title = coverpage_news[n].get_text()

    list_titles.append(title)
    

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('section', class_='meteredContent')
    x = body[0].find_all('p')
    
    # Unifying the paragraphs
    list_paragraphs = []
    for p in range(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)

for content in news_contents:
  print(content, end="\n\n")
