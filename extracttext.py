import json
import time
from newspaper import Article

def readJSON(JSONfilepath, count):
    with open(JSONfilepath,'r') as sample:
        for line in sample:
            obj = json.loads(line.strip())
            #print("category: " + str(obj['category']))
            #print("headline: " + str(obj['headline']))
            #print("link: " + str(obj['link']))
            count=count+1
            print('no of records processed:' + str(count))
            #if count >1400:for split7
            #if count >1401:
            if count >527:#if count >81 and 146 527:
                prepareTextFile(str(obj['category']), str(obj['link']), count)


def prepareTextFile(category, url, count):
    article = Article(url)
    article.download()
    while article.download_state == 0: #ArticleDownloadState.NOT_STARTED is 0
        time.sleep(1)
    article.parse()

    # print(article.title)
    # print(article.text)
    #print(article)
    with open ('D:\\MSIT\\2019-2ndSem\\Industrial projects\\Code\\corpus\\news-category-dataset\\splitjson\\extract_text\\split_8.txt', 'a+', encoding="utf-8") as f:
        f.write('\n')
        f.write('__label__')
        f.write(category)
        f.write('\n')
        f.write(article.title)
        f.write('\n')
        f.write(article.text)
        f.write('\n')
        f.write('\n')
        print('records written:' + str(count))

count = 0
JSONfilepath='D:\\MSIT\\2019-2ndSem\\Industrial projects\\Code\\corpus\\news-category-dataset\\splitjson\\split_8.json'
readJSON(JSONfilepath, count)
