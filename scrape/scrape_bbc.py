#!/usr/bin/env python3

#===============================================================================
# Scrape bbc.com coronoavirus us and canada news articles
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

url = "https://www.bbc.com/news/world/us_and_canada"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all(class_='gs-c-promo-heading')
stream_post_news = soup1.find_all(class_='lx-stream-post')

number_of_coverpage_news_articles = len(coverpage_news)
number_of_stream_post_news_articles = len(stream_post_news)
number_of_articles = number_of_coverpage_news_articles + number_of_stream_post_news_articles

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in range(0, number_of_coverpage_news_articles):

    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n]['href']:
        continue

    # Getting the link of the article
    link = coverpage_news[n]['href']
    if (link.find("https://") == -1):
        link = "https://bbc.com{}".format(link)
    print(link)
    list_links.append(link)

    # Getting the title
    title = coverpage_news[n].get_text()
    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='story-body')
    if len(body) == 0: continue
    x = body[0].find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in range(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    news_contents.append(final_article)

for n in range(0, number_of_stream_post_news_articles):

    # We need to ignore "live" pages since they are not articles
    if "live" in stream_post_news[n].find('a')['href']:
        continue

    # Getting the link of the article
    link = stream_post_news[n].find('a')['href']
    if (link.find("https://") == -1):
        link = "https://bbc.com{}".format(link)
    print(link)
    list_links.append(link)

    # Getting the title
    title = stream_post_news[n].get_text()
    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='story-body')
    if len(body) == 0: continue
    x = body[0].find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in range(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    news_contents.append(final_article)

f = open("../central/bbc_" + str(number_of_articles) + ".txt", "w")
f2 = open("../central/central_articles.txt", "a")
for content in news_contents:
    f.write(content)
    f2.write(content)
f.close()
f2.close()