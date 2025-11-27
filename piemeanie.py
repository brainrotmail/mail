import os
import time
from typing import Iterator

import requests
from dotenv import load_dotenv
from imap_tools.mailbox import MailBox
from imap_tools.message import MailMessage
from imap_tools.query import AND
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Log

import handle_email.handle_email as mailman
import handle_users.handle_users as userman
import site_logic
from site_logic import Service

load_dotenv()
HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
FOLDER = os.getenv("MAIL_FOLDER")
RECEIVING_DOMAIN = "cutesillymeowmeow.xyz"


class Website_tinycc(Service):
    async def signup(self, receiving_domain: str, username: str):
        log = app.query_one("#signup-log", Log)
        signup_url = self.signup_url
        headers = self.headers

        # username = (
        #     userman.generate_username
        # )  # to do (replace with a signle function generate user, in the gen pass func)
        # password = userman.generate_password

        data = {
            "username": username,
            "email": f"{username}@{receiving_domain}",
            "password": userman.generate_password(),
        }

        response = requests.post(signup_url, headers=headers, data=data)

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{data}, {response}, \n")
        log.write_line(f" signup: logging {data}, {response},")

    async def verify(self, urls: set):
        log = app.query_one("#signup-log", Log)
        for i in urls:
            if self.verify_link_part in i:
                response = requests.get(i, headers=self.headers)
                log.write_line(f", verifying i: {response}")


tinycc = Website_tinycc(
    url="https://tinycc.com",
    signup_url="https://tinycc.com/tiny/signup",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    },
    sender_email="noreply@tinycc.com",
    uses_code=False,
    verify_link_part="https://tinycc.com/tiny/email-register",
)


class MainApp(App, Website_tinycc):
    """App to display account making."""

    def compose(self) -> ComposeResult:
        yield Button("tinycc.com signup :3", id="hi")
        with VerticalScroll(id="the-container"):
            yield Log(id="inbox-log")
            yield Log(id="signup-log")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        self.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)
        for i in range(5):
            await tinycc.signup(RECEIVING_DOMAIN, userman.generate_username())
            time.sleep(1)

    @work(exclusive=True, thread=True)
    def poll_mailserver(self, HOST, USERNAME, PASSWORD, FOLDER):
        # "adapted" from here: https://github.com/ikvk/imap_tools/blob/master/examples/idle.py#L25
        done = False
        connection_start_time = time.monotonic()
        connection_live_time = 0.0
        while not done:
            log = self.query_one("#inbox-log", Log)
            try:
                mb = MailBox(HOST)
                with mb.login(USERNAME, PASSWORD, FOLDER) as mailbox:
                    self.call_from_thread(
                        log.write_line, f"{'@@ new connection', time.asctime()}"
                    )
                    while connection_live_time < 29 * 60:
                        responses = mailbox.idle.wait(timeout=3 * 60)
                        self.call_from_thread(
                            log.write_line,
                            f"{time.asctime(), 'IDLE responses:', responses}",
                        )
                        if responses:
                            inbox_dump = mailbox.fetch(AND(seen=False))
                            self.call_from_thread(
                                log.write_line, "received some emails"
                            )
                            self.process_mail(inbox_dump)
                        connection_live_time = time.monotonic() - connection_start_time

            except Exception as e:
                self.call_from_thread(
                    log.write_line, f"Got error: {e}; retrying in 15s."
                )
                time.sleep(15)
                continue

    # @work(exclusive=True, thread=True)
    def process_mail(self, email_bundle: Iterator[MailMessage]):
        log = self.query_one("#inbox-log", Log)
        for msg in email_bundle:
            body = msg.html or msg.text or ""
            sender = msg.from_

            # service_target = {site for site in site_logic.services if site.sender_email == sender}
            # should return just one site in the set! ^^

            # for site in site_logic.services:
            #     if site.sender_email == sender:
            #         service_target = site

            if not tinycc.uses_code:
                urls = mailman.extract_urls(body)
                self.call_from_thread(
                    log.write_line, f"email contains these urls: {urls}"
                )
                hopefully = tinycc.verify(urls)
            else:
                pass


app = MainApp()
app.run()
