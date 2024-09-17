import requests, json, os
from urllib.parse import unquote

def get_user_dao(query_id):
    token = get_access_token(query_id)
    headers = {
        'accept': 'application/json',
        'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.production.tonxdao.app/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger',
    }

    response = requests.get('https://app.production.tonxdao.app/api/v1/dao_users', headers=headers)

    if response.status_code != 200:
        return False

    return response.json()


def get_token(query_id):
    token = get_access_token(query_id)
    
    if not token:
        return False
    
    headers = {
        'accept': 'application/json',
        'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.production.tonxdao.app/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger',
    }

    response = requests.get('https://app.production.tonxdao.app/api/v1/centrifugo-token', headers=headers)
    
    if response.status_code != 200:
        return False
    
    return response.json()["token"]

def get_access_token(query_id):
    headers = {
        'accept': 'application/json',
        'accept-language': 'en,en-EG;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://app.production.tonxdao.app',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.production.tonxdao.app/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger',
    }

    json_data = {
        'initData': query_id,
    }
    
    response = requests.post('https://app.production.tonxdao.app/api/v1/login/web-app', headers=headers, json=json_data)
    
    if response.status_code != 200:
        return False
    
    return response.json()['access_token']

def get_username(query_id:str):
    data = json.loads(unquote(query_id).split('&')[1].split('=')[1])
    if 'username' in data:
        return data['username']
    return '<NOT SET>'
def config(name, default):
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config.get(name, default)


def banner():
    clear()
    banner = r"""
  ██████╗ ██╗     ██╗████████╗ ██████╗██╗  ██╗
 ██╔════╝ ██║     ██║╚══██╔══╝██╔════╝██║  ██║
 ██║  ███╗██║     ██║   ██║   ██║     ███████║
 ██║   ██║██║     ██║   ██║   ██║     ██╔══██║
 ╚██████╔╝███████╗██║   ██║   ╚██████╗██║  ██║
  ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
"""
    print(f"\033[92m{banner}")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
