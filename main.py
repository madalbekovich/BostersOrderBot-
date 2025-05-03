import time
import json
import os
import re
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from fake_useragent import UserAgent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
os.makedirs("captcha_images", exist_ok=True)

class FakeUserAgent:
    @staticmethod
    def get():
        f_user = UserAgent().random
        return f_user

class BusinessNetBoosterOrderBot:
    def __init__(self):
        self.driver = None
        self.base_url = "http://business.netboosters.ru/"
        self.order_url = "http://business.netboosters.ru/sched.php"

    def __init_webdriver__(self):
        logging.info('[+] INFO:\nИнициализация драйвера...')

        user_agent = FakeUserAgent.get()
        options = ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        # options.add_argument('window-size=275,112')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = Chrome(options=options)

    def screenshot_of_code(self):
        if not self.driver:
            logging.info("Driver not initalizied")

        captcha_image = os.path.join('captcha_images', "captcha.png")
        print(captcha_image)
        self.driver.get_screenshot_as_file(captcha_image)
        return captcha_image

    def get_text_of_image(self, file: str) -> str == None:
        if not self.driver:
            logging.info("Driver not initalizied")
        reader = easyocr.Reader(['ch_sim', 'en'])
        result = reader.readtext(file)
        image_path = 'result_captcha.txt'
        image_result = [text for text in result]
        text = image_result[5]
        print(text)
        pattern = r"'([^']+)'"
        match = re.search(pattern, str(text))

        if match:
            extracted_text = match.group(1)
            print(extracted_text)
        pass

    def login(self):
        url = self.base_url
        self.__init_webdriver__()
        try:
            if self.driver:
                self.driver.get(url)
                time.sleep(3)
                image_path = self.screenshot_of_code()
                self.get_text_of_image(image_path)
        except Exception as _ex:
            logging.info("[+] INFO: Driver not initalizied")
            logging.info(f"Damn has some error:\n {_ex}")
        # finally:
        #     driver.close()

    def login_with_cookie(self, cookie_file):
        self.__init_webdriver__()
        if not self.driver:
            logging.info("Driver not initalizied")
        if not cookie_file:
            logging.info("File for read Cookie not found")

        self.driver.get(self.base_url)

        with open(cookie_file, 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.get(self.base_url)

    def pick_up_order(self): # passing request_interval
        user_agent = FakeUserAgent.get()
        # logging.info(user_agent)
        while True:
            self.driver.get(self.order_url)
            # time.sleep(random.randrange(3, request_interval))
            self.driver.execute_script(
                f"Object.defineProperty(navigator, 'userAgent', {{get: function () {{ return '{user_agent}'; }}}});"
            )
            try:
                # order_button = self.driver.find_elements("xpath", "//a[contains(text(), 'Забрать заказ')]")

                wait = WebDriverWait(self.driver, 5)
                order_button = wait.until(
                    element_to_be_clickable(("xpath", "//a[contains(text(), 'Забрать заказ')]"))
                )
                order_button.click()
                logging.info("Found Order")
            except Exception as _ex:
                logging.info("No orders yet...")

if __name__ == "__main__":
    action = BusinessNetBoosterOrderBot()
    action.login_with_cookie('cookie.json')
    time.sleep(5)
    action.pick_up_order() # request_interval 5s default