import json
import urllib.request as u

API = "http://127.0.0.1:8000"

def register(username, email, password, role="analyst"):
    url = f"{API}/api/auth/register/"
    data = json.dumps({"username": username, "email": email, "password": password, "role": role}).encode()
    req = u.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = u.urlopen(req, timeout=10)
        print('STATUS', resp.status)
        print(resp.read().decode())
    except Exception as e:
        print('ERROR', repr(e))

if __name__ == '__main__':
    register('newuser2', 'newuser2@local', 'pwd12345')
