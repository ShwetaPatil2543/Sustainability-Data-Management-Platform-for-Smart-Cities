import json
import sys
import urllib.request as u

API = "http://127.0.0.1:8000"

def post_token(username, password):
    url = f"{API}/api/token/"
    data = json.dumps({"username": username, "password": password}).encode()
    req = u.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = u.urlopen(req, timeout=10)
        body = resp.read().decode()
        print("TOKEN_STATUS", resp.status)
        print(body)
        return json.loads(body)
    except Exception as e:
        print("TOKEN_ERROR", repr(e))
        return None

def get_smart_dashboard(token):
    url = f"{API}/api/dashboard/smart/"
    req = u.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = u.urlopen(req, timeout=10)
        body = resp.read().decode()
        print("DASH_STATUS", resp.status)
        print(body)
        return json.loads(body)
    except Exception as e:
        print("DASH_ERROR", repr(e))
        return None


def download_report(token, fmt="pdf"):
    url = f"{API}/api/reports/{fmt}/"
    req = u.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = u.urlopen(req, timeout=15)
        body = resp.read()
        print(f"REPORT_{fmt.upper()}_STATUS", resp.status)
        print(f"REPORT_{fmt.upper()}_LENGTH", len(body))
        return True
    except Exception as e:
        print(f"REPORT_{fmt.upper()}_ERROR", repr(e))
        return False


if __name__ == '__main__':
    username = 'sdmp_test'
    password = 'testpass123'

    tok = post_token(username, password)
    if not tok or 'access' not in tok:
        print('Failed to obtain access token')
        sys.exit(1)

    access = tok['access']
    get_smart_dashboard(access)
    download_report(access, 'pdf')
    download_report(access, 'csv')
