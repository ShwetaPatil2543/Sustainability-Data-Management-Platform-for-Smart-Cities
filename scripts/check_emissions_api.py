import urllib.request, urllib.error

url = 'http://127.0.0.1:8000/api/emissions/'
try:
    resp = urllib.request.urlopen(url)
    print('CODE', resp.getcode())
    print(resp.read().decode('utf-8')[:1000])
except urllib.error.HTTPError as e:
    print('HTTP ERROR', e.code)
    try:
        print(e.read().decode('utf-8')[:1000])
    except:
        pass
except Exception as e:
    print('ERR', e)
