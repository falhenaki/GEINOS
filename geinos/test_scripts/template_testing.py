import requests

def test_upload():
    file = open('config_output.xml')
    my_string = file.read()
    payload = {'file': my_string, 'filename': 'config_output.xml'}
    login = {'username': 'test', 'password': 'password'}
    s = requests.session()
    r = s.get('http://127.0.0.1:5000')
    r = s.post('http://127.0.0.1:5000/login', login)
    r = s.post('http://127.0.0.1:5000/uploaded_files', files=payload)
    r = s.get('http://127.0.0.1:5000/uploaded_files/config_output.xml')

test_upload()

def test_jinjaconvert():
    r = requests.put('http://127.0.0.1:5000/uploaded_files/generate_jinja2/config_output.xml')
    #print(r.text)
    r = requests.post('http://127.0.0.1:5000/assign/config_output.xml/group1')


test_jinjaconvert()