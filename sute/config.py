class Config:
    HOST = "https://m.kuku.lu"
    PATH_ADDRESS_LIST = "/index._addrlist.php"
    PATH_SNED_MAIL = "/new.php"
    PATH_RECV_MAIL = "/recv.php"
    PATH_MAIL_LIST = "/recv._ajax.php"
    PATH_MAIL_CONTENT = "/smphone.app.recv.view.php"

    HEADERS: dict = {}

    SESSION_ID_KEY = "cookie_uidenc_seted"
    CSRF_TOKEN_KEY = "cookie_csrf_token"
    CSRF_TOKEN_TAG = "cookie_csrf_token"
