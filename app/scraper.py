from bs4 import BeautifulSoup
import requests
URL = "https://emergency.uw.edu/"
page = requests.get(URL)
soup = BeautifulSoup(page.content,"html.parser")
mainContent = soup.find(id="main_content")
print(mainContent.prettify())

for element in mainContent.title.next_elements:
    print(repr(element))