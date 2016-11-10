import alexa
from bs4 import BeautifulSoup
import requests
import requests_cache

requests_cache.install_cache('cache')

list = alexa.get_list(100)

for website in list:
  print(website[1])
  try:
    response = requests.get("http://" + website[1])
    soup = BeautifulSoup(response.text, "lxml")
    # Extracting script file sources
    for script in soup.find_all('script'):
      source = script.get('src')
      # Skipping inline scripts
      if source != None:
        # Considering only jquery scripts
        if 'jquery' in source:
          # Skipping scripts which host jquery on their own domain
          if (website[1].split(".")[0] not in source) and (source.startswith('http') or source.startswith('//')):
            print(source)
  except:
    continue
