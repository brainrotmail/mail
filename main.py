import email
import getpass

from imapclient import IMAPClient

HOST = "imap.mailbox.org"
USERNAME = input("Username: ")
PASSWORD = getpass.getpass()

# basic ass MVP:
# log into mailserver with IMAP,
# fetch new mail,
# extract all links,
# print to stdout
# using IMAPClient now


def main():
    with IMAPClient(HOST) as server:
        server.login(USERNAME, PASSWORD)
        server.select_folder("INBOX", readonly=True)

        messages = server.search("ALL")
        for uid, message_data in server.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            print(uid, email_message.get("From"), email_message.get("Subject"))


if __name__ == "__main__":
    main()
