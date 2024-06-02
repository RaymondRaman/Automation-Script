"""
Author: Raymond Li
Date: 2024-06-01
Description: This script is used to automatically sell textbooks on Carousell.
To use this script, you need to fill in the required information in the initialization of the Carousell class.
1. The path to save the cookies (Please use EditThisCookie extension to export the cookies and save them in a text file)
2. The path to the Excel file containing the details of the textbooks to sell

Also, please fill in the photo_directory in the main function

Remark:
Please make sure the photo folder name is the same with title in excel.
"""

# import necessary libraries
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import glob
import json
import sys


class Carousell:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)

        self.xpaths = {
            'upload_photo_button': '/html/body/div[1]/div/main/div/div/div[2]/div[1]/div/div/label/input',
            'category': '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div',
            'category_input': '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div/input',
            'textbooks_xpath': '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div[2]',
            'category_select': '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div[2]/div[2]',
            'title_input': '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/div/div/div/input'
        }

        # Please fill the following information
        self.category = 'textbooks'
        self.paths = {
            'save_cookies_path': '',
            'excel_path': ''
        }

    def sell(self, title, condition, price, description, frow, file_paths):
        wait = WebDriverWait(self.driver, 200)
        carousell.driver.get('https://www.carousell.com.hk/sell')

        upload_photo_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, self.xpaths['upload_photo_button'])))

        try:
            upload_photo_button.send_keys('\n'.join(file_paths))
        except:
            print("Please make sure the folder name is the same in excel.")
            sys.exit()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['category']))
        )
        print(f"""******* Photos have been successfully uploaded *******\n""")

        # Auto click the category button
        category = self.driver.find_element(
            By.XPATH,
            self.xpaths['category']
        )
        category.click()

        # Auto fill in the title
        category_input = self.driver.find_element(
            By.XPATH,
            self.xpaths['category_input']
        )
        category_input.send_keys(self.category)

        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, self.xpaths['category_select']))
            )

            # Locate the category_select element
            category_select = self.driver.find_element(
                By.XPATH, self.xpaths['category_select'])

            # Click the category_select element
            category_select.click()
        except:
            category_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpaths['category_select'])))
            self.driver.execute_script(
                "arguments[0].click();", category_select)

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.xpaths['title_input']))
        )

        title_input = self.driver.find_element(
            By.XPATH, self.xpaths['title_input'])
        title_input.send_keys(title)

        try:
            if condition == 'Brand new':
                brand_new = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[2]/div/div[2]/div[1]/button[1]')
                brand_new.click()
            elif condition == 'Like new':
                like_new = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[2]/div/div[2]/div[1]/button[2]')
                like_new.click()
        except:
            if condition == 'Brand new':
                brand_new = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[2]/div/div[2]/div[1]/button[1]/span')
                brand_new.click()
            elif condition == 'Like new':
                like_new = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[2]/div/div[2]/div[1]/button[2]/span')
                like_new.click()

        price_input = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[4]/div[1]/div/div/input')
        price_input.send_keys(price)

        description_input = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[5]/div/div/div[1]/textarea')
        description_input.send_keys(description)

        level = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[4]/div[6]/div/div[2]/div/button[2]')
        level.click()

        try:
            meet_up = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[3]/label/div')
            meet_up.click()
        except:
            meet_up = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[3]/label')

        if frow:
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[2]/div/div/input'))
            )

            location = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[2]/div/div/input')
            location.send_keys('Sha Tin Wai')

            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[3]/div/div[2]/div/p[2]'))
            )
            location_select = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[3]/div/div[2]/div/p[2]')
            location_select.click()

            add_note_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[1]/div/div[2]/button')
            add_note_button.click()

            try:
                mail = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[5]/label')
                mail.click()
            except:
                mail = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[5]/label/div/p')
                mail.click()

        submit = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[2]/button')
        submit.click()

        # wait for the post to be uploaded
        time.sleep(40)
        print(f"""******* Item has been successfully uploaded *******\n""")


if __name__ == '__main__':
    # Set the path to the chromedriver
    os.environ['PATH'] += r'C:/SeleniumDrivers'

    # Create a new instance of the Chrome driver
    carousell = Carousell()

    # Open the coursell website
    carousell.driver.get('https://www.carousell.com.hk/')

    # Load cookies from a file
    with open(carousell.paths['save_cookies_path'], 'r') as f:
        cookies = json.load(f)

    # Add each cookie to the browser
    for cookie in cookies:
        if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = "None"
        carousell.driver.add_cookie(cookie)

    # Refresh the page to apply the cookies
    carousell.driver.refresh()

    # Load the excel file to get the item to sell
    # Please fill in the path to the excel file
    df = pd.read_excel(carousell.paths['excel_path'])

    for index, row in df.iterrows():
        title = row['Listing Title']
        condition = row['Condition']
        price = row['Price']
        description = row['Description']
        frow = True if index == 0 else False

        # Generate photo_directory and file_paths for each textbook
        photo_directory = (
            f''
            f'{title}'
        )

        file_paths = glob.glob(os.path.join(
            photo_directory, '**', '*.jpg'), recursive=True)

        # Sell the item
        print(f"""******* Selling the item *******\nTitle: {title}\nCondition: {
              condition}\nPrice: {price}\nDescription: {description}\n""")

        carousell.sell(title, condition, price, description, frow, file_paths)

    # Close the browser
    carousell.driver.quit()
