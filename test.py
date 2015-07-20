import urllib, urllib2 
from bs4 import BeautifulSoup
import string

url = "http://es.goolzoom.com/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

div = soup.find('div', id='divTextboxBuscador')
if div != None:
    print 'trobat'
raw_input()

