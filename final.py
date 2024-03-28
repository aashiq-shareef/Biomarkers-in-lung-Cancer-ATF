import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
import time
import psutil
import subprocess
import pyautogui
import pygetwindow as gw
import win32api
from pathlib import Path
from urllib.parse import urlparse
import requests
import os

def read_tsv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def process_pos_gene_list_with_david(file_path):
    try:
        driver = webdriver.Chrome()
        driver.get("https://david.ncifcrf.gov/summary.jsp")

        gene_list_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "pasteBox")))
        gene_list_input.send_keys(file_path)

        identifier_dropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Identifier")))
        identifier_dropdown = Select(driver.find_element(By.NAME, "Identifier"))
        identifier_dropdown.select_by_value("OFFICIAL_GENE_SYMBOL")

        species_input = driver.find_element(By.ID, "speciesSelect")
        species_input.send_keys("Homo sapiens")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tt-suggestion tt-selectable' and text()='Homo sapiens']")))
        suggestion_element = driver.find_element(By.XPATH, "//div[@class='tt-suggestion tt-selectable' and text()='Homo sapiens']")
        suggestion_element.click()

        list_type_radio = driver.find_element(By.CSS_SELECTOR, "input[name='rbUploadType'][value='list']")
        list_type_radio.click()

        submit_button = driver.find_element(By.NAME, "B52")
        submit_button.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@value='Show Gene List']")))

        show_gene_list_button = driver.find_element(By.XPATH, "//button[@value='Show Gene List']")
        show_gene_list_button.click()

        download_link = driver.find_element(By.XPATH, "//a[contains(@href,'download')]")

        time.sleep(1)

        ActionChains(driver).context_click(download_link).perform()

        pyautogui.press('k')

        timeout = 10
        start_time = time.time()

        while "Save As" not in pyautogui.getActiveWindowTitle():
            if time.time() - start_time > timeout:
                print("Timeout: 'Save As' tab did not open within the specified time.")
                break
            time.sleep(1)

        pyautogui.press('backspace')

        pyautogui.typewrite("DavidSVRUpregulatedResult")
        time.sleep(1)

        pyautogui.press('enter')
        time.sleep(4)
        
    except TimeoutException as e:
        print("Timeout exception:", e)
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        print("DavidSVRUpregulatedResult has been download in your desktop")
        if driver:
            driver.quit()

##########################################################################################
            
def process_neg_gene_list_with_david(file_path):
    try:
        driver = webdriver.Chrome()
        driver.get("https://david.ncifcrf.gov/summary.jsp")

        gene_list_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "pasteBox")))
        gene_list_input.send_keys(file_path)

        identifier_dropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Identifier")))
        identifier_dropdown = Select(driver.find_element(By.NAME, "Identifier"))
        identifier_dropdown.select_by_value("OFFICIAL_GENE_SYMBOL")

        species_input = driver.find_element(By.ID, "speciesSelect")
        species_input.send_keys("Homo sapiens")

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tt-suggestion tt-selectable' and text()='Homo sapiens']")))
        suggestion_element = driver.find_element(By.XPATH, "//div[@class='tt-suggestion tt-selectable' and text()='Homo sapiens']")
        suggestion_element.click()

        list_type_radio = driver.find_element(By.CSS_SELECTOR, "input[name='rbUploadType'][value='list']")
        list_type_radio.click()

        submit_button = driver.find_element(By.NAME, "B52")
        submit_button.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@value='Show Gene List']")))

        show_gene_list_button = driver.find_element(By.XPATH, "//button[@value='Show Gene List']")
        show_gene_list_button.click()

        download_link = driver.find_element(By.XPATH, "//a[contains(@href,'download')]")

        time.sleep(1)

        ActionChains(driver).context_click(download_link).perform()

        pyautogui.press('k')

        timeout = 10 
        start_time = time.time()

        while "Save As" not in pyautogui.getActiveWindowTitle():
            if time.time() - start_time > timeout:
                print("Timeout: 'Save As' tab did not open within the specified time.")
                break
            time.sleep(1)
        
        pyautogui.press('backspace')

        pyautogui.typewrite("DavidSVRDownregulatedResult")
        time.sleep(1)

        pyautogui.press('enter')
        time.sleep(4)
        
    except TimeoutException as e:
        print("Timeout exception:", e)
    except Exception as e:
        print("An error occurred:", e)
        
    finally:
        print("DavidSVRDownregulatedResult has been download in your desktop")
        if driver:
            driver.quit()

