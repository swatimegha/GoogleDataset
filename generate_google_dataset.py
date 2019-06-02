import csv
from downloader import Downloader
import re
import os

def googleSearch(category1, category2):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    label1 = category1.title().replace(" ", "")
    label2 = category2.title().replace(" ", "")
    for j in search(category2, tld="co.in", num=200, stop=200, pause=2):
        #print(j)
        prepareTextFile(label1, label2, j)

def prepareTextFile(label1, label2, url):
    dir = 'D:\\MSIT\\2019-2ndSem\\Industrial projects\\Google_Dataset\\'
    path = dir + label1
    if os.path.exists(path):
        print("Path exist")
    else:
        os.makedirs(path)
        print("dir created")
    f1 = path + '\\' +label1 + '.txt'
    f2 = path + '\\' +label2 + '.txt'
    u = path + '\\' + 'url.txt'


    #article = Downloader.download_article(url)
   # article = Downloader.parse_article(article)
    article = Downloader.get_article(url)
    art = article.text
    art = re.sub(' +', ' ', art.replace('\n',' '))

    try:
        with open(f1,'a+', encoding="utf-8") as f1, open (f2,'a+', encoding="utf-8") as f2, open(u,'a+', encoding="utf-8") as u:

            u.write(url)
            u.write('\n')
            f1.write('\n__label__' + label1 + ' ')
            f1.write(art)
            f2.write('\n__label__' + label2 + ' ')
            f2.write(art)

        # remove_empty_lines(file_storage+data_filename)
        # print('records written:' + str(count))
    except:
        print("Error of parsing")



with open('D:\\MSIT\\2019-2ndSem\\Industrial projects\\Google_Dataset\\ibm-cat-list.csv','rt')as f:
    data = csv.reader(f)
    for row in data:
        print("level 1: " + row[0] + "level 2: " +row[1])
        googleSearch(row[0], row[1])