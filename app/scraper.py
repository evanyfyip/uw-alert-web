from bs4 import BeautifulSoup
import requests

#scrapes UW alerts for all the text for each alert. 
def scrape_uw_alerts():
    URL = "https://emergency.uw.edu/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,"html.parser")
    mainContent = soup.find(id="main_content")
    p_tags = mainContent.find_all('p')
    return p_tags