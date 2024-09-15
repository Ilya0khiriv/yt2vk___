import json
import os


def p(text):
    d = __file__.split("/")[-1]
    print(f"[{d}] {text}")
class YTdb:
    def __init__(self, channel_id):
        self.filename = f"{os.path.dirname(os.path.abspath(__file__))}/yt.json"
        self.channel_id = channel_id
        self.db = {}
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump({}, file)  # Write an empty JSON object to the file

        with open(self.filename, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():  # Check if the file is not empty
                self.db[self.channel_id] = [
                    {"done": []},
                    {"all": []}
                ]
                p("Created new database")
            else:
                self.db = json.loads(content)
                if self.channel_id not in self.db:
                    self.db[self.channel_id] = [
                        {"done": []},
                        {"all": []}
                    ]
                p("Loaded existing database")

        self.list_done = self.db[self.channel_id][0]["done"]
        self.list_all = self.db[self.channel_id][1]["all"]
        self.to_download = []

    def save_changes(func):
        def wrapper(self, *args, **kwargs):

            self.db[self.channel_id][0]["done"] = self.list_done
            self.db[self.channel_id][1]["all"] = self.list_all

            result = func(self, *args, **kwargs)
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.db, file, ensure_ascii=False, indent=4)

            return result
        return wrapper

    @save_changes
    def add(self, clips):
        for clip in clips:
            if clip not in self.list_all:
                self.list_all.append(clip)

    @save_changes
    def done(self, clip=None, init = None):

        if not init:
            self.list_done.append(clip)

        self.to_download = [item for item in self.list_all if item not in self.list_done]



    @save_changes
    def clear_bd(self, key = None, whole=None):
        if key:
            p("he")
            self.db.pop(key, None)

        if whole:
            self.db = {}