##########################################################################################

def navigate_to_pos_data(file_path,cyto_path):

    cytoscape_executable_path = cyto_path
    subprocess.Popen([cytoscape_executable_path])

    cytoscape_window = None
    timeout = 60
    start_time = time.time()
    while time.time() - start_time < timeout:
        cytoscape_window = gw.getWindowsWithTitle('Session: New Session')
        if cytoscape_window:
            break
        time.sleep(1)

    if cytoscape_window:
        cytoscape_window = cytoscape_window[0]
        width = 1280
        height = 850
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        cytoscape_window.resizeTo(width, height)
        cytoscape_window.moveTo((screen_width - width) // 2, (screen_height - height) // 2)
    else:
        print("Cytoscape window not found within the timeout period.")
        
    try:
        driver = webdriver.Chrome()

        time.sleep(1)
        chrome_window = gw.getWindowsWithTitle('chrome')[0]
        chrome_window.activate()

        driver.get("https://string-db.org/")

        js_code = """
        var div = document.createElement('div');
        div.style.cssText = 'position: absolute; top: 50px; left: 10%; right: 10%; width: auto; height: auto; padding: 40px; font-size: 20px; font-weight: bold; text-align: center; z-index: 9999; color: black; overflow-y: auto; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); border-radius: 20px; font-family: Georgia, serif';
        div.innerHTML = "<p>ATTENTION USER:<br>This website will be automatically redirected to the Login page.</p>";
        div.innerHTML += "<p> Select Sign-Up: To create a new account and save the progress of your specific account on the website.</p>";
        div.innerHTML += "<p>Redirecting in 20Secs</p>";
        document.body.appendChild(div);

        var angle = 90; // Set the angle to 90 degrees for left to right gradient
        div.style.background = 'linear-gradient(' + angle + 'deg, #E4EfE9, #E4EfE9)';
        """
        driver.execute_script(js_code)

        time.sleep(20)

        my_data_link = driver.find_element(By.CSS_SELECTOR, "a.main_nav_tag[href*='/cgi/my?sessionId=']")
        my_data_link.click()

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button full_width']")))
        login_button.click()

        WebDriverWait(driver, 600).until(EC.url_contains("/cgi/my?"))
        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/my?"))

        gene_sets_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='my_page_selector MP_collapsed']")))
        gene_sets_element.click()

        create_new_gene_set_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cgi/uploadnewgeneset')]")))
        create_new_gene_set_element.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/uploadnewgeneset?"))

        gene_set_description_input = driver.find_element(By.ID, "geneset_description")
        gene_set_description_input.clear()
        gene_set_description_input.send_keys("UpRegulated")

        organism_search_input = driver.find_element(By.ID, "species_text_user_genelist")
        organism_search_input.clear()
        organism_search_input.send_keys("Homo sapiens")
        organism_search_input.click()

        text_area = driver.find_element(By.ID, "loginuser_geneset_items_uploaded")
        text_area.clear()
        text_area = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginuser_geneset_items_uploaded")))
        text_area.send_keys(file_path)

        checkbox = driver.find_element(By.ID, "loginuser_geneset_enable_statistics")
        driver.execute_script("arguments[0].click();", checkbox)

        continue_button = driver.find_element(By.XPATH, "//input[@value='Continue ->']")
        continue_button.click()

        continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue ->']")))
        continue_button.click()

        ok_button = driver.find_element(By.XPATH, "//input[@value='OK']")
        ok_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/my?"))
        driver.refresh()

        show_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/cgi/showgeneset')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", show_link)

        show_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cgi/showgeneset')]")))
        show_link.click()

        view_network_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='View as Interaction Network']")))
        view_network_button.click()

        continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'proceed_form') and contains(@class,'button')]")))
        continue_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/network?"))

        settings_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bottom_page_selector_settings")))
        settings_button.click()

        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='evidence']")))
        checkbox.click()

        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='hide_singletons']")))
        checkbox.click()

        update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button error_info_button']")))
        update_button.click()

        export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='bottom_page_selector_table']")))
        export_button.click()

        download_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=tsv_short']")))
        download_link = driver.find_element(By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=tsv_short']")
        download_link.click()
        time.sleep(2)

        download_link1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=highres_image']")))
        download_link1 = driver.find_element(By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=highres_image']")
        download_link1.click()
        time.sleep(5)

        for _ in range(5):
            try:
                send_to_cytoscape_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='cs_linkout' and text()='Send network to Cytoscape']"))
                )
                send_to_cytoscape_link.click()
        
                network_sent_message = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, "//span[@class='cs_message' and text()='Network sent!']"))
                )
                break 
            except TimeoutException:
                print("Network sent message not shown. Trying again...")
        else:
            print("Failed to send network to Cytoscape.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        print("All the files have been Download Successfully from the STRING Server")
        print("Downloaded files : string_hires_image.png and string_interactions_short.tsv ")
        driver.quit()
    
    time.sleep(5)

    pyautogui.click(381, 670); time.sleep(1)
    pyautogui.click(487, 357); time.sleep(5)
    pyautogui.click(467, 437); time.sleep(1)
    pyautogui.click(452, 780); time.sleep(1)
    pyautogui.click(578, 847); time.sleep(5)

    pyautogui.click(542, 163); time.sleep(1)
    pyautogui.click(675, 767); time.sleep(2)
    pyautogui.click(380, 364); time.sleep(1)
    pyautogui.click(472, 622); time.sleep(1)
    pyautogui.click(732, 662); time.sleep(1)
    pyautogui.click(732, 662); time.sleep(1)
    pyautogui.typewrite("display name"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(472, 622); time.sleep(1)
    pyautogui.click(429, 747); time.sleep(1)
    pyautogui.click(646, 409); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)

    pyautogui.click(1108, 848); time.sleep(1)
    pyautogui.click(1184, 917); time.sleep(2)
    pyautogui.click(1279, 392); time.sleep(4)
    pyautogui.click(861, 741); time.sleep(1)
    pyautogui.typewrite("UpReg"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(1440, 613); time.sleep(4)
    pyautogui.click(915, 741); time.sleep(1)
    pyautogui.typewrite("UpRegulatedOP"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(957, 575); time.sleep(1)
    pyautogui.click(1558, 132); time.sleep(1)
    pyautogui.click(956, 576); time.sleep(1)

##########################################################################################

def navigate_to_neg_data(file_path, cyto_path):

    cytoscape_executable_path = cyto_path
    subprocess.Popen([cytoscape_executable_path])

    cytoscape_window = None
    timeout = 60
    start_time = time.time()
    while time.time() - start_time < timeout:
        cytoscape_window = gw.getWindowsWithTitle('Session: New Session')
        if cytoscape_window:
            break
        time.sleep(1)

    if cytoscape_window:
        cytoscape_window = cytoscape_window[0]
        width = 1280
        height = 850
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        cytoscape_window.resizeTo(width, height)
        cytoscape_window.moveTo((screen_width - width) // 2, (screen_height - height) // 2)
    else:
        print("Cytoscape window not found within the timeout period.")

    try:
        driver = webdriver.Chrome()

        time.sleep(1)
        chrome_window = gw.getWindowsWithTitle('chrome')[0]
        chrome_window.activate()

        driver.get("https://string-db.org/")

        js_code = """
        var div = document.createElement('div');
        div.style.cssText = 'position: absolute; top: 50px; left: 10%; right: 10%; width: auto; height: auto; padding: 40px; font-size: 20px; font-weight: bold; text-align: center; z-index: 9999; color: black; overflow-y: auto; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); border-radius: 20px; font-family: Georgia, serif';
        div.innerHTML = "<p>ATTENTION USER:<br>This website will be automatically redirected to the Login page.</p>";
        div.innerHTML += "<p> Select Log-In: To Login in to your account and continue the remaining progress.</p>";
        div.innerHTML += "<p>Redirecting in 20Secs</p>";
        document.body.appendChild(div);

        var angle = 90; // Set the angle to 90 degrees for left to right gradient
        div.style.background = 'linear-gradient(' + angle + 'deg, #E4EfE9, #E4EfE9)';
        """
        driver.execute_script(js_code)

        time.sleep(20)

        my_data_link = driver.find_element(By.CSS_SELECTOR, "a.main_nav_tag[href*='/cgi/my?sessionId=']")
        my_data_link.click()

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button full_width']")))
        login_button.click()

        WebDriverWait(driver, 600).until(EC.url_contains("/cgi/my?"))
        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/my?"))

        gene_sets_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='my_page_selector MP_collapsed']")))
        gene_sets_element.click()

        anchor_tag = driver.find_element(By.XPATH, "//a[contains(@href, '/cgi/uploadnewgeneset?sessionId=')]")
        anchor_tag.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/uploadnewgeneset?"))

        gene_set_description_input = driver.find_element(By.ID, "geneset_description")
        gene_set_description_input.clear()
        gene_set_description_input.send_keys("DownRegulated")

        organism_search_input = driver.find_element(By.ID, "species_text_user_genelist")
        organism_search_input.clear()
        organism_search_input.send_keys("Homo sapiens")
        organism_search_input.click()

        text_area = driver.find_element(By.ID, "loginuser_geneset_items_uploaded")
        text_area.clear()
        text_area = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginuser_geneset_items_uploaded")))
        text_area.send_keys(file_path)

        checkbox = driver.find_element(By.ID, "loginuser_geneset_enable_statistics")
        driver.execute_script("arguments[0].click();", checkbox)

        continue_button = driver.find_element(By.XPATH, "//input[@value='Continue ->']")
        continue_button.click()

        continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue ->']")))
        continue_button.click()

        ok_button = driver.find_element(By.XPATH, "//input[@value='OK']")
        ok_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/my?"))
        driver.refresh()

        show_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/cgi/showgeneset')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", show_link)

        show_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cgi/showgeneset')]")))
        show_link.click()

        view_network_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='View as Interaction Network']")))
        view_network_button.click()

        continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'proceed_form') and contains(@class,'button')]")))
        continue_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/cgi/network?"))

        settings_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bottom_page_selector_settings")))
        settings_button.click()

        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='evidence']")))
        checkbox.click()

        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='hide_singletons']")))
        checkbox.click()

        update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button error_info_button']")))
        update_button.click()

        export_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='bottom_page_selector_table']")))
        export_button.click()

        download_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=tsv_short']")))
        download_link = driver.find_element(By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=tsv_short']")
        download_link.click()
        time.sleep(2)

        download_link1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=highres_image']")))
        download_link1 = driver.find_element(By.CSS_SELECTOR, "a.updateNonce[href*='downloadDataFormat=highres_image']")
        download_link1.click()
        time.sleep(5)

        for _ in range(5):
            try:
                send_to_cytoscape_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='cs_linkout' and text()='Send network to Cytoscape']"))
                )
                send_to_cytoscape_link.click()
        
                network_sent_message = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, "//span[@class='cs_message' and text()='Network sent!']"))
                )
                break 
            except TimeoutException:
                print("Network sent message not shown. Trying again...")

        else:
            print("Failed to send network to Cytoscape.")
    except Exception as e:
        print("An error occurred:", e)

    finally:
        print("All the files have been Download Successfully from the STRING Server")
        print("Downloaded files : string_hires_image (1).png and string_interactions_short (1).tsv ")
        driver.quit()

    time.sleep(5)

    pyautogui.click(381, 670); time.sleep(1)
    pyautogui.click(487, 357); time.sleep(5)
    pyautogui.click(467, 437); time.sleep(1)
    pyautogui.click(452, 780); time.sleep(1)
    pyautogui.click(578, 847); time.sleep(5)

    pyautogui.click(542, 163); time.sleep(1)
    pyautogui.click(675, 767); time.sleep(2)
    pyautogui.click(380, 364); time.sleep(1)
    pyautogui.click(472, 622); time.sleep(1)
    pyautogui.click(732, 662); time.sleep(1)
    pyautogui.click(732, 662); time.sleep(1)
    pyautogui.typewrite("display name"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(472, 622); time.sleep(1)
    pyautogui.click(429, 747); time.sleep(1)
    pyautogui.click(646, 409); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)

    pyautogui.click(1108, 848); time.sleep(1)
    pyautogui.click(1184, 917); time.sleep(2)
    pyautogui.click(1279, 392); time.sleep(4)
    pyautogui.click(861, 741); time.sleep(1)
    pyautogui.typewrite("DownReg"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(1440, 613); time.sleep(4)
    pyautogui.click(915, 741); time.sleep(1)
    pyautogui.typewrite("DownRegulatedOP"); time.sleep(1)
    pyautogui.press("enter"); time.sleep(1)
    pyautogui.click(957, 575); time.sleep(1)
    pyautogui.click(1558, 132); time.sleep(1)
    pyautogui.click(956, 576); time.sleep(1)

##########################################################################################
    
def get_file_path(prompt, file_type):
    while True:
        file_path = input(prompt)
        if file_path.lower().endswith(file_type):
            return file_path
        else:
            print(f"Invalid file type. Please enter a path to a {file_type} file.")

def process_UpRegulated_files(csv_file_path, tsv_file_path):
    try:
        csv_df = pd.read_csv(csv_file_path, skiprows=1) 
        tsv_df = pd.read_csv(tsv_file_path, delimiter='\t')

        merged_df1 = pd.merge(csv_df, tsv_df, how='inner', left_on='Name', right_on='node2_string_id')
        merged_df1['node1'] = None  
        merged_df1['node2'] = merged_df1['node2'] 

        merged_df2 = pd.merge(csv_df, tsv_df, how='inner', left_on='Name', right_on='node1_string_id')
        merged_df2['node1'] = merged_df2['#node1']
        merged_df2['node2'] = None

        final_output = pd.concat([merged_df1[['Rank', 'Name', 'Score', 'node1', 'node2']], 
                                  merged_df2[['Rank', 'Name', 'Score', 'node1', 'node2']]])

        final_output = final_output.drop_duplicates(subset=['Name'])

        final_output.reset_index(drop=True, inplace=True)

        final_output = final_output[['Rank', 'Name', 'node1', 'node2', 'Score']]

        final_output = final_output.sort_values(by='Score', ascending=False)

        final_output_sorted = final_output.sort_values(by='Score', ascending=False)

        final_output_sorted['Genes'] = final_output_sorted['node1'].fillna('') + final_output_sorted['node2'].fillna('')

        print(final_output_sorted)

        folder_name = "UpRegulated Survival Analysis"
        os.makedirs(folder_name, exist_ok=True)

        driver = webdriver.Chrome()

        url = "http://gepia2.cancer-pku.cn/#survival"
        driver.get(url)

        last_processed_index_file = "last_processed_index.txt"
        last_processed_index = 0
        if os.path.exists(last_processed_index_file):
            with open(last_processed_index_file, "r") as f:
                last_processed_index = int(f.read())

        for index, row in final_output_sorted.iloc[last_processed_index:].iterrows():

            text_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "survival_signature")))
            text_element.clear()
            text_element.send_keys(row['Genes'])

            option_element = driver.find_element(By.XPATH, "//select[@id='survival_tcgat']/option[@value='LUAD']")
            option_element.click()

            add_button = driver.find_element(By.ID, "survival_tcgatadd")
            add_button.click()

            plot_button = driver.find_element(By.ID, "survival_plot")
            plot_button.click()
            time.sleep(4)

            wait = WebDriverWait(driver, 30)
            iframe = wait.until(EC.presence_of_element_located((By.ID, "iframe")))
            src_value = iframe.get_attribute("src")

            if src_value:
                parsed_url = urlparse(src_value)
                filename = os.path.basename(parsed_url.path)

                file_path = os.path.join(folder_name, filename)

                response = requests.get(src_value, timeout=60)

                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"File '{filename}' downloaded successfully.")
                else:
                    print(f"Failed to download the file '{filename}'. Status code:", response.status_code)
            else:
                print("No src value found for the iframe. Skipping download.")

            last_processed_index = index + 1

            with open(last_processed_index_file, "w") as f:
                f.write(str(last_processed_index))

            driver.refresh()

        driver.quit()

        if os.path.exists(last_processed_index_file):
            os.remove(last_processed_index_file)

    except FileNotFoundError:
        print("File not found. Please check the file paths and try again.")

