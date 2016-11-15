from bs4 import BeautifulSoup
import requests
from math import ceil

ALEXA_URL="http://www.alexa.com/topsites/global"

def get_top_websites_global(n=100):
  count = 0
  list = []

  pages = int(ceil(n/25.0))

  for page in range(0, pages):
    response = requests.get(ALEXA_URL + ";" + str(page))

    soup = BeautifulSoup(response.text, "lxml")
    websites = soup.find_all('li', {'class':'site-listing'})

    for website in websites:
      count = count + 1
      if count > n:
        break
      list.append( (website.div.contents[0], website.a.contents[0].lower() ) ) 

    if count > n:
      break

  return list
