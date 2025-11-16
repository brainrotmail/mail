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
    server = IMAPClient(HOST, use_uid=True)

    server.login(USERNAME, PASSWORD)

    select_info = server.select_folder("INBOX")
    print("%d messages in INBOX" % select_info[b"EXISTS"])

    messages = server.search("ALL")

    print("%d messages from our best friend" % len(messages))

    for msgid, data in server.fetch(messages, ["ENVELOPE"]).items():
        envelope = data[b"ENVELOPE"]

        print(envelope.subject.decode(), "\n")

    server.logout()


if __name__ == "__main__":
    main()
