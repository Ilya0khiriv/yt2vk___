import sys
import threading
import time

from download_from_yt import Youtube as dyt
from settings import Settings
from video_id import Video
from get_video_from_site import YT as yt
from adb_upload import Uploader
import psutil
import os
import copy





def p(*text):
    d = __file__.split("/")[-1]
    try:
        f = " ".join(text)
    except:
        f = str(text)
    print(f"[{d}] {f}")


class main:

    def force_stop_chrome(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check if the process name is 'chrome'
                if 'chrome' in proc.info['name'].lower():
                    pid = proc.info['pid']
                    # Kill the process
                    os.kill(pid, 9)  # 9 is the SIGKILL signal
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def putlink_intheend(self):
        links = f"{os.path.dirname(os.path.abspath(__file__))}/links.txt"
        with open(links, 'r') as file:
            lines = file.readlines()
            line1 = lines[0]
            lines.remove(line1)

        with open(links, 'w') as file:
            file.write("".join(lines + [line1]))

    def __init__(self):
        self.start_download_premature = False
        self.vk = None
        self.settings = Settings()
        self.links = self.settings.vk_yt
        self.stop_cycle = False
        self.v = False
        self.start_time = None

        self.do_next_error = 0

        try: self.force_stop_chrome()
        except: pass

        self.yt = yt()
        self.yt.start(self)

        self.translate = False
        self.cl = None

        self.video = Video()

        for i in self.links:


            self.translate = False

            try:
                if i[3] == "ru":
                    self.translate = True
            except:
                pass

            cust_limit = None
            try:
                if i[4]:
                    cust_limit = int(i[4])
            except:
                pass

            p(i[0], i[2])


            self.cycle(i[0], i[2], i[1], limit=cust_limit)
            if self.settings.move_list == 1: self.putlink_intheend()

        self.vk.power_button()

    def cycle(self, VK, YT, VKname, limit = None):
        if not limit:
            limit = self.settings.donwload_limit
        print("\n"); print("\n")
        self.vk = Uploader(group=VK, gname=VKname, machine=self)
        vk_init = threading.Thread(target=self.vk.init)
        vk_init.start()  # open needed comminity to donwload videos to


        # set up downloader
        self.clip = dyt(video=self.video, driver=self.yt.driver, machine=self)

        # set up db
        clip_list = self.yt.analyze_channel(YT)
        print(clip_list)
        self.cl = clip_list



        self.yt.check_with_yt = self.settings.check_wih_yt #skip db unpdate
        if self.settings.only_scan is True: return #do not download

        self.start_download_premature = True #makes it start the cycle

        clip = self.clip #easier to manage code

        loop = 0

        try: vk_init.join()
        except: pass

        try: self.v.join()
        except: pass

        while True:
            print("\n"); print("\n"); print("\n"); print("\n"); print("\n")
            if len(clip_list.to_download) < 1:
                try:
                    self.v.join()
                except:
                    pass
                break

            while self.start_download_premature is False:
                time.sleep(1)
                p("Waiting for VK to release lock")

            self.start_time = int(time.time())
            self.start_download_premature = False
            self.stop_cycle = False

            loop += 1
            if loop > limit:
                self.stop_cycle = True

            if self.stop_cycle is True:
                self.stop_cycle = False
                p("Waiting for VK to finish...")

                try: self.v.join()
                except: pass

                break

            # reset driver
            # self.driver = self.yt.restart()
            # self.clip.driver = self.driver


            p(f"Downloaded in total: {len(clip_list.list_done)-1}/{len(clip_list.list_all)-1}, {len(clip_list.list_all)-len(clip_list.list_done)-1} left")
            p(f"Current limit is:    {loop}/{limit}")
            p("Starting youtube downloader")



            clip.id = clip_list.to_download[-1]
            clip.download()

            if self.do_next_error == 1:
                self.do_next_error = 0
                break

            clip_list.done(clip=clip_list.to_download[-1])




            #if it looped once wait to finish
            try: p("Waiting for upload to finish"); self.v.join()
            except: pass

            print("------------", self.video.title)
            self.vk.title = self.video.title
            self.vk.file_name = f'{self.video.hashed}.mp4'
            file_path = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{self.vk.file_name}"

            if os.path.exists(file_path):
                print("File exists!")

                self.v = threading.Thread(target=self.vk.sequence)
                self.v.start()
            else:
                print("noooo file !!!!!!!")


m = main()
