from typing import List, Optional

from .client import Client
from .config import Config
from .exception import AlreadyEmailAddressExsist, UnknownException
from .function import Func
from .objects import Mail


class Sute:
    client: Client
    ses_id: Optional[str] = None
    mails: List[Mail] = []

    def __init__(
        self, ses_id: Optional[str] = None, proxies: Optional[dict] = None
    ) -> None:
        self.client = Client(proxies)
        self.ses_id = ses_id
        self.login()

    def login(self) -> None:
        if self.ses_id:
            self.client.update_session_id(self.ses_id)
        else:
            self.client.save_session_id()
        self.refresh_address_list()

    def refresh_address_list(self) -> None:
        res = self.client.get_request(Config.HOST + Config.PATH_ADDRESS_LIST)
        self.mails = [
            Mail(address, self.client)
            for address in Func.get_all_tag_texts(res.text, "span")
        ]

    def get_all_domain(self) -> list:
        res = self.client.get_request(Config.HOST)
        return Func.get_all_radio_button_values(res.text, "input_manualmaildomain")

    def create_new_address(self, user: str, domain: str) -> Mail:
        self.check_new_address(user, domain)
        params = self._create_payload(user, domain, "addMailAddrByManual")
        self.client.get_request(Config.HOST, params=params)
        self.refresh_address_list()
        return self.mails[-1]

    def create_new_random_address(self) -> Mail:
        params = self._create_payload("", "", "addMailAddrByAuto")
        self.client.get_request(Config.HOST, params=params)
        self.refresh_address_list()
        return self.mails[-1]

    def check_new_address(self, user: str, domain: str) -> None:
        params = self._create_payload(user, domain, "checkNewMailUser")
        res = self.client.get_request(Config.HOST, params=params)
        if "OFFER" in res.text:
            suggest_address = "{user}@{domain}".format(
                user=res.text.split(",")[1], domain=res.text.split(",")[2]
            )
            raise AlreadyEmailAddressExsist(
                f"{user}@{domain} is already exists. suggest: {suggest_address}"
            )
        elif "OK" == res.text:
            pass
        else:
            raise UnknownException("reason='{reason}'".format(reason=res.text))

    def _create_payload(self, user: str, domain: str, action: str) -> dict:
        return {
            "action": action,
            "nopost": 1,
            "UID_enc": self.client.get_session_id(),
            "csrf_token_check": self.client.get_csrf_token(),
            "newuser": user,
            "newdomain": domain,
            "_": Func.get_epoctime_int(),
        }
