import os
import subprocess
import tempfile

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


from AppKit import NSWorkspace







def p(text):
    d = __file__.split("/")[-1]
    print(f"[{d}] {text}")


class Chrome:
    def activate_app(self, app_name):
        workspace = NSWorkspace.sharedWorkspace()
        apps = workspace.runningApplications()

        for app in apps:
            if app.localizedName() == app_name:
                app.activateWithOptions_(0)
                return True
        return False

    def get_frontmost_app_name(self):
        script = 'tell application "System Events" to get name of first application process whose frontmost is true'
        try:
            result = subprocess.check_output(['osascript', '-e', script]).strip()
            return result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return "Error retrieving app name"

    def __init__(self, h=False, dir=False):
        chrome_profile_path = "/Users/ilya/Library/Application Support/Google/Chrome/Default"
        self.driver = None
        self.chrome_options = Options()

        if h is True:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--window-size=1920x1080")
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage")

        if dir is False:
            self.chrome_options.add_argument(f'user-data-dir={chrome_profile_path}')
        else:
            user_data_dir = tempfile.mkdtemp()
            self.chrome_options.add_argument(f'user-data-dir={user_data_dir}')

        # Enable logging for performance and network

        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-logging")
        # Add user data dir and profile path
        self.chrome_options.add_argument(f'user-data-dir={chrome_profile_path}')
        self.chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Keeps Chrome in the background

        # Additional arguments
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection of automation
        self.chrome_options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess")  # Enable network service

        # Setup Chrome driver with network capabilities
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})



    def start(self):
        e = self.get_frontmost_app_name()
        self.driver = webdriver.Chrome(
            service=Service(f"{os.path.dirname(os.path.abspath(__file__))}/chromedriver"),
            options=self.chrome_options
        )
        self.activate_app(e)
        return self.driver




