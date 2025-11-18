import getpass

from bs4 import BeautifulSoup
from imap_tools import AND, MailBox

HOST = "imap.mailbox.org"
USERNAME = input("Username: ")
PASSWORD = getpass.getpass()
FOLDER = "BRAINROT"


def main():
    mailbox = MailBox(HOST)
    mailbox.login(USERNAME, PASSWORD, FOLDER)
    for msg in mailbox.fetch(AND(all=True)):
        body = msg.html or msg.text or ""

        urls = set()
        soup = BeautifulSoup(body, "html.parser")
        for link in soup.find_all("a", href=True):
            urls.add(link["href"])

        print(urls)


if __name__ == "__main__":
    main()
