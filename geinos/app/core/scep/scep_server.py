import requests
from app.core.scep import scep_connector
from requests_ntlm import HttpNtlmAuth
from app.core.log import log_connector

"""
Gets the webpage of a scep server with a challenge password
"""

def get_challenge_password():
    server = scep_connector.get_scep()
    if server is None:
        return "Error: No SCEP server defined"

    try:
        result = requests.get(server.server,
                          auth=HttpNtlmAuth('domain\\' + server.username, server.password), timeout=1)
    except requests.exceptions.ConnectTimeout:
        return "Error: Connection to SCEP server timed out"

    if result.status_code == 401:
        return "Error 401 fro SCEP server: Unauthorized."

    page = result.content.decode('UTF-16')
    if "cache is full" in page:
        return "Error: Server password cache is full"

    if not page.find("The enrollment challenge password is"):
        return "Error: Could not find challenge password"
    str1 = 'The enrollment challenge password is: <B'
    i = 0
    for index,s in enumerate(page.split('>')):
        if s.find(str1) is 1:
            i = index + 1
    password = page.split('>')[i]
    return password

def add_scep(server,username, password):
    """
    adds user with given username password and email
    :param username: username to add
    :param password: user password
    :return: true if server is added false otherwise
    """
    if scep_connector.add_scep(server,username, password):
        return True
    return False
