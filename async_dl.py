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

def prepare_dir_gen_url(path, sk, num):
    if os.path.exists(path):
        print("Path exist")
    else:
        os.makedirs(path)
        print("Dir created")
    u = path + '/' + sk + '.txt'
    ua = path + '/' + '_URLS' + '.txt'
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    try:
        with open(ua, 'a+', encoding="utf-8") as fa:
            fa.write("........" + sk + "........")
            fa.write('\n')
    except IOError: \
            print("Error of writing files")

    for j in search(sk, tld="co.in", num=int(num), stop=int(num), pause=15):
        try:
            with open(u, 'a+', encoding="utf-8") as f, open(ua, 'a+', encoding="utf-8") as fa:
                f.write(j)
                f.write('\n')
                fa.write(j)
                fa.write('\n')
        except IOError:
            print("Error of writing files")

if __name__ == '__main__':
    # TODO: reading of labels from csv file can be added
    out_dir = 'output'
    with open('cats.csv','rt')as f:
        data = csv.reader(f)
        for row in data:
            print("level 1: " + row[0] + " || level 2: " + row[1] + " || search key: " + row[2] + " noOfLinks:" + str(NUM_OF_LINKS))
            l1 = row[0].title().replace(" ", "")
            l2 = row[1].title().replace(" ", "")
            path = out_dir + '/' + l1
            print(l1)
            prepare_dir_gen_url(path, row[2], NUM_OF_LINKS)
            time.sleep(SLEEP_TIME_IN_SEC)
            #link_file = path + '/url.txt'
            #print("........link file generated.........")
            #google_search(row[0], row[1], row[2], row[3])
            #google_search(link_file, "about ballet dance")
            #dl = AsyncDownloader(link_file, l1, l2, path)
            #asyncio.run(dl.main())
            #os.remove(link_file)
            #print("........link file removed.........")

