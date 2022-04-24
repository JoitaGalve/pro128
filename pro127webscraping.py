import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Chrome(r"C:\Users\Vijay\Downloads\chromedriver_win32\chromedriver")
browser.get(START_URL)
time.sleep(10)

headers = ["stars_name", "Distance", "Mass", "Radius", "Constellation", "right_ascension", "declination", "app_mag", "spectral_type", "brown_dwarf", "orbital_period", "semimajor_axis", "discovery_year"]
planet_data = []
new_planet_data = []
final_planet_data = []

def scrape():
    
    for i in range(0, 502):


        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])

                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        temp_list.append('')
            
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org" + hyperlink_li_tag.find_all("a", href = True)[0]["href"])

            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            
    '''with open("scraper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)'''

def scrape_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0])
            
            except:
                temp_list.append('')

        new_planet_data.append(temp_list)        

scrape()

for index, data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elm.replace("\n", '') for elm in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("final2.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)