from collections import deque
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
import time


class Kling:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--incognito')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
        options.add_argument("--use_subprocess")
        self.driver = webdriver.Chrome(options=options)

        self.xpaths = {
            'login_button': '/html/body/div[1]/div[2]/header/div[1]/div/button',
            'user_name_field': '/html/body/div[1]/div[3]/div/div/div/div/div[2]/div[1]/div/div/input',
            'password_field': '/html/body/div[1]/div[3]/div/div/div/div/div[2]/div[2]/div/div/input',
            'sign_in_button': '/html/body/div[1]/div[3]/div/div/div/div/div[2]/div[3]/button',
            'sider_button': 'slider-btn',
            'side_button_2': 'slider-shadow',
            'video_button': '/html/body/div[1]/div[1]/div/main/div[3]/div/div[2]/svg',
            'generate_button': '/html/body/div[1]/div[1]/div/main/div[1]/div[5]/div[2]/div[1]/div/button'
        }

    def solve_puzzle(self):
        print("Solving puzzle")
        iframe = self.driver.find_element(
            By.CSS_SELECTOR, 'iframe[src*="https://captcha.uvfuns.com/iframe/index.html"]')
        self.driver.switch_to.frame(iframe)
        while True:
            try:
                # Locate the slider button inside the iframe
                slider_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'slider-btn'))
                )

                # Perform the action within the iframe until the button disappears
                actions = ActionChains(self.driver)
                actions.click_and_hold(slider_button).move_by_offset(
                    220, 0).release().perform()

            except TimeoutException:
                print("Successfully logged in!!!")
                break
            except WebDriverException:
                print("Successfully logged in!!!")
                break
        self.driver.switch_to.default_content()

    def close_pop_up(self):
        time.sleep(1)
        try:
            pop_up_close = self.driver.find_element(
                By.XPATH, "//button[.//div/div[text()='I Got It']]"
            )
            pop_up_close.click()
            return True
        except:
            return True

    def login(self, username, password):
        print("Waiting for login")
        kling.driver.get('https://klingai.com/')
        kling.close_pop_up()

        while True:
            try:
                WebDriverWait(kling.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, kling.xpaths['login_button']
                                                    )))
                login_button = kling.driver.find_element(
                    By.XPATH, kling.xpaths['login_button'])
                login_button.click()
            except:
                break

        WebDriverWait(kling.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, kling.xpaths['user_name_field']
                                            )))
        user_name_field = kling.driver.find_element(
            By.XPATH, kling.xpaths['user_name_field'])
        user_name_field.send_keys(username)

        password_field = kling.driver.find_element(
            By.XPATH, kling.xpaths['password_field'])
        password_field.send_keys(password)

        sign_in_button = kling.driver.find_element(
            By.XPATH, kling.xpaths['sign_in_button'])
        sign_in_button.click()
        time.sleep(10)

        self.solve_puzzle()

    def generate_ai_video(self):
        print("Starting AI video generation")
        try:
            kling.driver.get('https://www.klingai.com/text-to-video/new')
            while True:
                res = self.close_pop_up()
                if res:
                    break

            video_item = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.video-works-box__item')
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", video_item)

            video_item.click()

            generate_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.xpaths['generate_button'])
                )
            )

            for _ in range(6):
                generate_button.click()
                time.sleep(10)

        except TimeoutException:
            print("AI Videos button or first video not found")
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")


if __name__ == '__main__':
    kling = Kling()
    queue = deque()
    with open('login.txt') as f:
        login = f.readlines()
        for line in login:
            username, password = line.split(' ', 1)
            password = password.strip()
            queue.append((username, password))

    while queue:
        username, password = queue.popleft()

        kling.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        kling.driver.delete_all_cookies()

        kling.login(username, password)
        kling.generate_ai_video()

    print("All tasks completed")