##########################################################################################
        
def get_file_path(prompt, file_type):
    while True:
        file_path = input(prompt)
        if file_path.lower().endswith(file_type):
            return file_path
        else:
            print(f"Invalid file type. Please enter a path to a {file_type} file.")

def process_DownRegulated_files(csv_file_path, tsv_file_path):
    try:
        csv_df = pd.read_csv(csv_file_path, skiprows=1) 
        tsv_df = pd.read_csv(tsv_file_path, delimiter='\t')

        merged_df1 = pd.merge(csv_df, tsv_df, how='inner', left_on='Name', right_on='node2_string_id')
        merged_df1['node1'] = None  
        merged_df1['node2'] = merged_df1['node2'] 

        merged_df2 = pd.merge(csv_df, tsv_df, how='inner', left_on='Name', right_on='node1_string_id')
        merged_df2['node1'] = merged_df2['#node1']
        merged_df2['node2'] = None

        final_output = pd.concat([merged_df1[['Rank', 'Name', 'Score', 'node1', 'node2']], 
                                  merged_df2[['Rank', 'Name', 'Score', 'node1', 'node2']]])

        final_output = final_output.drop_duplicates(subset=['Name'])

        final_output.reset_index(drop=True, inplace=True)

        final_output = final_output[['Rank', 'Name', 'node1', 'node2', 'Score']]

        final_output = final_output.sort_values(by='Score', ascending=False)

        final_output_sorted = final_output.sort_values(by='Score', ascending=False)

        final_output_sorted['Genes'] = final_output_sorted['node1'].fillna('') + final_output_sorted['node2'].fillna('')

        print(final_output_sorted)

        folder_name = "DownRegulated Survival Analysis"
        os.makedirs(folder_name, exist_ok=True)

        driver = webdriver.Chrome()

        url = "http://gepia2.cancer-pku.cn/#survival"
        driver.get(url)

        last_processed_index_file = "last_processed_index.txt"
        last_processed_index = 0
        if os.path.exists(last_processed_index_file):
            with open(last_processed_index_file, "r") as f:
                last_processed_index = int(f.read())

        for index, row in final_output_sorted.iloc[last_processed_index:].iterrows():

            text_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "survival_signature")))
            text_element.clear()
            text_element.send_keys(row['Genes'])

            option_element = driver.find_element(By.XPATH, "//select[@id='survival_tcgat']/option[@value='LUAD']")
            option_element.click()

            add_button = driver.find_element(By.ID, "survival_tcgatadd")
            add_button.click()

            plot_button = driver.find_element(By.ID, "survival_plot")
            plot_button.click()
            time.sleep(4)

            wait = WebDriverWait(driver, 30)
            iframe = wait.until(EC.presence_of_element_located((By.ID, "iframe")))
            src_value = iframe.get_attribute("src")

            if src_value:
                parsed_url = urlparse(src_value)
                filename = os.path.basename(parsed_url.path)

                file_path = os.path.join(folder_name, filename)

                response = requests.get(src_value, timeout=60)

                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"File '{filename}' downloaded successfully.")
                else:
                    print(f"Failed to download the file '{filename}'. Status code:", response.status_code)
            else:
                print("No src value found for the iframe. Skipping download.")

            last_processed_index = index + 1

            with open(last_processed_index_file, "w") as f:
                f.write(str(last_processed_index))

            driver.refresh()

        driver.quit()

        if os.path.exists(last_processed_index_file):
            os.remove(last_processed_index_file)

    except FileNotFoundError:
        print("File not found. Please check the file paths and try again.")

