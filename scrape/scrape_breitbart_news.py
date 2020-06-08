#!/usr/bin/env python3

#===============================================================================
# Scrape Breitbart News COVID-19 articles
#
# Dartmouth College, LING48 / COSC72, Spring 2020
# Anne Bailey, Stephen Crowe, Thanh Nguyen Jr
# Professor Rolando Coto-Solano
#
# This script is based off of the following tutorial:
# https://towardsdatascience.com/web-scraping-news-articles-in-python-9dd605799558
#
# This script uses the BeautifulSoup package. See the documentation here:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#
# Usage: from terminal run `pipenv run python3 scrape_breitbart_news.py`
# Without the debugger: `pipenv run python3 -O scrape_brietbart_news.py`
#===============================================================================

# imports
import requests
from bs4 import BeautifulSoup

if __debug__:
    print("Debug active!\n")
else:
    print("Debug inactive!\n")

number_of_pages = 45

# Empty lists for content, links and titles
news_contents = []
list_links = []
set_links = set()
list_titles = []

for i in range(1, number_of_pages+1):
    # url definition
    url = "https://www.breitbart.com/tag/coronavirus/page/{}".format(i)

    # Request
    r1 = requests.get(url)
    r1.status_code

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coronavirus_wrapper = soup1.find('section', class_="aList")

    # News identification
    coverpage_news = coronavirus_wrapper.find_all('h2')

    for n in range(0, len(coverpage_news)):
            
        # We need to ignore "live" pages since they are not articles
        if "live" in coverpage_news[n].find('a')['href']:  
            continue
        
        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        link = "https://www.breitbart.com{}".format(link)

        # Skipping if already seen
        if link in set_links:
            if __debug__:
                print("skipping...\t{}".format(link))
            continue

        list_links.append(link)
        set_links.add(link)
        
        # Getting the title
        title = coverpage_news[n].get_text()
        list_titles.append(title)

        if __debug__:
            print(link)
        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('div', class_="entry-content")
        if body:
            x = body[0].find_all('p')
        
            # Unifying the paragraphs
            list_paragraphs = []
            for p in range(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
        
            news_contents.append(final_article)

# Write contents of news articles to file
to_write = "../conservative/breitbart_news_{}.txt".format(len(news_contents))
if __debug__:
    print(f"writing to file {to_write} now")

f = open(to_write, "w")
for content in news_contents:
    f.write(content)
    f.write("\n\n")
f.close()