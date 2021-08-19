import requests, sys, webbrowser, os
import time
import csv

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


driver = webdriver.Chrome(options=chrome_options)
driver.delete_all_cookies()

# set the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = "work/download/"
logs_dir     = "work/logs/"

os.makedirs(download_dir,mode = 0o666)
os.makedirs(logs_dir,mode = 0o666)

driver.get('https://realtimedata.waternsw.com.au/?ppbm=GW967138.1.1|419_NAMOI|GROUND_WATER&gw&1&gwcf_org')
#page_source_overview = driver.page_source


   
driver.save_screenshot(logs_dir + 'image1.png') 

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='webhyd']")))

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='gwgwcf_org']")))

time.sleep(1)

bl_bmp = driver.find_element(By.XPATH, "//input[@id='selorder__110.00_110.00__1']")
#bl_bmp.clear()
#bl_bmp.click()

time.sleep(1)

bl_ahd = driver.find_element(By.XPATH, "//input[@id='selorder__110.00_115.00__1']")   
#bl_bmp.clear()
bl_ahd.click()
time.sleep(1)

bl_temp = driver.find_element(By.XPATH, "//input[@id='selorder__2080.00_2080.00__1']")
#bl_bmp.clear()
bl_temp.click()

driver.save_screenshot(logs_dir + 'image2.png') 

time.sleep(1)
s1 = Select(driver.find_element_by_id('gw_period'))
s1.select_by_visible_text('Custom')

driver.save_screenshot(logs_dir + 'image3.png')

time.sleep(1)
s2 = Select(driver.find_element_by_id('output'))
s2.select_by_visible_text('Table')

driver.save_screenshot(logs_dir + 'image4.png')

time.sleep(1)
s3 = Select(driver.find_element_by_id('interval'))
s3.select_by_visible_text('Daily')

driver.save_screenshot(logs_dir + 'image5.png')

time.sleep(2)

bl_sdate = driver.find_element(By.ID, 'cdate1')
bl_sdate.clear()
bl_sdate.send_keys('14/12/2020')

time.sleep(2)
bl_edate = driver.find_element(By.XPATH, "//input[@id='cdate2']")
time.sleep(2)
bl_edate.clear()
bl_edate.send_keys('26/12/2020')

driver.save_screenshot(logs_dir + 'image6.png')

time.sleep(1)
get_output_button = driver.find_element_by_xpath("//button[@id='submit']")
time.sleep(2)
get_output_button.click()
time.sleep(20)

driver.save_screenshot(logs_dir + 'image7.png')

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//body/div[4]/div[1]/div[1]/div[1]/div[1]/iframe[1]")))

table = driver.find_element(By.XPATH, "//body/div[@id='wrapper']/div[2]/table[1]")

with open(download_dir + 'GW967138.1.1_20210112.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    
    for row in table.find_elements_by_css_selector('tr'):
        wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])


driver.save_screenshot(logs_dir + 'image8.png')

driver.quit()