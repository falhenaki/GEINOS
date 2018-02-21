###class definitions go here###
# this is is just a simple call to see if we are able to communicate with the device/send data
import requests

filepath = 'body.txt'

with open(filepath) as fh:
  data = fh.read()

headers = {'Accept':'application/xml', 'Content-Type' : 'application/xml'}
r = requests.put('http://localhost:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/new-netconf-device', headers = headers, data = data)

print(r)
