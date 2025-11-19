import os
import webbrowser
from dotenv import load_dotenv
from handle_email import handle_email




def main():
    load_dotenv()
    HOST = os.getenv("MAIL_HOST")
    USERNAME = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")
    FOLDER = os.getenv("MAIL_FOLDER")
    handle_email.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)


def open_urls(urls):
    for i in urls:
        if i.startswith("https://"):
            webbrowser.open(i)


if __name__ == "__main__":
    main()
