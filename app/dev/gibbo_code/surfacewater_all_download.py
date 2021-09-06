
import sys, webbrowser
import csv, time 
import datetime
import logging

from datetime import timedelta
from flutils_all import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
 

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "./downloads",
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

def surfacewater_scrape_and_write(meter_no, download_url, date_1, downloads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)
        
    date_2 = date_1 + timedelta(days=18)
    sdate = (date_1).strftime('%d/%m/%Y')
    edate = (date_2).strftime('%d/%m/%Y')  # edate == today - 1
    run_date = datetime.datetime.today()
    ldate = (run_date).strftime('%Y%m%d')    # ldate = logfile date
    
    logging.info(' ' + meter_no + ' scraping started for ' + str(sdate) + ' to ' + str(edate) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    driver = webdriver.Chrome(options=chrome_options)    # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
#    logging.info(' ' + meter_no + ' defined webdriver.Chrome, about to get URL ' + download_url + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    driver.get(download_url)
#    logging.info(' ' + meter_no + ' completed download url' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    # print("Page title was '{}'".format(driver.title))

    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='webhyd']")))

    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='rsrscf_org']")))


    sf_swl = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selorder__100.00_100.00__1']")))
    # should be checked already

    
    sf_dr = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selorder__100.00_141.00__1']")))   
    sf_dr.click()
    
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image1.png') 

    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rs_period")))
    finally:
        s1 = Select(driver.find_element_by_id('rs_period'))
        s1.select_by_visible_text('Custom')

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image2.png')

    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "output")))
    finally:
        s2 = Select(driver.find_element_by_id('output'))
        s2.select_by_visible_text('Table')

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image3.png')
    
    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "interval")))
    finally:
        s3 = Select(driver.find_element_by_id('interval'))
        s3.select_by_visible_text('15 minutes')

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image4.png')

    time.sleep(2)

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cdate1")))
    finally:
        sf_sdate = driver.find_element(By.ID, 'cdate1')
        sf_sdate.clear()
        sf_sdate.send_keys(sdate)
    
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cdate2")))
    finally:
        sf_edate = driver.find_element(By.ID, 'cdate2')
        sf_edate.clear()
        sf_edate.send_keys(edate)
    
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image5.png')

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='submit']")))
    finally:
        get_output_button = driver.find_element_by_xpath("//button[@id='submit']")
        get_output_button.click()

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image6.png')

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'OK')]")))
    finally:
        get_output_button = driver.find_element_by_xpath("//button[contains(text(),'OK')]")
        get_output_button.click()

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image7.png')

    WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//body/div[4]/div[1]/div[1]/div[1]/div[1]/iframe[1]")))

    # //body/div[4]/div[1]/div[1]/div[1]/div[1]/iframe[1]

    table = driver.find_element(By.XPATH, "//body/div[@id='wrapper']/div[2]/table[1]")

    with open(downloads_dir + meter_no + '_' + ldate + '.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        
        for row in table.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image8.png')

    driver.quit()
    logging.info(' Scraping ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
