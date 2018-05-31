import requests


from requests_ntlm import HttpNtlmAuth

result=requests.get("http://192.168.56.102/certsrv/mscep_admin/",auth=HttpNtlmAuth('domain\\administrator','Password12'))
print(result.content.decode('UTF-16'))