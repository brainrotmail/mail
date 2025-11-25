import requests

def tinycc(username, password, domain):
    cookies = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
    }
    website = 'https://tinycc.com'
    
    data = {
        'username': username,
        'email': f"{username}@{domain}",
        'password': password,
    }

    response = requests.post('https://tinycc.com/tiny/signup', cookies=cookies, headers=headers, data=data)
    
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{data},{response}, \n")