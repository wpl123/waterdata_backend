
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



# meter_no = ""
# download_url = ""
# last_download = datetime.datetime.now()
# downloads_dir = ""
# logs_dir = ""

def groundwater_3col_scrape_and_write(meter_no, download_url, last_download, downloads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)

    yesterday = datetime.datetime.today() - timedelta(days=1)
    sdate = check_start_end_dates('groundwater', meter_no)
    edate = (yesterday).strftime('%d/%m/%Y')  # edate == today - 1
    ldate = (yesterday).strftime('%Y%m%d')    # ldate = logfile date
    

    if last_download > yesterday:
        logging.info(' Start date ' + str(last_download) + ' is greater than the end date ' + str(yesterday) + '. Exiting. ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        return
    else:
        logging.info(' ' + meter_no + ' scraping started for ' + str(last_download) + ' to ' + str(yesterday) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))    

    driver = webdriver.Chrome(options=chrome_options)    # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file

    driver.get(download_url)

    # print("Page title was '{}'".format(driver.title))

    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='webhyd']")))

    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='gwgwcf_org']")))


    bl_bmp = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selorder__110.00_110.00__1']")))
    # should be checked already

    # time.sleep(1)
    bl_ahd = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selorder__110.00_115.00__1']")))   
    bl_ahd.click()
    
    # time.sleep(1)
    bl_temp = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='selorder__2080.00_2080.00__1']")))
    bl_temp.click()
    
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image1.png') 

    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "gw_period")))
    finally:
        s1 = Select(driver.find_element_by_id('gw_period'))
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
        s3.select_by_visible_text('Daily')

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image4.png')

    time.sleep(2)

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cdate1")))
    finally:
        bl_sdate = driver.find_element(By.ID, 'cdate1')
        bl_sdate.clear()
        bl_sdate.send_keys(sdate)
    
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cdate2")))
    finally:
        bl_edate = driver.find_element(By.ID, 'cdate2')
        bl_edate.clear()
        bl_edate.send_keys(edate)
    
    driver.save_screenshot(logs_dir + meter_no + '_' + 'image5.png')

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='submit']")))
    finally:
        get_output_button = driver.find_element_by_xpath("//button[@id='submit']")
        get_output_button.click()

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image6.png')

    WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//body/div[4]/div[1]/div[1]/div[1]/div[1]/iframe[1]")))

    table = driver.find_element(By.XPATH, "//body/div[@id='wrapper']/div[2]/table[1]")

    with open(downloads_dir + meter_no + '_' + ldate + '.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        
        for row in table.find_elements_by_css_selector('tr'):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

    driver.save_screenshot(logs_dir + meter_no + '_' + 'image7.png')

    driver.quit()

    logging.info(' Scraping ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))