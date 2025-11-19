import os

from dotenv import load_dotenv

from handle_email import handle_email


def main():
    load_dotenv()
    HOST = os.getenv("MAIL_HOST")
    USERNAME = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    FOLDER = os.getenv("MAIL_FOLDER")
    handle_email.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)


if __name__ == "__main__":
    main()
