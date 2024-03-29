# header

# imports
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sys

url = "https://www.washingtonexaminer.com/tag/coronavirus"

# Request
r1 = requests.get(url)
r1.status_code
print(r1)
sys.exit()

# We'll save in coverpage the cover page content
coverpage = r1.content
# print(coverpage)

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all(class_='ThumbnailAuthorDatePromo-title')
print(len(coverpage_news))
sys.exit()

number_of_articles = 5

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

import sys
for n in range(0, number_of_articles):
        
    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n].find('a')['href']:  
        continue
    
    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    # print(link)
    # sys.exit()
    list_links.append(link)
    
    # Getting the title
    title = coverpage_news[n].get_text()
    list_titles.append(title)
    
    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('article', class_='Article__Content')
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