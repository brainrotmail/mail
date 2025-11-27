import requests

import handle_users.handle_users as userman


class Service:
    def __init__(
        self,
        url: str,
        signup_url: str,
        headers: dict,
        sender_email: str,
        verify_link_part: str,
        uses_code: bool,
    ):
        self.url = url
        self.signup_url = signup_url
        self.headers = headers
        self.sender_email = sender_email
        self.verify_link_part = verify_link_part
        self.uses_code = uses_code


class Website_tinycc(Service):
    def signup(self, receiving_domain: str, username: str):
        signup_url = self.signup_url
        headers = self.headers

        # username = (
        #     userman.generate_username
        # )  # to do (replace with a signle function generate user, in the gen pass func)
        # password = userman.generate_password

        data = {
            "username": username,
            "email": f"{username}@{receiving_domain}",
            "password": userman.generate_password(),
        }

        response = requests.post(signup_url, headers=headers, data=data)

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{data}, {response}, \n")

    def verify(self, urls: set):
        for i in urls:
            if self.verify_link_part in i:
                response = requests.get(i, headers=self.headers)
                print(response)


tinycc = Website_tinycc(
    url="https://tinycc.com",
    signup_url="https://tinycc.com/tiny/signup",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    },
    sender_email="noreply@tinycc.com",
    uses_code=False,
    verify_link_part="https://tinycc.com/tiny/email-register",
)

services: frozenset = frozenset([tinycc])
