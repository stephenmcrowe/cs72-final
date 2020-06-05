#!/usr/bin/env python3

#===============================================================================
# Scrape forbes.com COVID-19 articles
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
# Usage: from terminal run `pipenv run python3 scrape_forbes.py`
#===============================================================================

# imports
import requests
from bs4 import BeautifulSoup

# Empty lists for content, links and titles
news_contents = []
set_links = set()
list_links = []
list_titles = []

url = "https://www.bbc.com/news/coronavirus"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')
top_stories_wrapper = soup1.find("div", id="topos-component")
top_stories_a = top_stories_wrapper.find_all("a", class_="gs-c-promo-heading")

covid_US = soup1.find("div", attrs={"aria-labelledby": "nw-c-CoronavirusintheUS__title"})
covid_US_div = covid_US.find_all("div", class_="gel-layout__item")
covid_US_a = []
for div in covid_US_div:
    temp = div.find("a")
    if temp:
        covid_US_a.append(temp)

latest_updates_wrapper = soup1.find("div", class_="gel-wrap", attrs={"aria-labelledby": "latest-updates"})
latest_updates_a = latest_updates_wrapper.find_all("a", class_="qa-heading-link")
a_links = top_stories_a + covid_US_a + latest_updates_a

for story in a_links:
    # Getting the link of the article
    link = story['href']
    link = "https://www.bbc.com{}".format(link)
    if link not in set_links:
        set_links.add(link) # Must use a set here because multiple of same link
        list_links.append(link)

        # Getting the title
        title = story.get_text()
        list_titles.append(title)

for link in list_links:
    # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('div', class_="story-body__inner")
        x = body[0].find_all('p') if body else []
        
        # Unifying the paragraphs
        list_paragraphs = []
        for p in range(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
        
        if body:
            news_contents.append(final_article)

for content in news_contents:
  print(content, end="\n\n")