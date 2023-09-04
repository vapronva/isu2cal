import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

client_id = "profile"
client_secret = ""
authorization_url = "https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/auth"
token_url = "https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/token"
redirect_url = "https://id.itmo.ru/login/callback"
scope = ["openid", "email", "profile"]

driver = webdriver.Firefox()
driver.implicitly_wait(10)

oauth_session = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)
authorization_url, state = oauth_session.authorization_url(authorization_url)

driver.get(authorization_url)

callback_url = WebDriverWait(driver, 60).until(EC.url_contains(redirect_url))
callback_url = driver.current_url
print(callback_url)
driver.close()

code = callback_url.split("code=")[1]
print(code)

token = oauth_session.fetch_token(
    token_url=token_url,
    code=code,
    include_client_id=True,
    client_secret=client_secret,
)

response = requests.get(
    "https://qr.itmo.su/v1/user/pass",
    headers={"Authorization": "Bearer " + token["access_token"]},
)
print(response.json())

driver.quit()
