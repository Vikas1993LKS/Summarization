# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:31:55 2020

@author: Vikas.gupta
"""

import os
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from selenium.webdriver.common.keys import Keys


import datetime

start = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y")
end = datetime.datetime.strptime("31/12/2020", "%d/%m/%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

date_list = []

for date in date_generated:
    date_list.append(date.strftime("%d/%m/%Y"))


chrome_options = Options()
download_dir = r'/Summarization/data/Delhi/2020'

try:
    os.makedirs(download_dir)
except:
    pass

Bench_name = input("Please enter the bench for which judgments are required")

def scrapper(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,  # Change default directory for downloads
    "download.prompt_for_download": False  # To auto download the file
    })
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)
    #Bench_selection= driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[3]/td[1]/select")
    initial_links = []
    for date in date_list:
        time.sleep(3)
        print (date)
        driver.get(url)
        if (Bench_name == "Agra"):
            Bench_Selection = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/section/div/div/div/div/div/div/div/div[2]/select/option[2]")
            Bench_Selection.click()
        elif (Bench_name == "Bangalore"):
            Bench_Selection = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[3]/td[1]/select/option[6]")
            Bench_Selection.click()
        elif (Bench_name == "Chennai"):
            Bench_Selection = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[3]/td[1]/select/option[9]")
            Bench_Selection.click()
        elif (Bench_name == "Delhi"):
            Bench_Selection = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[3]/td[1]/select/option[13]")
            Bench_Selection.click()
        date_selection = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[5]/td[1]/input")
        time.sleep(2)
        date_selection.send_keys(date)
        search_button_click = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[4]/td[4]/button[1]")
        search_button_click.click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/main/div/div/form/table/tbody/tr[5]/td[1]/input").clear()
        try:
            pdf_table = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/table")
            for data in pdf_table.find_elements_by_xpath(".//a"):
                initial_links.append(data.get_attribute("href"))
        except:
            pass
    for new_url in initial_links:
        try:
            driver.get(new_url)
            pdf_element = driver.find_element_by_xpath("/html/body/div/main/div/div/div/section[2]/div/table/tbody/tr[5]/td[2]/a")
            pdf_element_link = pdf_element.get_attribute("href")
            time.sleep(3)
            driver.get(pdf_element_link)
        except:
            pass
        # data.click()
        # window_after = driver.window_handles[1]
        # time.sleep(3)    
        # driver.switch_to.window(window_after)
        # pdf_element = driver.find_element_by_xpath("/html/body/div/main/div/div/div/section[2]/div/table/tbody/tr[5]/td[2]/a")
        # pdf_element_link = pdf_element.get_attribute("href")
        # driver.get(pdf_element_link)
url = "https://www.itat.gov.in/judicial/tribunalorders"

scrapper(url)
