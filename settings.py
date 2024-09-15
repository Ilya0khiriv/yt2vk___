import json
import os


class Settings:

    def __init__(self):
        self.vk_yt = []

        self.check_wih_yt = True
        self.only_scan = False
        self.verbose = True
        self.donwload_limit = 6
        self.headless = False
        self.timout_scan = 0.1
        self.move_list = 1

        if self.only_scan is True:
            self.check_wih_yt = True

        links = f"{os.path.dirname(os.path.abspath(__file__))}/links.txt"
        with open(links, 'r', encoding='utf-8') as file:
            content = file.read()

            for i in content.splitlines():
                try:
                    if "#" in i[0]: continue
                    if len(i) < 3: continue
                    self.vk_yt.append(i.split(" -> "))
                except:
                    pass

