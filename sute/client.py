from typing import Optional

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

from .config import Config
from .exception import ConnectionTimeoutError, ReadTimeoutError


class Client:

    proxies: Optional[dict] = None
    session: requests.Session

    def __init__(self, proxies: Optional[dict] = None) -> None:
        self.proxies = proxies
        self.session = requests.Session()
        self.init_connection()

    def init_connection(self) -> None:
        self.get_request(Config.HOST)

    def get_csrf_token(self) -> str:
        return self.session.cookies.get_dict()[Config.CSRF_TOKEN_KEY]

    def get_session_id(self) -> str:
        return self.session.cookies.get_dict()[Config.SESSION_ID_KEY]

    def update_session_id(self, ses_id: str) -> None:
        self.session.cookies.set(Config.SESSION_ID_KEY, ses_id)
        self.init_connection()

    def save_session_id(self) -> None:
        with open(".ses", "wt") as ses_file:
            ses_file.write(self.get_session_id())

    def get_request(
        self, url: str, headers: dict = None, params: dict = None
    ) -> requests.Response:
        try:
            if headers is None:
                headers = Config.HEADERS
            return self.session.get(
                url=url,
                headers=headers,
                params=params,
                proxies=self.proxies,
                timeout=5.0,
            )
        except ConnectTimeout:
            raise ConnectionTimeoutError("[get failed] connection timeout.")
        except ReadTimeout:
            raise ReadTimeoutError("[get failed] read timeout.")
        except Exception:
            raise

    def post_request(
        self,
        url: str,
        headers: dict = None,
        json: dict = None,
        data: dict = None,
    ) -> requests.Response:
        try:
            if headers is None:
                headers = Config.HEADERS
            return self.session.post(
                url=url,
                headers=headers,
                json=json,
                data=data,
                proxies=self.proxies,
                timeout=5.0,
            )
        except ConnectTimeout:
            raise ConnectionTimeoutError("[post failed] connection timeout.")
        except ReadTimeout:
            raise ReadTimeoutError("[post failed] read timeout.")
        except Exception:
            raise
