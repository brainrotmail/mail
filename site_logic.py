import requests


class Service:
    def __init__(
        self, signup_url: str, signup_headers: str, email_domain: str, uses_code: bool
    ):
        self.signup_url = signup_url
        self.signup_headers = signup_headers
        self.email_domain = email_domain
        self.uses_code = uses_code


class Tiny_cc(Service):
    def signup(self):
        signup_url = self.signup_url
        headers = self.signup_headers

    def verify():
        pass


def tinycc(username, password, domain, headers, signup_url):
    signup_url = "https://tinycc.com/tiny/signup"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    }

    data = {
        "username": username,
        "email": f"{username}@{domain}",
        "password": password,
    }

    response = requests.post(signup_url, headers=headers, data=data)

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{data}, {response}, \n")