##########################################################################################

def main():
    file_path = input("Enter your Raw GEO database TSV file: ")
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
    try:
        tsv_data = read_tsv_file(file_path)
        print("File imported successfully")
        
        df = pd.read_csv(file_path, sep='\t')
        
        df_positive = df[df['log2FoldChange'] >= 0]
        df_positive = df_positive.sort_values(by='log2FoldChange')
        df_positive = df_positive[['Symbol']]
        df_str_positive = df_positive.to_string(index=False, header=False)

        sampled_df_str_positive = '\n'.join(df_str_positive.split('\n')[:500])

        #######################################################################

        df_negative = df[df['log2FoldChange'] < 0]
        df_negative = df_negative.sort_values(by='log2FoldChange')
        df_negative = df_negative[['Symbol']]
        df_str_negative = df_negative.to_string(index=False, header=False)

        sampled_df_str_negative = '\n'.join(df_str_negative.split('\n')[:500])
        
    except FileNotFoundError:
        print("File not found. Please enter a valid file path.")
    
    print("-----")

    user_input = input("Enter your cytoscape executable path: ")
    if user_input.startswith('"') and user_input.endswith('"'):
        user_input = user_input[1:-1]
    cyto_path = user_input
    print("Processed cytoscape path:", cyto_path)

    process_pos_gene_list_with_david(sampled_df_str_positive)

    while True:
        if "chromedriver" not in (p.name() for p in psutil.process_iter()):
            break
        time.sleep(10)

    process_neg_gene_list_with_david(sampled_df_str_negative)

    time.sleep(5)

    def is_cytoscape_running():
        for process in psutil.process_iter():
            if process.name() == "Cytoscape.exe":
                return True
        return False

    navigate_to_pos_data(sampled_df_str_positive, cyto_path)

    while is_cytoscape_running():
        time.sleep(10) 

    navigate_to_neg_data(sampled_df_str_negative, cyto_path)

    print("-----")
    print("-----")
    print("To generate the gene's name using the node_string_id, drop the necessary files into the prompt that appears.")
    print("-----")
    print("To Process the UpRegulated Files")
    print("----------")

    csv_file_path_1 = input("Enter the path of the UpRegulatedOP.csv file from Cytoscape: ")
    if csv_file_path_1.startswith('"') and csv_file_path_1.endswith('"'):
        csv_file_path_1 = csv_file_path_1[1:-1]

    tsv_file_path_1 = input("Enter the path of the string_interactions_short.tsv from String Server: ")
    if tsv_file_path_1.startswith('"') and tsv_file_path_1.endswith('"'):
        tsv_file_path_1 = tsv_file_path_1[1:-1]

    process_UpRegulated_files(csv_file_path_1, tsv_file_path_1)

    print("-----")
    print("-----")
    print("To Process the DownRegulated Files")
    print("----------")

    csv_file_path_2 = input("Enter the path of the DownRegulatedOP.csv file from Cytoscape: ")
    if csv_file_path_2.startswith('"') and csv_file_path_2.endswith('"'):
        csv_file_path_2 = csv_file_path_2[1:-1]

    tsv_file_path_2 = input("Enter the path of the string_interactions_short (1).tsv from String Server: ")
    if tsv_file_path_2.startswith('"') and tsv_file_path_2.endswith('"'):
        tsv_file_path_2 = tsv_file_path_2[1:-1]

    process_DownRegulated_files(csv_file_path_2, tsv_file_path_2)

if __name__ == "__main__":
    main()

