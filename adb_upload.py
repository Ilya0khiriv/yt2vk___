import os
import re
import subprocess
import time
from datetime import datetime


def p(*text):
    d = __file__.split("/")[-1]
    f = " ".join(text)
    print(f"[{d}] {f}")



class Uploader:
    def __init__(self, group=None, gname=None, name=None, machine=None):
        list_audios = []
        if not "device" in self.run_command("adb devices")[0]:
            p("No device detected, stop script")
            exit()
        else:
            p("Android device connected")

        self.video = None
        self.gname = gname
        self.machine = machine
        self.group = group
        self.path = f'{os.path.dirname(os.path.abspath(__file__))}/platform-tools/adb'
        self.video_pc_path = f'{os.path.dirname(os.path.abspath(__file__))}/videos'
        self.file_name = name
        self.title = None
        self.clips = None

    def power_button(self):
        self.run_command("adb shell input keyevent 26")

    def extract_text_from_image(self):
        output_file = "d.txt"
        image_path = f"./screenshot.png"
        # Run the tesseract command
        command = f"tesseract {image_path} {output_file}"
        subprocess.run(command, shell=True)

        # Read the output text file
        with open(f"{output_file}.txt", 'r') as file:
            text = file.read()

        return text

    def take_screenshot(self):
        output_file = f"./screenshot.png"
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Take screenshot on the device
        screenshot_command = "adb shell screencap -p /sdcard/screenshot.png"
        subprocess.run(screenshot_command, shell=True)

        # Pull the screenshot from the device to the computer
        pull_command = f"adb pull /sdcard/screenshot.png {output_file}"
        subprocess.run(pull_command, shell=True)

        # Remove the screenshot from the device
        remove_command = "adb shell rm /sdcard/screenshot.png"
        subprocess.run(remove_command, shell=True)

    def run_command(self, cmd_, errors=False):
        process = subprocess.Popen(cmd_, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if errors == True:
            return stdout.decode('utf-8'), stderr.decode('utf-8')
        return stdout.decode('utf-8'), stderr.decode('utf-8')

    def dump_ui(self):
        result = self.run_command("adb shell uiautomator dump && adb shell cat /sdcard/window_dump.xml")
        return result

    def find_element(self, element=None, activity=None):
        if element in activity:
            print("found")
            print("======")
            s = element.split()

            for i in s:
                if "bounds" in str(i):
                    s = i
                    break
            print(s)
            s = s.split('"')
            s = s[1]
            print(s)
            s = s.split("][")
            print(s)
            s1, s2 = s
            s1, s2 = s1[1:].split(","), s2[:-1].split(",")
            print(s1, s2)
            left, top = map(int, s1)
            right, bottom = map(int, s2)

            # Calculate the center point
            center_x = int((left + right) / 2)
            center_y = int((top + bottom) / 2)
            return center_x, center_y

        return False

    def click(self, cords=None, long=False, swipe=False, time=1000):
        if swipe is True:
            x1, y1, x2, y2 = cords
            self.run_command(f"adb shell input touchscreen swipe {x1} {y1} {x2} {y2} {time}")
            return

        x, y = cords

        if long is True:
            self.run_command(f"adb shell input touchscreen swipe {x} {y} {x} {y} {time}")
            return

        self.run_command(f"adb shell input tap {x} {y}")

    def amount_of_clips(self, ui):
        print(ui)
        el = ui[0].split("<")
        print(el)

        g = ""
        for e in el:
            if "text=" in e and " clips" in e:
                print(e)
                g = e
                break

        pos1 = g.find("text=")
        print(g[pos1:])
        pos2 = g.find(' clips"')
        return int(g[pos1 + 6:pos2])

        pass

    def set_creation_date_to_now(self, file_path):
        now = datetime.now()
        now_str = now.strftime("%m/%d/%Y %H:%M:%S")
        command = f'SetFile -d "{now_str}" "{file_path}"'
        subprocess.run(command, shell=True)

    def set_modification_date(self, file_path):
        today = datetime.now()
        mod_time = today.timestamp()
        os.utime(file_path, (mod_time, mod_time))

    def uploading_progress(self):
        keywords = ["processing clip", "clip uploading"]

        self.click(swipe=True, cords=[10, 10, 10, 800], time=100)

        self.take_screenshot()
        f = self.extract_text_from_image()
        f = f.splitlines()

        for keyword in keywords:
            for i in f:
                if keyword in i.lower():
                    print(f"=={i}==")
                    return False
        return True

    def when_on_screen(func):
        def wrapper(self, *args, **kwargs):
            p(f"Looking for string '{kwargs['string']}'")
            tries = 0
            while True:
                tries += 1
                text = self.run_command(
                    "adb shell uiautomator dump /sdcard/ui_dump.xml && adb shell cat /sdcard/ui_dump.xml")

                if kwargs['string'] in text[0]:
                    kwargs.update({"ui": text})
                    break

                if tries > 4:
                    self.run_command("adb shell input keyevent 4")
                    raise Exception(f"{kwargs['string']} not found")

            result = func(self, *args, **kwargs)
            p("Clicked")
            return result

        return wrapper

    @when_on_screen
    def click_on_desc(self, string, ui=None):
        if ui:
            text = ui

        else:

            text = self.run_command(
                "adb shell uiautomator dump /sdcard/ui_dump.xml && adb shell cat /sdcard/ui_dump.xml")

        text = text[0].splitlines()[1]
        search_content_desc = string

        bounds_pattern = re.compile(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"')
        text = text.split("><")

        def extract_bounds(string):
            match = bounds_pattern.search(string)
            if match:
                x1, y1, x2, y2 = map(int, match.groups())
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                self.run_command(f"adb shell input tap {center_x} {center_y}")

        cont = []
        for i in text:

            if search_content_desc in i:
                cont.append(i)

        extract_bounds(cont[-1])

    def init(self):

        self.run_command("adb shell am force-stop com.vk.clips")

        # self.run_command("adb shell am force-stop com.vk.clips")

        self.run_command(
            f"adb shell am start -n com.vk.clips/.links.ClipsLinkRedirActivity -a android.intent.action.VIEW -d {self.group}")
        p(f"Opening on ADB {self.gname}")
        while True:
            ui = self.run_command("adb shell uiautomator dump /sdcard/ui_dump.xml && adb shell cat /sdcard/ui_dump.xml")
            if self.gname in ui[0]:
                break

    def sequence(self):
        tries = 0
        while True:

            try:
                self.wrapped_sequence()
                return
            except:
                tries += 1
                p(f"Wrapped sequence failed - [{tries}]")
                self.init()

    def wrapped_sequence(self):
        self.machine.start_download_premature = True

        p(f"Working on {self.file_name}")



        p("Set createtion date")
        self.set_creation_date_to_now(f"{self.video_pc_path}/{self.file_name}")
        self.set_modification_date(f"{self.video_pc_path}/{self.file_name}")

        p("Push file to android")
        print(self.run_command(f'adb push \"{self.video_pc_path}/{self.file_name}\" /sdcard/ytvk'))
        path_ytkvfile = f"sdcard/ytvk/{self.file_name}"
        self.run_command(
            f"adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{path_ytkvfile}")
        self.run_command(f"adb shell am start -n com.vk.clips/.ui.base.MainActivity")
        self.click_on_desc(string='index="2" text="" resource-id="" class="android.view.View')
        self.click_on_desc(string=self.file_name)
        self.click_on_desc(string="com.vk.clips:id/entry_points_photos_go")
        self.click_on_desc(string="com.vk.clips:id/timeline_accept")
        self.click_on_desc(string="Descriptions can now contain up")

        self.run_command(f'adb shell am startservice ca.zgrs.clipper/.ClipboardService')

        s = self.title

        self.run_command(f'adb shell \'am broadcast -a clipper.set -e text "{s}"\'')


        time.sleep(0.5)
        self.run_command(f'adb shell input keyevent 279')

        self.click_on_desc(string="com.vk.clips:id/ivEndIcon")
        self.click_on_desc(string="com.vk.clips:id/btn_send")



        not_found = 0

        def clean_up():
            p("removing ", self.file_name)
            self.run_command(f"adb shell rm /sdcard/ytvk/{self.file_name}")
            os.remove(f"{self.video_pc_path}/{self.file_name}")

        while True:
            prev = ""
            ui = self.run_command("adb shell uiautomator dump /sdcard/ui_dump.xml && adb shell cat /sdcard/ui_dump.xml")[0]

            if not_found > 3:
                clean_up()

                p("UPLOADED!!!! ")
                break

            text = str(ui)



            try:
                start_index = text.find('text="Uploading: ')
            except:
                p("String not found")
                clean_up()
                continue


            if start_index != -1:

                not_found = 0
                # Calculate the starting index of the next 4 symbols
                next_index = start_index + len("Uploading:")

                # Extract the next 4 symbols
                next_4_symbols = text[next_index + 7:next_index + 9]


                if text[next_index + 7:next_index + 10][-1] == "0":
                    p("Uploading:", f"100%")
                    continue
                if next_4_symbols != prev:
                    p("Uploading:", f"{next_4_symbols}%")
                prev = next_4_symbols

            else:
                not_found += 1
                p(f"return to vk clips before 3 now - {not_found-1}")


        epoch_time = int(time.time()) - self.machine.start_time

        minutes = epoch_time // 60
        seconds = epoch_time % 60
        p(f">>>>  Video was downloaded in {minutes}:{seconds}")
