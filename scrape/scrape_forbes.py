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
# This script uses the Selenium package. See the documentation here:
# https://selenium-python.readthedocs.io/
#
# Usage: from terminal run `pipenv run python3 scrape_forbes.py`
#===============================================================================

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import time
import sys
from selenium import webdriver

url = "https://www.forbes.com/coronavirus"

# Selenium needs to access Chrome browser driver. The options open the browser
# in incognito mode and doesn't actually open a window.
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless') # for some reason forbes/coronavirus does not load when using headless browser
# May need to replace chromedriver with path to chromedriver executable
# Download chromedriver executable here: https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome("chromedriver", chrome_options=options)

# Get the webpage
driver.get(url)
print(driver.title)
# Click the load more button up to number_of_pages_to_load times
number_of_pages_to_load = 20
for i in range(number_of_pages_to_load):
  try:
    load_more_button = driver.find_elements_by_class_name("load-more")[0]
    time.sleep(1)
    load_more_button.click()
    time.sleep(1)
    print('Page: ' + str(i))
  except Exception as e:
    print(e)
    break
print("Complete")
page_source = driver.page_source
driver.quit()

soup1 = BeautifulSoup(page_source, 'html5lib')

# News identification
coverpage_news = soup1.find_all(class_='stream-item__title')
number_of_articles = len(coverpage_news)
print("Number of news articles: " + str(number_of_articles))

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in range(0, number_of_articles):
    try:
        # We need to ignore "live" pages since they are not articles
        if "live" in coverpage_news[n]['href']:
            continue

        # Getting the link of the article
        link = coverpage_news[n]['href']
        print(link)

        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].get_text()

        list_titles.append(title)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all(class_="article-body")
        x = body[0].find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in range(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)
    except Exception as e:
        print(e)
        continue

f = open("../central/forbes_" + str(number_of_articles) + ".txt", "w")
f2 = open("../central/central_articles.txt", "a")
for content in news_contents:
    f.write(content)
    f2.write(content)
f.close()
f2.close()