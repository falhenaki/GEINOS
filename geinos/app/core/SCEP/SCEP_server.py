import requests
from requests_ntlm import HttpNtlmAuth

"""
Gets the webpage of a SCEP server with a challenge password
TODO: User defined name and password
"""

def get_challenge_password():
    result = requests.get("http://192.168.56.102/certsrv/mscep_admin/",
                          auth=HttpNtlmAuth('domain\\administrator', 'Password12'))
    page = result.content.decode('UTF-16')
    str1 = 'The enrollment challenge password is: <B'
    i = 0
    for index,s in enumerate(page.split('>')):
        if s.find(str1) is 1:
            i = index + 1
    password = page.split('>')[i]
    print(page.split('>')[i][:17])
    return password