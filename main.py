import os
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from fake_useragent import UserAgent
import chromedriver_autoinstaller

class SeleniumDriver():

    def __init__(self, proxy=False, headless=False, capsolver=False, default_directory=os.path.join(os.getcwd(), "downloads")):
        self.default_directory = default_directory
        self.headless = headless
        self.proxy = None
        self.proxy_extention_path = None
        self.capsolver = capsolver
        self.proxy_type_http = None
        if proxy:
            self.proxy_type_http = proxy
            username, passandhost, port = str(proxy).split(":")
            password, host = passandhost.split("@")
            self.proxy = {"user": username, "pass": password, "host": host, "port": port}

        self.driver = self.init_driver()

    def init_driver(self):
        driver = None
        while True:
            try:
                chromedriver_autoinstaller.install()
                
                options = Options()
                prefs = {}
                if self.default_directory:
                    if not os.path.exists(self.default_directory):
                        os.makedirs(self.default_directory)
                    prefs["download.default_directory"] = self.default_directory
                    
                options.add_experimental_option("prefs", prefs)
                ua = UserAgent()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-infobars")
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--lang=en-us")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--remote-debugging-port=9222")
                options.add_argument("--disable-webrtc")
                options.add_argument("--disable-ipv6")
                options.add_argument(f"--profile-directory=Profile 1")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

                # Proxy
                if self.proxy:
                    if 'user' in self.proxy.keys() and 'pass' in self.proxy.keys():
                        str_p = uuid.uuid4()
                        self.proxy_extention_path = os.path.join(os.getcwd(), 'savgetbrowser', 'core', 'proxy_extension', 'proxy', 'proxy_auth_extension')
                        current_dir = os.path.join(os.getcwd(), 'savgetbrowser', 'core', 'proxy_extension')
                        manifest_json_path = os.path.join(current_dir, 'manifest.json')
                        background_js_path = os.path.join(current_dir, 'background.js')
                        with open(manifest_json_path, 'r', encoding='utf-8') as f:
                            manifest_json = f.read()
                        with open(background_js_path, 'r', encoding='utf-8') as f:
                            background_js = f.read()
                        
                        def replace_variables_in_js(js_content: str, variables_dict: dict):
                            for variable, value in variables_dict.items():
                                js_content = js_content.replace('{{ ' + variable + ' }}', value)
                            return js_content
                        
                        variables_dict = {
                            'proxy_host': self.proxy['host'],
                            'proxy_port': self.proxy['port'],
                            'proxy_user': self.proxy['user'],
                            'proxy_pass': self.proxy['pass']
                        }
                        
                        background_js = replace_variables_in_js(background_js, variables_dict)
                        
                        if not os.path.exists(self.proxy_extention_path):
                            os.makedirs(self.proxy_extention_path)
                        
                        with open(os.path.join(self.proxy_extention_path, 'manifest.json'), 'w', encoding='utf-8') as f:
                            f.write(manifest_json)
                        
                        with open(os.path.join(self.proxy_extention_path, 'background.js'), 'w', encoding='utf-8') as f:
                            f.write(background_js)
                        
                        options.add_argument(f"--load-extension={self.proxy_extention_path}")
                    else:
                        options.add_argument(f'--proxy-server={self.proxy["host"]}:{self.proxy["port"]}')
                
                # Capsolver extension
                capsolver_extention_path = os.path.join(os.getcwd(), 'savgetbrowser', 'core', 'capsolver')
                
                # Load multiple extensions
                extensions = []
                if self.proxy_extention_path: # Proxy extension
                    extensions.append(self.proxy_extention_path)
                if capsolver_extention_path: # Capsolver extension
                    extensions.append(capsolver_extention_path)
                options.add_argument("--load-extension=" + ",".join(extensions))

                if self.headless:
                    options.add_argument("--headless")

                service = Service()
                driver = webdriver.Chrome(service=service, options=options)
                self.driver = driver
                stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                )

                return driver
            except Exception as e:
                print(f"Error initializing driver: {e}")
                try:
                    driver.close()
                except:
                    pass
                try:
                    driver.quit()
                except:
                    pass
                continue
    
    def start(self):
        self.driver.get("http://google.com")
        time.sleep(5)
        self.driver.get("https://www.hostinger.com/")

        # with open("./cookies.json", 'r') as f:
        #     cookies = json.loads(f.read())
        # for item in cookies:
        #     print(item)
        #     try:
        #         self.driver.add_cookie(item)
        #     except:
        #         continue
        # self.driver.get("https://hpanel.hostinger.com/")

        time_start = time.time()
        while True:
            df = time.time() - time_start
            if df > 30:
                break
            try:
                button_login = self.driver.find_element(By.ID, "hgr-topmenu-login")
                if button_login:
                    ActionChains(self.driver).move_to_element(button_login).click(button_login).perform()
            except:
                continue

        # melodymoodsofficial@gmail.com
        # 390a229915720d73e25f466b059bcc64

        print("кчть")
        while True:
            time.sleep(1)

if __name__ == "__main__":
    ho = SeleniumDriver()
    # ho = SeleniumDriver(proxy="c28a4282e7:gijq5LJV@23.236.223.39:4444")

        
    # import pandas as pd
    # import gspread
    # from gspread_dataframe import get_as_dataframe

    # link = "https://docs.google.com/spreadsheets/d/1pq28QXeT7FfXbPSTmM7dB5MzAFIVDcVhtLyP79453b8"
    # sheet_url = f'{link}/export?format=csv&gid=0#gid=0'
    # df = pd.read_csv(sheet_url)
    # print(df.head())


    ho.start()