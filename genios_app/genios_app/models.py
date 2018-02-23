###class definitions go here###
# this is is just a simple call to see if we are able to communicate with the device/send data
import requests, os
def simple_ping():
  """
  Basic test ping to check if the Orbit device can be reached
  :return: response from device
  """
  APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
  APP_STATIC = os.path.join(APP_ROUTE, 'static')
  filepath = 'body.txt'

  with open(os.path.join(APP_STATIC, filepath)) as fh:
    data = fh.read()

  headers = {'Accept':'application/xml', 'Content-Type' : 'application/xml'}
  r = requests.put('http://localhost:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/new-netconf-device', headers = headers, data = data)

  return r
