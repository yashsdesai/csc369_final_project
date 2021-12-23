from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from pyspark import SparkConf
from pyspark import SparkContext
import rsa
import json
import time
import os
import sys
import csv

LOAD_DELAY = 3

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

def scrape_jobs(driver):
    jobs = driver.execute_script(
        "return (function(){ var jobs = []; var els = document.getElementById("
        "'experience-section').getElementsByTagName('ul')[0].getElementsByTagName('li'); for (var i=0; "
        "i<els.length; i++){   if(els[i].className!='pv-entity__position-group-role-item-fading-timeline'){   "
        "  if(els[i].getElementsByClassName('pv-entity__position-group-role-item-fading-timeline').length>0){ "
        "     } else {       try {         position = els[i].getElementsByClassName("
        "'pv-entity__summary-info')[0].getElementsByTagName('h3')[0].innerText;       }       catch(err) { "
        "position = ''; }        try {         company_name = els[i].getElementsByClassName("
        "'pv-entity__summary-info')[0].getElementsByClassName('pv-entity__secondary-title')[0].innerText;     "
        "  } catch (err) { company_name = ''; }        try{         date_ranges = els["
        "i].getElementsByClassName('pv-entity__summary-info')[0].getElementsByClassName("
        "'pv-entity__date-range')[0].getElementsByTagName('span')[1].innerText;       } catch (err) {"
        "date_ranges = ''; }        try{         job_location = els[i].getElementsByClassName("
        "'pv-entity__summary-info')[0].getElementsByClassName('pv-entity__location')[0].getElementsByTagName("
        "'span')[1].innerText;       } catch (err) {job_location = ''; }        try{         company_url = "
        "els[i].getElementsByTagName('a')[0].href;       } catch (err) {company_url = ''; }        jobs.push("
        "[position, company_name, company_url, date_ranges, job_location]);     }   } } return jobs; })();")

    return jobs

def search(driver, name, university=None, company=None):
    search_bars = driver.find_elements(By.CLASS_NAME, "search-global-typeahead__input")
    search_keywords = search_bars[0]
    search_keywords.send_keys(name)
    search_keywords.send_keys(Keys.RETURN)
    time.sleep(LOAD_DELAY)

    driver.find_element(By.LINK_TEXT, "See all people results").click()
    time.sleep(LOAD_DELAY)

    results = driver.find_elements(By.CLASS_NAME, "entity-result__item")

    for entry in results:
        try:
            subtitle = entry.find_element(By.CLASS_NAME, "entity-result__primary-subtitle")
            if(university in subtitle.text or company in subtitle.text):
                entry.click()
                break


        except:
            print("failed")

def print_single_result(name, rdd):
    print(name + ": {")
    for i in rdd.collect():
        print("\t" + i + ",")

if __name__== "__main__":

    print(sys.argv)
    print("Load delay: " + str(LOAD_DELAY))
    print("Welcome to Scraper 1.0")
    print("**WARNING: ONLY COMPATIBLE WITH CHROMIUM-BASED BROWSERS**")

    f = open("credentials.txt", "rt")
    email = f.readline()
    password = f.readline()
    f.close()


    print("For any unknown fields, hit RETURN")
    name = input("Enter name: ")
    university = input("Enter university: ")
    company = input("Enter company: ")

    # Initialize chromium webdriver
    driver_path = str(os.getcwd()) + "/chromedriver"
    service = Service(driver_path)
    options = Options()

    # replace with your own browser path
    options.binary_location = "/usr/bin/brave-browser"

    driver = webdriver.Chrome(options=options, service=service)
    driver.set_window_size(3000, 1024)

    if(name == None or name == ""):
        print("Name is required")
        exit()

    driver.get("https://linkedin.com/login")
    time.sleep(LOAD_DELAY)


    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    #driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    driver.get("https://linkedin.com/feed/")
    time.sleep(LOAD_DELAY)

    search(driver, name, university, company)
    time.sleep(LOAD_DELAY)

    jobs = scrape_jobs(driver)
    jobs_rdd = sc.parallelize(jobs)
    #role = input("Relevant Role: ")

    #jobs.rdd.filter(lambda x: role in x)
    jobs_rdd = jobs_rdd.map(lambda x: (x[1], x[0]))

    print("\n" + name + ":")

    for i in jobs_rdd.collect():
        print(i)





