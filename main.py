import os
import threading

from dotenv import load_dotenv

import handle_email.handle_email as handle_email


def main():
    load_dotenv()
    HOST = os.getenv("MAIL_HOST")
    USERNAME = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    FOLDER = os.getenv("MAIL_FOLDER")

    def killme():
        handle_email.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)

    threading.Thread(target=killme, name="killer").start()
    print("hi!")


if __name__ == "__main__":
    main()
