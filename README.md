# BrainrotMail

## Description:

Generates unlimited email addresses (useful for website sign-ups) and automatically carries out the email verification step

## Operation:

Polls an IMAP server with [IDLE](https://en.wikipedia.org/wiki/IMAP_IDLE), scrapes links from the email HTML, sends http request/opens browser for the verification link
Reads credentials and settings from environment variables

TODO:
- per-site modules in separate user modules section
- menu to select these
- etc


# Setup instructions:
Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/):
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone repo:
```sh
git clone https://github.com/brainrotmail/mail && cd mail
```

Set environment variables:
```sh
cp ./.env.example ./.env
# edit the .env 
```

Run project:
```sh
uv run main.py
```




we tried like three imap libraries email is hard ok
