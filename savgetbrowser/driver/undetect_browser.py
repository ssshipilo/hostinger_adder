import os
import time
import uuid
import undetected_chromedriver as uc
from selenium_stealth import stealth
from fake_useragent import UserAgent

class UndetectBrowser():

    def __init__(self, proxy=None, headless=False, capsolver=False):
        self.headless = headless
        self.proxy = None
        self.capsolver = capsolver
        self.proxy_type_http = None
        if proxy:
            self.proxy_type_http = proxy
            username, passandhost, port = str(proxy).split(":")
            password, host = passandhost.split("@")
            self.proxy = {"user": username, "pass": password, "host": host, "port": port}
        self.driver = None

    def init_driver(self, default_directory=os.path.join(os.getcwd(), "downloads")):
        driver = None
        while True:
            try:
                if not os.path.exists(default_directory):
                    os.makedirs(default_directory)
                    
                options = uc.ChromeOptions()
                prefs = {
                    "download.default_directory": default_directory
                }
                # options.add_experimental_option("prefs", prefs)

                ua = UserAgent()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-infobars")
                options.add_argument(f"--user-agent={str(ua.chrome)}")
                # options.add_argument("--disable-extensions")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--lang=en-us")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
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
                extensions = [
                    self.proxy_extention_path,  # Proxy extension
                    capsolver_extention_path    # Capsolver extension
                ]
                options.add_argument("--load-extension=" + ",".join(extensions))

                if self.headless:
                    driver = uc.Chrome(options=options, headless=True, use_subprocess=False)
                else:
                    driver = uc.Chrome(options=options, headless=False, use_subprocess=False)
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

if __name__ == "__main__":
    ho = UndetectBrowser(proxy="c28a4282e7:gijq5LJV@192.241.80.252:4444")
