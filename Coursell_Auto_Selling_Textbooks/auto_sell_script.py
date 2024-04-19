# import necessary libraries
import pandas as pd
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pickle


class Carousell:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options)
        # Please fill in your username/email and password
        self.username = ''
        self.password = ''
        # Please fill in the path to save the cookies
        self.save_cookies_path = ''

    def login(self):
        # Open the coursell login website
        self.driver.get('https://www.carousell.com.hk/login/')
        # Click the second button on the page
        login_button = self.driver.find_elements(
            By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[1]/button[2]')
        login_button[0].click()
        # Fill in the Email and Password
        email = self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[1]/form/div[1]/div/div/input")
        email.send_keys(self.username)
        password = self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[1]/form/div[2]/div/div/input")
        password.send_keys(self.password)
        submit = self.driver.find_elements(
            By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[1]/form/button')
        submit[0].click()

        # Save the cookies
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(self.save_cookies_path, "wb"))

    def sell(self, title, condition, price, description, frow, first_time):
        if frow:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a'))
            )
            sell_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a')
            sell_button.click()
        else:
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/header/div/div/div/div[3]/a'))
            )
            sell_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/header/div/div/div/div[3]/a')
            sell_button.click()

        # Manully upload the photo
        # If you figure out how to upload the photo automatically, please let me know
        # I would love to hear that
        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div'))
        )

        # Auto click the category button
        category = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div'
        )
        category.click()

        # Auto fill in the title
        category_input = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div/input'
        )
        category_input.send_keys('textbooks')

        textbooks_xpath = '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div/div[2]'
        # Locate the category_select element
        category_select = self.driver.find_element(
            By.XPATH, textbooks_xpath)

        # Click the category_select element
        category_select.click()

        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/div/div/div/input'))
        )

        title_input = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/div/div/div/input')
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
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[2]/div/div/input'))
            )

            location = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[2]/div/div/input')
            location.send_keys('Sha Tin Wai')

            # location_select = self.driver.find_element(
            #     By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/form/div[1]/div[6]/div[4]/div/div[3]/div/div[2]/div/p[1]')
            # location_select.click()

            WebDriverWait(self.driver, 100).until(
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
        time.sleep(20)


if __name__ == '__main__':
    # Set the path to the chromedriver
    os.environ['PATH'] += r'C:/SeleniumDrivers'

    # Create a new instance of the Chrome driver
    carousell = Carousell()

    # Open the coursell website
    carousell.driver.get('https://www.carousell.com.hk/')

    first_time = True

    # Check if the cookies file exists
    if os.path.exists(carousell.save_cookies_path):
        # Load the cookies
        cookies = pickle.load(open(carousell.save_cookies_path, "rb"))
        try:
            for cookie in cookies:
                carousell.driver.add_cookie(cookie)
            # Refresh the page
            carousell.driver.refresh()
            first_time = False
        except:
            # Login to the carousell
            carousell.login()
    else:
        # Login to the carousell
        carousell.login()

    # Load the excel file to get the item to sell
    # Please fill in the path to the excel file
    df = pd.read_excel(
        '')
    for index, row in df.iterrows():
        title = row['Listing Title']
        condition = row['Condition']
        price = row['Price']
        description = row['Description']
        print(f"{title}: {condition} ${price} {description}")
        frow = True if index == 0 else False

        # Sell the item
        carousell.sell(title, condition, price, description, frow, first_time)

    # Close the browser
    carousell.driver.quit()
