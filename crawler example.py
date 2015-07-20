import urllib
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import string

class Crawler:
    maximum = 0
    rec = 0
    s_url = 'http://es.goolzoom.com/'
    n_urls = 0
    visited_urls = {}

    def __init__(self, url, recursive, max_urls, count = 0, v_urls = {}):
        self.maximum = max_urls
        self.recursive = recursive
        self.s_url = url
        self.n_urls = count
        self.visited_urls = v_urls

    def explore(self):
        soup = self.get_parser()
        if(soup == None):
            return
        for link in soup.find_all('a'):
            if((self.n_urls >= self.maximum) and (self.maximum != 0)):
                break
            self.n_urls = self.n_urls+1
            if(self.recursive == 1):
                new_url = link.get('href')
                new_url = self.get_url(new_url)
                if(new_url != None):
                    if(self.visited(new_url) == False):
                        # print(new_url)
                        new_crawler = Crawler(new_url, self.recursive, self.maximum, self.n_urls, self.visited_urls)
                        new_crawler.explore()
            else:
                new_url = self.get_url(link.get('href')
                self.visited_urls[new_url] = 1
                 
    def get_parser(self):
        if((self.n_urls >= self.maximum) and (self.maximum > 0)):
            return None
        try:
            req = urllib.request.Request(self.s_url)
            page = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            return None

        self.visited_urls[self.s_url] = 1
        soup = BeautifulSoup(page)

        return soup

    def download_imgs(self):
        soup = self.get_parser()
        for img in soup.find_all('img'):
            img_url = self.get_url(img.get('src'))
            last_slash = img_url.rfind('/') + 1
            name = img_url[last_slash:]
            try:
                req = urllib.request.Request(img_url)
                page = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                continue
            f = open(name, 'bw')
            f.write(page.read())
            f.close()


    def visited(self,url):
        if (url in self.visited_urls):
            return True
        else:
            return False

    def get_url(self, url):
        if(url == None):
            return None
        if (len(url) <= 2):
            return None
        if(url[0:10] == 'javascript'):
            return None
        if((url[0:7] == 'http://') or (url[0:8] == 'https://')):
            return url
        else:
            last_slash = self.s_url.rfind('/')
            if(url[0:2] == '//'):
                new_url = self.s_url[0:last_slash] + url[1:]
            else:
                new_url = self.s_url[0:last_slash] + url
             
            return new_url

    def print_pages(self):
        for key in self.visited_urls.keys():
            print (key)

    def dump_to_file(self, filename = 'crawler_dump'):
        f = open(filename, 'a')
        for key in self.visited_urls.keys():
            f.write(key)
            f.write('\n')
        f.close()
