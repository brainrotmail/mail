import requests

import handle_users.handle_users as userman


class Service:
    def __init__(
        self, signup_url: str, headers: dict, sender_email: str, uses_code: bool
    ):
        self.signup_url = signup_url
        self.headers = headers
        self.sender_email = sender_email
        self.uses_code = uses_code


class Website_tinycc(Service):
    def signup(self, receiving_domain: str):
        signup_url = self.signup_url
        headers = self.headers

        username = (
            userman.generate_username
        )  # to do (replace with a signle function generate user, in the gen pass func)
        password = userman.generate_password

        data = {
            "username": username,
            "email": f"{username}@{receiving_domain}",
            "password": password,
        }

        response = requests.post(signup_url, headers=headers, data=data)

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{data}, {response}, \n")

    def verify(self, urls: set):
        for i in urls:
            if "https://tinycc.com/tiny/email-register" in i:
                response = requests.get(i, headers=self.headers)
                print(response)


tinycc = Website_tinycc(
    signup_url="https://tinycc.com/tiny/signup",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    },
    sender_email="noreply@tinycc.com",
    uses_code=False,
)

services: frozenset = frozenset([tinycc])
