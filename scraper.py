import requests
from bs4 import BeautifulSoup


url = "https://www.ceneo.pl/95365253#tab=reviews"
response = requests.get(url)

page_dom = BeautifulSoup(response.text, 'html.parser')

