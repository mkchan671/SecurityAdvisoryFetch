#!/usr/bin/python3
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
import asyncio
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
"""
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.utils import ChromeType
#from pyvirtualdisplay import Display

#display = Display(visible=False, size=(800, 600)).start()


#browser = webdriver.Chrome(options=chrome_options)


fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
browser = webdriver.Firefox(options=fireFoxOptions)
"""
#init driver
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
browser = webdriver.Chrome(executable_path="./chromedriver.exe",options=chrome_options)
#url

#baseUrl = "https://support.f5.com/csp/article/"
df = pd.read_csv("f5CodeList.csv")
#save to CSV
filename = "f5.csv"
#csv_writer = csv.writer(open(filename, 'w', encoding='utf-8'))
dataToSave = []
##TODO
#url = baseUrl + code
#dateToSave.append()
headerInc = True
for url in df["Link"]:
    r = browser.get(url)
    #wait page to load
    delay = 5 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'askf5table')))
        print ("Page is ready!")
        print (myElem.text)
    except TimeoutException:
        print ("Loading took too much time!")
        dataToSave.append(["","APM None\nLTM None\nDNS None"])

    soup = bs(browser.page_source.encode(encoding='utf-8',errors='replace'), "html.parser")
    code = soup.find("span", {"class":"ng-binding ng-scope"}).text
    print (code)
    rowSpanCounter = 0
    colWithSpan = []
    rowAdd = 0
    
    for tr in soup.find_all("tr"):
        data = []
        # for headers ( entered only once - the first time - )
        for th in tr.find_all("th"):
            data.append(th.text)
        if data and headerInc:
            print("Inserting headers : {}".format(','.join(data)))
            #csv_writer.writerow(data)
            dataToSave.append(data)
            headerInc = False
        else:
            data.clear()

        for td in tr.find_all("td"):
            #Check if contain any APM LTM DNS product, none return none


            if td.a:
                data.append(td.a.text.strip())
            else:
                data.append(td.text.strip())
            if(rowSpanCounter > 0 and not rowAdd):
                #addSpace in col ind
                data.insert(0,' ')
                rowSpanCounter -= 1
                rowAdd = 1
            else:
                if (td.has_attr('rowspan')):
                        rowSpanCounter = int(td.get('rowspan',1)) -1
                        colWithSpan.append(0)
                        rowAdd = 1
                """
                for colInd in range(len(td)):
                    if (td[colInd].has_attr('rowspan')):
                        rowSpanCounter = int(td[colInd].get('rowspan',1))
                        colWithSpan.append(colInd)
                """
        if data:
            #print("Inserting data: {}".format(','.join(data)))
            #csv_writer.writerow(data)
            if(data[0]=="Product"):
                data.clear()
            else:
                dataToSave.append(data)
            rowAdd = 0
    #csv_writer.writerow([code,''])
    dataToSave.append([code,''])
saveDf = pd.DataFrame(dataToSave)
saveDf.to_csv(filename, index=False, header=False)
#close driver        
browser.quit()
#display.stop()