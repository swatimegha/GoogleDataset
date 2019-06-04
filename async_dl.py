import aiohttp
import asyncio
from downloader import Downloader
import re
import os
import ssl

PARALLELISM = 50

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


def google_search(link_file,  category2):
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    for j in search(category2, num=200, stop=200, pause=2):
        #print(j)
        try:
            with open(link_file,'a+', encoding="utf-8") as f:
                f.write(j)
                f.write('\n')
        except IOError:
            print("Error of writing files")


if __name__ == '__main__':
    # TODO: reading of labels from csv file can be added
    link_file='D:\\MSIT\\2019-2ndSem\\Industrial projects\\Google_Dataset\\link.txt'
    output = 'D:\\MSIT\\2019-2ndSem\\Industrial projects\\Google_Dataset\\'
    google_search(link_file, "about ballet dance")
    dl = AsyncDownloader(link_file, "artEnt", "dance", output)
    asyncio.run(dl.main())