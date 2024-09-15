import hashlib
import os


def p(text):
    d = __file__.split("/")[-1]
    print(f"[{d}] {text}")


class Video:

    def __init__(self):
        self.path = f"{os.path.dirname(os.path.abspath(__file__))}/videos"
        try:
            os.makedirs(self.path)
            p(f"Folder '{self.path}' created successfully.")

        except FileExistsError:
            p(f"Folder '{self.path}' already exists.")

        self.folder = None
        self.name = None
        self.title = None
        self.description = None
        self.error = None
        self.hashed = None

    def hash(self):
        self.hashed = hashlib.sha256(f"{self.title}".encode('utf-8')).hexdigest()

