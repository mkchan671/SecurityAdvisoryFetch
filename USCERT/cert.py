#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup as bs
import asyncio
import re
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
"""
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.utils import ChromeType
#from selenium.webdriver.chrome.options import Options
#from pyvirtualdisplay import Display

#display = Display(visible=False, size=(800, 600)).start()



#browser = webdriver.Chrome(options=chrome_options)
"""
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

browser = webdriver.Chrome(executable_path="./chromedriver.exe",options=chrome_options)
vulnRank = ["High","Medium","Low","Not Yet Assigned"]
df = pd.read_csv("certList.csv")
"""
#init driver
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()
browser = webdriver.Firefox(firefox_options=fireFoxOptions)
"""
#url
baseUrl = "https://us-cert.cisa.gov/ncas/bulletins/"
codeList= df["certID"]
#init
dataT = []
header = True
for code in codeList:
    url = baseUrl + code
    r = browser.get(url)
    #wait page to load
    delay = 5 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'low_v')))
        print ("Page is ready!")
        #print (myElem.text)
    except TimeoutException:
        print ("Loading took too much time!")

    soup = bs(browser.page_source.encode(encoding='utf-8',errors='replace'), "html.parser")
    "save to .csv"
    filename = "USCERT-Bulletins-" + code + ".csv"
    #csv_writer = csv.writer(open(filename, 'w', encoding='utf-8'))

    vulnI = -1
    for tr in soup.find_all("tr"):
        data = []
        # for headers ( entered only once - the first time - )
        for th in tr.find_all("th"):
            data.append(th.text)
        if data:
            #print("Inserting headers : {}".format(','.join(data)))
            data.append("Vuln")
            if(vulnI == -1 and header):
                data.insert(0,"Source \n(H -HK-CERT/\nU - US-CERT/\nM - MSS)")
                data.insert(len(data)-1,"Relevant to Corporate IT \n(Yes / No / Maybe)")
                dataT.append(data)
                header = False
            vulnI +=1;
            continue

        for td in tr.find_all("td"):
            if td.a:
                data.append(td.a.text.strip())
            else:
                data.append(td.text.strip())

        if data:
            #print("Inserting data: {}".format(','.join(data)))
            #TODO: replace to "=HYPERLINK("https://google.com","abc")"
            data.insert(0," ")
            data.append(vulnRank[vulnI])
            data.insert(len(data)-1," ")
            dataT.append(data)
savedf = pd.DataFrame(dataT)
savedf.to_csv(filename, index=False, header=False)
#csv_writer.writerow("")
#close driver        
browser.quit()
print("Browse Completed, quit")
#display.stop()