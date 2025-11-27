import os

from dotenv import load_dotenv

import handle_email.handle_email as mailman
import handle_users.handle_users as userman
import site_logic


def main():
    load_dotenv()
    HOST = os.getenv("MAIL_HOST")
    USERNAME = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    FOLDER = os.getenv("MAIL_FOLDER")
    RECEIVING_DOMAIN = os.getenv("RECEIVING_DOMAIN")
    for i in range(5):
        site_logic.tinycc.signup(RECEIVING_DOMAIN, userman.generate_username())
    mailman.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)


if __name__ == "__main__":
    main()
