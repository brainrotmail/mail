import os
import threading
import time

from dotenv import load_dotenv
from imap_tools.mailbox import MailBox
from imap_tools.query import AND
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Log

import handle_email.handle_email as mailman
import handle_users.handle_users as userman
import site_logic

load_dotenv()
HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
FOLDER = os.getenv("MAIL_FOLDER")
RECEIVING_DOMAIN = "cutesillymeowmeow.xyz"


class MainApp(App):
    """App to display account making."""

    def compose(self) -> ComposeResult:
        yield Button("Hiii", id="hi")
        with VerticalScroll(id="the-container"):
            yield Log(id="inbox-log")

    def poll_mailserver(self, HOST, USERNAME, PASSWORD, FOLDER):
        # "adapted" from here: https://github.com/ikvk/imap_tools/blob/master/examples/idle.py#L25
        done = False
        connection_start_time = time.monotonic()
        connection_live_time = 0.0
        while not done:
            log = self.query_one(Log)
            try:
                mb = MailBox(HOST)
                with mb.login(USERNAME, PASSWORD, FOLDER) as mailbox:
                    log.write_line(f"{'@@ new connection', time.asctime()}")
                    while connection_live_time < 29 * 60:
                        responses = mailbox.idle.wait(timeout=3 * 60)
                        log.write_line(
                            f"{time.asctime(), 'IDLE responses:', responses}"
                        )
                        if responses:
                            inbox_dump = mailbox.fetch(AND(seen=False))
                            mailman.process_mail(inbox_dump)
                        connection_live_time = time.monotonic() - connection_start_time

            except Exception as e:
                print(f"Got error: {e}; retrying in 15s.")
                time.sleep(15)
                continue

    async def siteupper(self):
        site_logic.tinycc.signup(
            RECEIVING_DOMAIN,
            userman.databaseaddstuff(site_logic.tinycc.url, "batchname").name,
        )
        log = self.query_one(Log)

        log.write_line("WHATEVER")

    def killme(self):
        self.poll_mailserver(HOST, USERNAME, PASSWORD, FOLDER)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        self.update_weather("Barcelona")

    @work(exclusive=True)
    async def update_weather(self, city: str) -> None:
        """Update the weather for the given city."""
        inbox_log_widget = self.query_one("#inbox-log", Log)
        if city:
            # weather = await siteupper("cutesillymeowmeow.xyz")
            # weather_widget.write(weather)
            results = await self.siteupper()
            inbox_log_widget.write(results)
            threading.Thread(target=self.killme, name="killer").start()

        else:
            # No city, so just blank out the weather
            inbox_log_widget.write("")


app = MainApp()
app.run()
