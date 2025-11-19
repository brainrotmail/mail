import getpass
import time
from typing import Iterator

from bs4 import BeautifulSoup
from imap_tools import AND, MailBox
from imap_tools.message import MailMessage

HOST = "imap.gmx.org"
USERNAME = input("Username: ")
PASSWORD = getpass.getpass()
FOLDER = "INBOX"


def main():
    # mailbox = MailBox(HOST)
    # mailbox.login(USERNAME, PASSWORD, FOLDER)
    # inbox_dump = mailbox.fetch(AND(all=True))

    # process_mail(inbox_dump)
    poll_mailserver()
    pass


def poll_mailserver():
    while True:
        try:
            mb = MailBox(HOST)
            with mb.login(USERNAME, PASSWORD, FOLDER) as mailbox:
                inbox_dump = mailbox.fetch(AND(seen=False))

                process_mail(inbox_dump)

        except Exception as e:
            print(f"Got error: {e}; retrying in 15s.")
            time.sleep(15)
            continue

        time.sleep(60)


def process_mail(email_bundle: Iterator[MailMessage]):
    for msg in email_bundle:
        body = msg.html or msg.text or ""

        print(extract_urls(body))
        print("*** === ***")


def extract_urls(body: str) -> set:
    urls = set()
    soup = BeautifulSoup(body, "html.parser")
    for link in soup.find_all("a", href=True):
        urls.add(link["href"])
    return urls


# so i need it to:
# - detect new email (in loop? IDLE?)
# - decide if email plaintext or hmtl
# - extract URLs
# - send http requests to all/some


if __name__ == "__main__":
    main()
