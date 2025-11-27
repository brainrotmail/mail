import time
from typing import Iterator

from bs4 import BeautifulSoup
from imap_tools.mailbox import MailBox
from imap_tools.message import MailMessage
from imap_tools.query import AND

import site_logic


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
                    responses = mailbox.idle.wait(timeout=3 * 60)
                    print(time.asctime(), "IDLE responses:", responses)
                    if responses:
                        inbox_dump = mailbox.fetch(AND(seen=False))
                        process_mail(inbox_dump)
                    connection_live_time = time.monotonic() - connection_start_time

        except Exception as e:
            print(f"Got error: {e}; retrying in 15s.")
            time.sleep(15)
            continue


def process_mail(email_bundle: Iterator[MailMessage]):
    for msg in email_bundle:
        body = msg.html or msg.text or ""
        sender = msg.from_

        # service_target = {site for site in site_logic.services if site.sender_email == sender}
        # should return just one site in the set! ^^

        for site in site_logic.services:
            if site.sender_email == sender:
                service_target = site

        if not service_target.uses_code:
            urls = extract_urls(body)
            print(urls)
            service_target.verify(urls)
        else:
            pass
