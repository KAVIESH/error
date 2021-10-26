from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

StartUrl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome('chromedriver.exe')
browser.get(StartUrl)
time.sleep(10)
planetData = []
newPlanetData = []

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

def Scrape():

    for i in range(0, 454):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tag = ul_tag.find_all("li")
            templist = []
            for index, li_tags in enumerate(li_tag):
                if index == 0:
                    templist.append(li_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(li_tags.contents[0])
                    except:
                        templist.append('')

            hyperlinkTag = li_tag[0]

            templist.append("https://exoplanets.nasa.gov/"+ hyperlinkTag.find_all("a", href = True)[0]["href"])
            planetData.append(templist)

        browser.find_elements_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()    
    

Scrape()

#Class 128

def ScrapeMoreData(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        templist = []
        for td_tag in td_tags:
            try:
                templist.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0]) 
            except:
                templist.append("")
        
        newPlanetData.append(templist)

for data in planetData:
    ScrapeMoreData(data[5])
finalPlanetData = []
for index, data in enumerate(planetData):
    finalPlanetData.append(data + finalPlanetData[index])

with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalPlanetData)




        