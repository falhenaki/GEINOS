import requests
from app.core.scep import scep_connector
from requests_ntlm import HttpNtlmAuth
from app.core.log import log_connector

"""
Gets the webpage of a scep server with a challenge password
"""


def get_thumbprint():
    server = scep_connector.get_scep()
    scep_admin = server.sys_server
    if server is None:
        return "Error: No SCEP server defined"

    try:
        result = requests.get(scep_admin,
                          auth=HttpNtlmAuth('domain\\' + server.username, server.password), timeout=1)
    except requests.exceptions.ConnectTimeout:
        return "Error: Connection to SCEP server timed out"

    if result.status_code == 401:
        return "Error 401 fro SCEP server: Unauthorized."

    page = result.content.decode('UTF-16')

    thumbprint_string = 'The thumbprint (hash value) for the CA certificate is: <B'
    thumbprint_string_index = 0
    for index,s in enumerate(page.split('>')):
        if s.find(thumbprint_string) is 1:
            thumbprint_string_index = index + 1
    thumbprint = page.split('>')[thumbprint_string_index].strip('</B').replace(" ","")
    return thumbprint


def get_otp():
    server = scep_connector.get_scep()
    scep_admin = server.sys_server
    if server is None:
        return "Error: No SCEP server defined"

    try:
        result = requests.get(scep_admin,
                          auth=HttpNtlmAuth('domain\\' + server.username, server.password), timeout=10)
    except requests.exceptions.ConnectTimeout:
        return "Error: Connection to SCEP server timed out"
    except requests.exceptions.ConnectionError:
        return "Error connecting to SCEP server."
    except Exception as e:
        return e
    if result.status_code == 401:
        return "Error 401 fro SCEP server: Unauthorized."

    page = result.content.decode('UTF-16')
    if "cache is full" in page:
        return "Error: Server password cache is full"

    if not page.find("The enrollment challenge password is"):
        return "Error: Could not find challenge password"
    pass_string = 'The enrollment challenge password is: <B'
    pass_string_index = 0
    for index,s in enumerate(page.split('>')):
        if s.find(pass_string) is 1:
            pass_string_index = index + 1
    password = page.split('>')[pass_string_index].strip('</B').strip()
    return password


def add_scep(server,username,password,digest,encrypt,cert_info_id,ca_server_id,country,state,locale,
                 organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id):
    """
    adds user with given username password and email
    :param username: username to add
    :param password: user password
    :return: true if server is added false otherwise
    """
    if scep_connector.add_scep(server,username,password,digest,encrypt,cert_info_id,ca_server_id,country,state,locale,
                               organization,org_unit,cert_server_id,key_id,ca_cert_id,client_cert_id):
        return True
    return False


def update_thumbprint(thumb):
    server = scep_connector.get_scep()
    if scep_connector.add_thumbprint(server,thumb):
        return True
    else:
        return False