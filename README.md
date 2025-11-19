# BrainrotMail

## Description:

Generates email accounts using a self-hosted email server, signs up for a website, and completes the verification process.

## Purpose of the program:

This program is able to generate fully usable email accounts and pass the verification process for any website by running the verification link sent to it's inbox.
Here's are some potential uses for this wonderful and TOS following program that is supposed to be used for educational purpuses only:

- sign up a lot of accounts to some website's newsletter to participate in some giveaway they may be running
- spam someone from many email acccounts
- make a lot of alternative accounts for any website
- refer many fake users to a givaway that rewards you extra entries for each referral


## To do list:

[x] buy domain

[ ] set up a self hosted email server

[ ] make a script that generates emails on our email server 

[ ] make the script also read emails from different inboxes

[ ] make the script run the desired (verification) link that it detects in the inbox


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