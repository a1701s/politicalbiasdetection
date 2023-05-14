from gdeltapi import GdeltDoc, Filters
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

now = datetime.today()
debugmode = True
textarray = []
gd = GdeltDoc()

if debugmode == False:
    userinputweeks = input("Weeks to search back: ")
    while not userinputweeks.isdigit():
        userinputweeks = input("Please enter an integer: ")
    userinputweeks = int(userinputweeks)
    if userinputweeks > 331:
        userinputweeks = 331
else:
    userinputweeks = 331

then = now - timedelta(weeks=userinputweeks)
formattednow = str(now.strftime('%Y-%m-%d'))
formattedthen = str(then.strftime('%Y-%m-%d'))

def lengthofsearch(inp):
    f = Filters(keyword = inp, start_date=formattedthen, end_date=formattednow, lang="English")
    articlesearch = gd.article_search(f)
    return len(articlesearch)

def querysearch(inp):
    f = Filters(keyword = inp, start_date=formattedthen, end_date=formattednow, lang="English")
    articlesearch = gd.article_search(f)
    return articlesearch

def tag_visible(element):
    blacklist = ['style', 'script', 'head', 'title', 'meta', '[document]', 'noscript', 'header', 'html', 'input']
    if element.parent.name in blacklist:
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll('p')
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.get_text().strip() for t in visible_texts)

def sitecontents(n, query):
    articles = querysearch(query)
    req = urllib.request.Request(articles['url'][n], headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    text = text_from_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').get_text()
    author_div = soup.find('div', class_="author_handle")
    
    if author_div:
        author = author_div.get_text()
    else:
        author = "Author not found"
    url = querysearch(query)['url'][n]

    return title, text, author, url