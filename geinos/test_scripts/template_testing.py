import requests

def test_upload():
    file = open('config_output.xml')
    payload = {'file': file, 'filename': 'config_output.xml'}
    login = {'username': 'test', 'password': 'password'}
    s = requests.session()
    print(payload)
    r = s.get('http://127.0.0.1:5000')
    r = s.post('http://127.0.0.1:5000/login', login)
    r = s.post('http://127.0.0.1:5000/uploaded_files', files=payload)
    print(r.json())
    r = s.get('http://127.0.0.1:5000/uploaded_files/config_output.xml')
    print(r.json())

test_upload()

def test_jinjaconvert():
    r = requests.put('http://127.0.0.1:5000/uploaded_files/generate_jinja2/config_output.xml')

#test_jinjaconvert()