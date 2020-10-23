import re

from bs4 import BeautifulSoup

from .client import Client
from .config import Config
from .function import Func


class Mail:
    address: str = None
    client: Client = None

    def __init__(self, address: str, client: Client) -> None:
        self.address = address
        self.client = client

    def __str__(self) -> str:
        return f"Mail(address={self.address})"

    def get_mail_list(self) -> list:
        params = self._create_payload()
        res = self.client.get_request(
            Config.HOST + Config.PATH_MAIL_LIST, params=params
        )
        soup = BeautifulSoup(res.text, "html.parser")

        mail_data = []
        for script in soup.find_all("script"):
            if "openMailData" in str(script):
                result = re.search(
                    r"openMailData\(\'(.*)\', \'(.*)\', \'(.*)\'\)*", str(script)
                )
                content = {
                    "id": result.group(1),
                    "key": result.group(2),
                    "tag": result.group(3),
                }
                content["title"] = soup.find(
                    id="area_mail_title_{id}".format(id=content["id"])
                ).text.strip()
                mail_data.append(Message(self.client, **content))
        return mail_data

    def _create_payload(self) -> dict:
        return {
            "nopost": 1,
            "q": self.address,
            "_": Func.get_epoctime_int(),
        }


class Message:
    id: str = None
    key: str = None
    tag: str = None
    title: str = None

    def __init__(
        self, client: Client, id: str, key: str, tag: str, title: str = None
    ) -> None:
        self.client = client
        self.id = id
        self.key = key
        self.tag = tag
        self.title = title

    def __str__(self) -> str:
        return f"Message(id={self.id}, title={self.title})"

    def get_title(self) -> str:
        params = self._create_payload()
        res = self.client.get_request(
            Config.HOST + Config.PATH_MAIL_LIST, params=params
        )
        soup = BeautifulSoup(res.text, "html.parser")

        mail_data = []
        for script in soup.find_all("script"):
            if "openMailData" in str(script):
                result = re.search(
                    r"openMailData\(\'(.*)\', \'(.*)\', \'(.*)\'\)*", str(script)
                )
                content = {
                    "id": result.group(1),
                    "key": result.group(2),
                    "tag": result.group(3),
                }
                mail_data.append(Message(self.client, **content))
        return mail_data

    def _create_payload(self) -> dict:
        return {
            "noscroll": 1,
            "UID_enc": self.client.get_session_id(),
            "num": self.id,
            "key": self.key,
            "pagewidth": 885,
            "t": Func.get_epoctime_int(),
        }
