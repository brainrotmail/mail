import requests

import handle_users.handle_users as userman


class Service:
    def __init__(
        self, signup_url: str, signup_headers: dict, email_domain: str, uses_code: bool
    ):
        self.signup_url = signup_url
        self.signup_headers = signup_headers
        self.email_domain = email_domain
        self.uses_code = uses_code

        def verify(self):
            pass


class Tiny_cc(Service):
    def signup(self, receiving_domain):
        signup_url = self.signup_url
        headers = self.signup_headers

        username = userman.generate_username
        password = userman.generate_password

        data = {
            "username": username,
            "email": f"{username}@{receiving_domain}",
            "password": password,
        }

        response = requests.post(signup_url, headers=headers, data=data)

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{data}, {response}, \n")


tiny1 = Tiny_cc(
    "https://tinycc.com/tiny/signup",
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    },
    "tinycc.com",
    False,
)
