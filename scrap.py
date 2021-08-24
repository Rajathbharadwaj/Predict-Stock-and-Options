import requests
import pprint
from bs4 import BeautifulSoup

URL = 'https://in.investing.com/indices/bank-nifty'
r =  requests.get(URL)
print(r.content)
soup = BeautifulSoup(r.content, 'lxml')
print(soup.prettify())
val = soup.find('div', 
                   attrs={'class':'last-price'})
print(val)