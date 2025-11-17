import email
import getpass
from email.policy import default as default_policy

from bs4 import BeautifulSoup
from imapclient import IMAPClient
from imapclient.response_types import SearchIds

HOST = "imap.mailbox.org"
USERNAME = input("Username: ")
PASSWORD = getpass.getpass()
FOLDER = "skoptsy"

# basic ass MVP:
# log into mailserver with IMAP,
# fetch new mail, (all for now)
# extract all links,
# print to stdout
# using IMAPClient now
# ^ working!


def main():
    with IMAPClient(HOST) as server:
        server.login(USERNAME, PASSWORD)
        server.select_folder(FOLDER, readonly=True)

        messages = server.search("ALL")
        print(type(messages))
        # for uid, message_data in server.fetch(messages, "RFC822").items():
        #     email_message = email.message_from_bytes(message_data[b"RFC822"])
        #     print(uid, email_message.get_content_type())
        process_emails(server, messages)


def process_emails(server: IMAPClient, messages: SearchIds):
    for uid, message_data in server.fetch(messages, "RFC822").items():
        email_message = email.message_from_bytes(
            message_data[b"RFC822"], policy=default_policy
        )
        if email_message.is_multipart():
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body += part.get_payload()
                    elif content_type == "text/html":
                        body += part.get_payload(decode=True).decode("utf-8")
            else:
                body = email_message.get_payload(decode=True).decode("utf-8")

            print(
                email_message.get_content_type(),
                html_extract_urls(body),
            )
    pass


def html_extract_urls(body):
    urls = set()
    html_document = body
    soup = BeautifulSoup(html_document, "html.parser")
    links = soup.find_all("a")
    for link in links:
        urls.add(link.get("href"))
    return urls


def text_extract_urls():
    pass


if __name__ == "__main__":
    main()
