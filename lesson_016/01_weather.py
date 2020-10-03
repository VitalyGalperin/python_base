# -*- coding: utf-8 -*-
import bs4
import requests


# response1 = requests.get('https://darksky.net/forecast/29.5516,34.9439/ca12/en').text
response = requests.get('https://darksky.net/details/29.5563,34.9525/2020-10-3/ca12/en').text

soup = bs4.BeautifulSoup(response, 'html.parser')

spans = soup.find_all('span')
script = soup.find_all('script')

for span in spans:
    if str(span).find('pressure') != -1:
        print(span)



