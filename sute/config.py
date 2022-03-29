class Config:
    HOST = "https://m.kuku.lu"
    PATH_ADDRESS_LIST = "/index._addrlist.php"
    PATH_SNED_MAIL = "/new.php"
    PATH_RECV_MAIL = "/recv.php"
    PATH_MAIL_LIST = "/recv._ajax.php"
    PATH_MAIL_CONTENT = "/smphone.app.recv.view.php"

    HEADERS: dict = {
        "User-agent": "Mozilla/5.0 (Linux; Android 8.0.0;"
        "MI 5s Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/79.0.3945.4 Mobile Safari/537.36 YaApp_Android/10.30 YaSearchBrowser/10.30"
    }

    SESSION_ID_KEY = "cookie_uidenc_seted"
    CSRF_TOKEN_KEY = "cookie_csrf_token"
    CSRF_TOKEN_TAG = "cookie_csrf_token"
