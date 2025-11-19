import getpass
from typing import Iterator

from bs4 import BeautifulSoup
from imap_tools import AND, MailBox
from imap_tools.message import MailMessage

HOST = "imap.gmx.org"
USERNAME = input("Username: ")
PASSWORD = getpass.getpass()
FOLDER = "INBOX"


def main():
    mailbox = MailBox(HOST)
    mailbox.login(USERNAME, PASSWORD, FOLDER)
    inbox_dump = mailbox.fetch(AND(all=True))

    process_mail(inbox_dump)


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
