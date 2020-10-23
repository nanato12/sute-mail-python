import time
import string
import random
from datetime import datetime

from bs4 import BeautifulSoup

from .config import Config


class Func:
    @staticmethod
    def log(text):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[{time}] {text}".format(time=now, text=text))

    @staticmethod
    def get_all_tag_texts(html: str, tag: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        return [element.text for element in soup.find_all(tag) if element.text != ""]

    @staticmethod
    def get_all_radio_button_values(html: str, name: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        return [
            element["value"]
            for element in soup.find_all("input", attrs={"name": name})
            if element["type"] == "radio"
        ]

    @staticmethod
    def get_csrf_token(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for meta in soup.find_all("meta", attrs={"name": Config.CSRF_TOKEN_TAG}):
            return meta.get("content")

    @staticmethod
    def get_epoctime_int():
        return int(time.time())

    @staticmethod
    def generate_random_string(count):
        return "".join([random.choice(string.ascii_letters) for _ in range(count)])
