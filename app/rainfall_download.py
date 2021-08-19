
import requests, sys, webbrowser
import csv, time 
import datetime
import logging

from datetime import timedelta
from flutils import *
from dbutils import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
 

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "work/download",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})



meter_no = ""
download_url = ""
last_download = datetime.datetime.now()
downloads_dir = ""
logs_dir = ""

def rainfall_scrape_and_write(meter_no, download_url, last_download, downloads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)
    
    yesterday = datetime.datetime.today() - timedelta(days=1)
    sdate = check_start_end_dates('rainfall', meter_no)
    edate = (yesterday).strftime('%d/%m/%Y')  # edate == today - 1
    ldate = (yesterday).strftime('%Y%m%d')    # ldate = logfile date
    
    if last_download > yesterday:
        logging.info(' Start date ' + str(last_download) + ' is greater than the end date ' + str(yesterday) + '. Exiting. ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        return
    else:
        logging.info(' ' + meter_no + ' scraping started for ' + str(last_download) + ' to ' + str(yesterday) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))    

    
    driver = webdriver.Chrome(options=chrome_options)    # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file

    driver.get(download_url)
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image0.png')
    # print("Page title was '{}'".format(driver.title))

    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='webhyd']")))

    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='gwgwcf_org']")))


    #ready = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//table[@id='dataTable']"))) 
    ready = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='dataTable']"))) 
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image1.png')

    dropdown = driver.find_element(By.ID, 'p_startYear')
    startyearSelect = Select(dropdown)     #.text.splitlines() 
    startyear = startyearSelect.first_selected_option.text

    table = driver.find_element(By.XPATH, "//table[@id='dataTable']")

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image2.png')

    with open(downloads_dir + meter_no + '_' + str(startyear) + '_' + ldate + '.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
       
        mth = ['1','2','3','4','5','6','7','8','9','10','11','12']
        wr.writerow(mth)
#        wr.writerow(yr)                     # insert the year of record on row 1

        for row in table.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image3.png')

    driver.quit()

    logging.info(' Scraping ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))