import re
from typing import Optional

from bs4 import BeautifulSoup

from .client import Client
from .config import Config
from .function import Func


class Mail:
    address: str
    client: Client

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
            result = re.search(
                r"openMailData\(\'(.*)\', \'(.*)\', \'(.*)\'\)*", str(script)
            )
            if result:
                content = {
                    "id": result.group(1),
                    "key": result.group(2),
                    "tag": result.group(3),
                }
            else:
                continue

            content["title"] = soup.find(
                id="area_mail_title_{id}".format(id=content["id"])
            ).text.strip()
            mail_data.append(Message(self.client, **content))
        return mail_data

    def delete_mailbox(self) -> int:
        res = self.client.get_request(Config.HOST + Config.PATH_ADDRESS_LIST)
        soup = BeautifulSoup(res.text, "html.parser")
        mail_num = soup.find("span", string=self.address).get("id").split("addr_")[1]
        params = self._create_payload()
        params.update([("action", "delAddrList"), ("num_list", mail_num)])

        res = self.client.get_request(
            Config.HOST + Config.PATH_ADDRESS_LIST, params=params
        )
        return res.status_code

    def _create_payload(self) -> dict:
        return {
            "nopost": 1,
            "q": self.address,
            "_": Func.get_epoctime_int(),
        }


class Message:
    id: str
    key: str
    tag: str
    title: Optional[str]
    text: Optional[str]
    sender: Optional[str]

    def __init__(
        self,
        client: Client,
        id: str,
        key: str,
        tag: str,
        sender: str = None,
        title: str = None,
        text: str = None,
    ) -> None:
        self.client = client
        self.id = id
        self.key = key
        self.tag = tag
        self.title = title
        self.text = self._read_mail()
        self.sender = re.findall(r"from\=(.*)\;replyto", tag)[0].replace("%40", "@")

    def __str__(self) -> str:
        return f"Message(id={self.id}, title={self.title})"

    def _read_mail(self) -> str:
        params = self._create_payload()
        res = self.client.post_request(
            Config.HOST + Config.PATH_MAIL_CONTENT, data=params
        )
        return res.text

    def _create_payload(self) -> dict:
        return {
            "noscroll": 1,
            "UID_enc": self.client.get_session_id().replace("%2F", "/"),
            "num": self.id,
            "key": self.key,
            "pagewidth": 885,
            "t": Func.get_epoctime_int(),
        }
