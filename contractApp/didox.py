import requests



headers = {'user-agent': 'my-app/0.0.1'}
URL = 'https://devapi.goodsign.biz'
authid = ''

def getAuth(serialNumber):
    payload = {}
    path = URL+'/v1/auth/authId/' + serialNumber

    r = requests.request("GET", path, headers=headers, data=payload)
    auth_id = r.text

    authid.join(auth_id)


def authDidox(auth_id, pkcs7):
    payload = {'authId':auth_id, 'pkcs7':pkcs7}
    path = URL+'/v1/auth/login'

    r = requests.request('POST', url=path, headers=headers, data=payload)

    print(r.text.encode('utf-8'))