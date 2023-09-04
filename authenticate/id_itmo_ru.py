from datetime import datetime

import requests
from pydantic import BaseModel, Field, HttpUrl, NonNegativeInt
from requests_oauthlib import OAuth2Session
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ID_ITMO_URL_AUTHORIZATION_ENDPOINT: str = (
    "https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/auth"
)

ID_ITMO_URL_TOKEN_ENDPOINT: str = (
    "https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/token"
)
ID_ITMO_URL_REDIRECT_PROFILE: str = "https://id.itmo.ru/login/callback"

USER_AGENT_ID_AUTHENTICATION: str = "isu2cal/1.0 (ReIdAp/1.2)"
USER_AGENT_GENERAL_REQUEST: str = "isu2cal/1.0"


class TokenResponseModel(BaseModel):
    access_token: str
    expires_in: NonNegativeInt
    refresh_expires_in: NonNegativeInt
    refresh_token: str
    token_type: str
    id_token: str
    not_before_policy: int = Field(..., alias="not-before-policy")
    session_state: str
    scope: list[str]
    expires_at: datetime


class ITMOAuthenticator:
    def __init__(
        self,
        client_id: str,
        client_secret: str | None,
        scope: list[str],
    ) -> None:
        self._client_id: str = client_id
        self._client_secret: str = client_secret if client_secret else ""
        self._scope = scope
        self.__oauth_session = OAuth2Session(
            client_id=self._client_id,
            redirect_uri=ID_ITMO_URL_REDIRECT_PROFILE,
            scope=self._scope,
        )
        self.__access_token: str | None = None
        self.__refresh_token: str | None = None
        self._token_type: str | None = None
        self._expires_at: datetime | None = None
        self.__post_init__()

    def __post_init__(self, enable_custom_user_agent: bool = False) -> None:
        firefox_profile = Options()
        if enable_custom_user_agent:
            firefox_profile.set_preference(
                "general.useragent.override",
                USER_AGENT_ID_AUTHENTICATION,
            )
        self.__driver = webdriver.Firefox(options=firefox_profile)
        self.__driver.implicitly_wait(10)

    def __update_tokens(self, token: TokenResponseModel) -> None:
        self.__access_token = token.access_token
        self.__refresh_token = token.refresh_token
        self._token_type = token.token_type
        self._expires_at = token.expires_at

    def authenticate(self) -> None:
        authorization_url, _ = self.__oauth_session.authorization_url(
            url=ID_ITMO_URL_AUTHORIZATION_ENDPOINT,
        )
        self.__driver.get(url=authorization_url)
        WebDriverWait(self.__driver, 60).until(
            EC.url_contains(ID_ITMO_URL_REDIRECT_PROFILE.__str__()),
        )
        callback_url = self.__driver.current_url
        self.__driver.close()
        token: TokenResponseModel = TokenResponseModel(
            **self.__oauth_session.fetch_token(
                token_url=ID_ITMO_URL_TOKEN_ENDPOINT,
                code=callback_url.split("code=")[1],
                method="POST",
                headers={
                    "User-Agent": USER_AGENT_ID_AUTHENTICATION,
                },
                include_client_id=True,
                client_secret=self._client_secret,
            ),
        )
        self.__update_tokens(token)
        self.__del_wd()

    def request(
        self,
        method: str,
        url: HttpUrl | str,
        timeout: NonNegativeInt = 20,
        user_agent: str = USER_AGENT_GENERAL_REQUEST,
        accept_language: str = "en",
        headers: dict | None = None,
        **kwargs,
    ) -> requests.Response:
        if headers is None:
            headers = {}
        headers.update(
            {
                "Authorization": f"Bearer {self.__access_token}",
                "User-Agent": user_agent,
                "Accept": "application/json",
                "Accept-Language": accept_language,
            },
        )
        return requests.request(
            method,
            url.__str__(),
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def __del_wd(self) -> None:
        self.__driver.quit()
