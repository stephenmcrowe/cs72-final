# header

# imports
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sys

url = "https://abcnews.go.com/Health/Coronavirus"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all(class_='ContentList__Item')

number_of_articles = len(coverpage_news)

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

num_scraped_articles = 0
for n in range(0, number_of_articles):
    try:
        # We need to ignore "live" pages since they are not articles
        if "live" in coverpage_news[n].find('a')['href']:  
            continue
        
        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)
        
        # Getting the title
        title = coverpage_news[n].get_text()
        list_titles.append(title)
        
        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('article', class_='Article__Content')
        if (len(body) > 0):
            x = body[0].find_all('p')
            
            # Unifying the paragraphs
            list_paragraphs = []
            for p in range(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
                
            news_contents.append(final_article)
            num_scraped_articles += 1
    except Exception as e:
        print(e)
        continue


f = open("../liberal/abc_" + str(num_scraped_articles) + ".txt", "w")
f2 = open("../liberal/liberal_articles.txt", "a")
for content in news_contents:
  f.write(content)
  f2.write(content)
f.close()
f2.close()