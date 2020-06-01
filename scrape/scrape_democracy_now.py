#!/usr/bin/env python3

#===============================================================================
# Scrape democracynow.com COVID-19 articles
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
# Usage: from terminal run `pipenv run python3 scrape_vox.py`
#===============================================================================

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sys

url = "https://www.democracynow.org/topics/coronavirus"

# Request
r1 = requests.get(url)
r1.status_code

coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all(class_='news_item')

number_of_articles = len(coverpage_news)

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in range(0, number_of_articles):

    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n].find('a')['href']:
        continue

    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    link = "https://www.democracynow.org{}".format(link)
    list_links.append(link)

    # Getting the title
    title = coverpage_news[n].get_text()

    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all(class_="primary_content")
    x = body[0].find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in range(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    news_contents.append(final_article)

f = open("../liberal/democracy_now_" + str(number_of_articles) + ".txt", "w")
f2 = open("../liberal/liberal_articles.txt", "a")
for content in news_contents:
  f.write(content)
  f2.write(content)
f.close()
f2.close()