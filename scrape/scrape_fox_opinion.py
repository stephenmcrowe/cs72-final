#!/usr/bin/env python3

#===============================================================================
# Scrape recent fox news opinion articles
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
# Usage: from terminal run `pipenv run python3 scrape_fox_opinion.py`
# Without the debugger: `pipenv run python3 -O scrape_fox_opinion.py`
#===============================================================================

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

if __debug__:
    print("Debug active!\n")
else:
    print("Debug inactive!\n")

url = "https://www.foxnews.com/opinion/"


# Selenium needs to access Chrome browser driver. The options open the browser
# in incognito mode and doesn't actually open a window.
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# May need to replace chromedriver with path to chromedriver executable
# Download chromedriver executable here: https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome("/Users/stephencrowe/Downloads/chromedriver 2", chrome_options=options)

# Get the webpage
driver.get(url)
if __debug__:
    print(driver.title)
# Click the load more button up to number_of_pages_to_load times
number_of_pages_to_load = 45
for i in range(number_of_pages_to_load):
  try:
    load_more_button = driver.find_elements_by_class_name("load-more")[0]
    time.sleep(1)
    load_more_button.click()
    time.sleep(1)
    if __debug__:
        print(f"Page: {i}")
  except Exception as e:
    print(e)
    break
if __debug__:
    print("Complete")
page_source = driver.page_source
driver.quit()

soup1 = BeautifulSoup(page_source, 'html5lib')

# News identification
coverpage_news = soup1.find_all("article", class_='article')

# Empty lists for content, links and titles
news_contents = []
list_links = []
set_links = set()
list_titles = []

for n in range(0, len(coverpage_news)):

    # We need to ignore "video" pages since they are not articles
    if "video" in coverpage_news[n].find('a')['href']:
        continue

    # Getting the link of the article
    old_link = coverpage_news[n].find('a')['href']
    link = "https://www.foxnews.com{}".format(old_link)

    # Skipping if already seen
    if 'https' in old_link or link in set_links:
        if __debug__:
            print("skipping...\t{}".format(link))
        continue

    list_links.append(link)
    set_links.add(link)

    # Getting the title
    title = coverpage_news[n].get_text()
    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    if __debug__:
        print(link)
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

# Write contents of news articles to file
to_write = "../conservative/fox_opinion_{}.txt".format(len(news_contents))
if __debug__:
    print(f"writing to file {to_write} now")

f = open(to_write, "w")
for content in news_contents:
    f.write(content)
    f.write("\n\n")
f.close()