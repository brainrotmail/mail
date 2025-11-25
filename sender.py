import requests
import time
import random
import string

name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
cookies = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
}

website = 'https://tinycc.com'

for i in range(10):
    username = f"{name}{i}"
    email = f'{name}{i}@cutesillymeowmeow.xyz'
    password = 'test'
    
    data = {
        'username': username,
        'email': email,
        'password': password,
    }
    
    response = requests.post('https://tinycc.com/tiny/signup', cookies=cookies, headers=headers, data=data)
    
    # logging (we need to move it to a differt script later)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{website} - {email} - {password}\n")
    
    time.sleep(1)
