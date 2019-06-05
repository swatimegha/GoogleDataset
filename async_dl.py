import time
import aiohttp
import asyncio
from downloader import Downloader
import re
import os
import ssl
import csv

PARALLELISM = 50
NUM_OF_LINKS = 250
SLEEP_TIME_IN_SEC = 240 # 4 min 

class AsyncDownloader:

    def __init__(self, file, label1, label2, output):
        with open(file, 'rt') as f:
            self.urls = [x.strip() for x in f]
            self.output_dir = output
            self.label1 = label1
            self.label2 = label2

    async def fetch(self, session, url, sem):
        try:
            async with session.get(url) as response, sem:
                if response.status != 200:
                    response.raise_for_status()
                return await response.text()
        except:
            return ""

    async def fetch_all(self, session, sem):
        results = await asyncio.gather(
            *[asyncio.create_task(self.fetch(session, url, sem)) for url in self.urls]
        )
        return results

    async def main(self):
        sem = asyncio.Semaphore(PARALLELISM)
        async with aiohttp.ClientSession() as session:
            htmls = await self.fetch_all(session, sem)
            for html in htmls:
                try:
                    art = Downloader.get_article("", html).text
                    art = re.sub(' +', ' ', art.replace('\n',' '))
                    self.save_to_file(art)
                except:
                    print("Cannot parse page")

    # TODO: file tree hierarchy can be optimized/changed
    def save_to_file(self, text):
        if text.strip().startswith("<") or text.strip().startswith('{'):
            return
        path = self.output_dir + '/' + self.label1
        if os.path.exists(path):
            print("Path exist")
        else:
            os.makedirs(path)
            print("Dir created")
        f1 = path + '/' + self.label1 + '.txt'
        f2 = path + '/' + self.label2 + '.txt'

        try:
            with \
                    open(f1, 'a+', encoding="utf-8") as f1, \
                    open(f2, 'a+', encoding="utf-8") as f2:

                f1.write('\n__label__' + self.label1 + ' ')
                f1.write(text)
                f2.write('\n__label__' + self.label2 + ' ')
                f2.write(text)

        except IOError:
            print("Error of writing files")

def prepare_dir_gen_url(path, subcat, search_key, num):
    if os.path.exists(path):
        print("Path exist")
    else:
        os.makedirs(path)
        print("Dir created")
    sk_path = path + '/' + search_key + '.txt'
    subcat_path = path + '/' + '_' + subcat + '.txt'
    cat_path = path + '/' + '_URLS' + '.txt'
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    for j in search(sk, tld="co.in", num=int(num), stop=int(num), pause=15):
        try:
            with open(sk_path, 'a+', encoding="utf-8") as fsk, open(subcat_path, 'a+', encoding="utf-8") as fsubcat, open(cat_path, 'a+', encoding="utf-8") as fcat:
                fsk.write(j)
                fsk.write('\n')
                fsubcat.write(j)
                fsubcat.write('\n')
                fcat.write(j)
                fcat.write('\n')
        except IOError:
            print("Error of writing files")

if __name__ == '__main__':
    out_dir = 'output'
    with open('cats.csv', 'rt') as f:
        data = csv.reader(f)
        for row in data:
            sk = row[2]
            print("level 1: " + row[0] + " || level 2: " + row[1] + " || search key: " + sk + " noOfLinks:" + str(NUM_OF_LINKS))
            l1 = row[0].title().replace(" ", "")
            l2 = row[1].title().replace(" ", "")
            path = out_dir + '/' + l1
            print(l1)
            prepare_dir_gen_url(path, row[1], sk, NUM_OF_LINKS)
            time.sleep(SLEEP_TIME_IN_SEC)

