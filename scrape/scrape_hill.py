#!/usr/bin/env python3

#===============================================================================
# Scrape thehill.com COVID-19 articles
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
# Usage: from terminal run `pipenv run python3 scrape_hill.py`
#===============================================================================

# imports
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sys

num_pages_to_scrape = 20

for i in range(num_pages_to_scrape):
    print("Page: " + str(i))
    try:
        # url definition
        url = "https://thehill.com/homenews/coronavirus-report?page=" + str(i)

        # Request
        r1 = requests.get(url)
        r1.status_code

        # We'll save in coverpage the cover page content
        coverpage = r1.content

        # Soup creation
        soup1 = BeautifulSoup(coverpage, 'html5lib')

        # News identification
        coverpage_news = soup1.find_all('h2', class_='node-title')

        number_of_articles = len(coverpage_news)
        print("Number of articles: " + str(number_of_articles))
        if number_of_articles == 0: break

        # Empty lists for content, links and titles
        news_contents = []
        list_links = []
        list_titles = []

        for n in range(0, number_of_articles):
            try:
                # We need to ignore "live" pages since they are not articles
                if "live" in coverpage_news[n].find('a')['href']:
                    continue

                # Getting the link of the article
                link = coverpage_news[n].find('a')['href']
                link = f"https://thehill.com{link}"
                list_links.append(link)
                print(link)

                # Getting the title
                title = coverpage_news[n].get_text()
                list_titles.append(title)

                # Reading the content (it is divided in paragraphs)
                article = requests.get(link)
                article_content = article.content
                soup_article = BeautifulSoup(article_content, 'html5lib')
                body = soup_article.find_all(class_='content-wrp')
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

        f = open("../central/hill.txt", "a")
        f2 = open("../central/central_articles.txt", "a")
        for content in news_contents:
            f.write(content)
            f2.write(content)
        f.close()
        f2.close()
    except Exception as e:
        print(e)
        continue

# for i in range(0, number_of_pages):
#     # url definition
#     url = "https://thehill.com/homenews/coronavirus-report?page={}".format(i)

#     # Request
#     r1 = requests.get(url)
#     r1.status_code

#     # We'll save in coverpage the cover page content
#     coverpage = r1.content

#     # Soup creation
#     soup1 = BeautifulSoup(coverpage, 'html5lib')

#     # News identification
#     coverpage_news = soup1.find_all('h2', class_='node-title')

#     for n in range(0, len(coverpage_news)):
            
#         # We need to ignore "live" pages since they are not articles
#         if "live" in coverpage_news[n].find('a')['href']:  
#             continue
        
#         # Getting the link of the article
#         link = coverpage_news[n].find('a')['href']
#         link = f"https://thehill.com{link}"
#         list_links.append(link)
        
#         # Getting the title
#         title = coverpage_news[n].get_text()
#         list_titles.append(title)

#         # Reading the content (it is divided in paragraphs)
#         article = requests.get(link)
#         article_content = article.content
#         soup_article = BeautifulSoup(article_content, 'html5lib')
#         body = soup_article.find_all('div', id="content")
#         x = body[0].find_all('p') if body else []
        
#         # Unifying the paragraphs
#         list_paragraphs = []
#         for p in range(0, len(x)):
#             paragraph = x[p].get_text()
#             list_paragraphs.append(paragraph)
#             final_article = " ".join(list_paragraphs)
        
#         if body:
#             news_contents.append(final_article)

# for content in news_contents:
#   print(content, end="\n\n")
