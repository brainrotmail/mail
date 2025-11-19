from imap_tools import AND, MailBox
from imap_tools.message import MailMessage
from typing import Iterator
from bs4 import BeautifulSoup
import time


def extract_code():
    pass


def log_result():
    pass


def extract_urls(body: str) -> set:
    urls = set()
    soup = BeautifulSoup(body, "html.parser")
    for link in soup.find_all("a", href=True):
        urls.add(link["href"])
    return urls


def poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER):
    # "adapted" from here: https://github.com/ikvk/imap_tools/blob/master/examples/idle.py#L25
    done = False
    connection_start_time = time.monotonic()
    connection_live_time = 0.0
    while not done:
        try:
            mb = MailBox(HOST)
            with mb.login(USERNAME, PASSWORD, FOLDER) as mailbox:
                print("@@ new connection", time.asctime())
                while connection_live_time < 29 * 60:
                    try:
                        responses = mailbox.idle.wait(timeout=3 * 60)
                        print(time.asctime(), "IDLE responses:", responses)
                        if responses:
                            inbox_dump = mailbox.fetch(AND(seen=False))
                            process_mail(inbox_dump)
                    except KeyboardInterrupt:
                        print("~KeyboardInterrupt")
                        done = True
                        break
                    connection_live_time = time.monotonic() - connection_start_time

        except Exception as e:
            print(f"Got error: {e}; retrying in 15s.")
            time.sleep(15)
            continue


def process_mail(email_bundle: Iterator[MailMessage]):
    for msg in email_bundle:
        body = msg.html or msg.text or ""

        print(extract_urls(body))
        # open_urls(extract_urls(body))
