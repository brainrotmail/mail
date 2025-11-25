from imap_tools import MailBox, A
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import webbrowser
import time
import os

load_dotenv()

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def openlinks():
    with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as m:
        while True:
            for msg in m.fetch(A(seen=False)):
                html = msg.html or ""
                soup = BeautifulSoup(html, "html.parser")
        
                links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
                
                for link in links:
                    if link.startswith("https://tinycc.com/tiny/email-register/"):
                        webbrowser.open(link)
            
            time.sleep(10)