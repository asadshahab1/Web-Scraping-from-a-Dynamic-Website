
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def updateTable(r,fileType,bannerType):
    soup = BeautifulSoup(r.content,"html.parser")
    tables = soup.find_all("table",{"class":'TableLined'})
    banner = soup.find("td",{"class":bannerType}).string.strip()
    str=""
    for i in tables:
        str=i.prettify()
    with open("abc.html","w") as v:
        v.write(str)
    with open("abc.html","r") as v:
        with open(fileType,"a+") as f:
            df = pd.read_html(v)
            df[0].pop(0)
            dataFrame = pd.DataFrame(df[0])
            dataFrame['Name']=[banner]*len(dataFrame)
            dataFrame.to_csv(f)
def runTheProgram(match_type,fileType,bannerType):
    URL = "http://howstat.com/cricket/Statistics/Players/PlayerCountryList.asp"
    driver = webdriver.Firefox()
    driver.get(URL)
    recent_players =driver.find_element("name","chkCurrent")
    recent_players.click()
    time.sleep(15)
    type_select = Select(driver.find_element("name","cboFormat"))
    type_select.select_by_value(match_type)
    time.sleep(10)
    select = Select(driver.find_element("name","cboCountry"))
    select.select_by_visible_text('India')
    time.sleep(10)
    link = driver.page_source
    driver.close()
    soup = BeautifulSoup(link,"html.parser")
    matches = soup.findAll("a",{"class":"LinkTable"})
    links = []
    for i in range(len(matches)):
        if i%2!=0:
            links.append(matches[i].get('href'))
    for i in links:
        match_page = requests.get("http://howstat.com/cricket/Statistics/Players/"+i)
        updateTable(match_page,fileType,bannerType)

runTheProgram("T","tests.csv","Banner1")
runTheProgram("O","ODI.csv","Banner2")
runTheProgram("W","T20.csv","Banner2")