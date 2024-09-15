import re
import sys
import time
from browser import Chrome
from yt_db import YTdb
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

def p(text):
    d = __file__.split("/")[-1]
    print(f"[{d}] {text}")

class YT:

    def __init__(self):
        self.ytdb = None
        self.chrome_cls = None
        self.machine = None
        self.driver = None

    def start(self, machine):
        self.chrome_cls = Chrome(h=machine.settings.headless)
        app = self.chrome_cls.get_frontmost_app_name()
        print(app)


        self.chrome_cls.start()
        self.chrome_cls.activate_app(app)
        self.driver = self.chrome_cls.driver
        self.machine = machine
        machine.driver = self.chrome_cls.driver



    def restart(self):
        app = self.chrome_cls.get_frontmost_app_name()
        print(app)
        
        try:
            self.driver.quit()
        except:
            p("Error quiting driver")
        self.chrome_cls.start()
        self.driver = self.chrome_cls.driver

        self.chrome_cls.activate_app(app)
        return self.chrome_cls.driver

    def analyze_channel(self, channel):
        if "https://" not in channel:
            channel = "https://" + channel


        channel_id = channel.split("/")[-2][1:]
        p(f"{channel} {channel_id}")

        self.ytdb = YTdb(channel_id)

        if self.machine.settings.check_wih_yt is True:
            self.driver.get(channel)

            def get_len():
                return len(self.driver.page_source)

            length = 0
            same = 0

            while True:
                try:
                    new_length = get_len()
                    # Scroll down using keys
                    body = self.driver.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.END)
                    time.sleep(self.machine.settings.timout_scan)

                    print(f"\r{new_length} {length} | Timeout in: {same}/10", end="")
                    sys.stdout.flush()

                    if new_length == length:
                        same += 1
                        if same > 10:
                            p("\n")
                            break
                        continue

                    same = 0
                    length = new_length
                except:
                    pass


            raw_data = self.driver.page_source


            clips = []

            page_source = self.driver.page_source

            pattern = r'/shorts/([a-zA-Z0-9_-]+)'

            # Find all matches
            matches = re.findall(pattern, page_source)

            # Print the matches
            for match in matches:
                if match not in clips:
                    clips.append(match)

            self.ytdb.add(clips)
        self.ytdb.done(init=True)
        self.ytdb.to_download

        return self.ytdb