from bs4 import BeautifulSoup
import requests
import re


def scrape_uw_alerts():
    prev_alert_list = ['no alerts']
    newest_alert_list = []
    date_counter = 0
    same_alert_flag = True
    pattern = "(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}"

    URL = "https://emergency.uw.edu/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,"html.parser")
    mainContent = soup.find(id="main_content")
    p_tags = mainContent.find_all('p')
    for p in p_tags:
        if re.match(pattern,p.text):
            date_counter+=1
        if date_counter<2:
            newest_alert_list.append(p)
    print(len(newest_alert_list))
    print(len(prev_alert_list))
    if(len(newest_alert_list) != len(prev_alert_list)):
        same_alert_flag = False
    else:
        for i in range(len(newest_alert_list)):
            if newest_alert_list[i].text != prev_alert_list[i].text:
                same_alert_flag = False
            else:
                pass
    
    if same_alert_flag == False:
        return newest_alert_list
    return None
