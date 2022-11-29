""" Modbus TCP Client and data forwarder """
import requests
import json
from datetime import datetime

# System parameters

# Station identifier string. It mus be set on the API side as well.
STATIONIDENTIFIER = "bRsT64wW23"
# RESTAPI Url
# URL = "http://phserver-2.linux-szerver.hu:5000/"
# TODO development server
URL = "http://193.225.33.218:5000/"
# API connection timeout in seconds
TIMEOUT = 10
# ModBus IDs
MODBUSIDS = [40000,40001,40002]
# Headers
HEADERS = {'Content-Type': 'application/json'}

def readModbusData():
    """ Reads data from the Modbus connection and returns it in JSON format """
    """

    Reading process wil be placed here
    
    """

    # TODO this has to be removed
    a1id=40000
    a1value=3.14
    a2id=40001
    a2value=8.22
    # Until that line

    jsonArr = {}
    jsonArr["stationIdenfifier"]=STATIONIDENTIFIER
    jsonArr["date"]=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    jsonArr["measures"]=[]
    # TODO this has to be changed
    jsonArr["measures"].append({ "id": a1id, "value": a1value })
    jsonArr["measures"].append({ "id": a2id, "value": a2value })

    return json.dumps(jsonArr)


dataToSend = readModbusData()

try:
  response = requests.request("POST", URL + "storedata/", headers=HEADERS, data=dataToSend, timeout=TIMEOUT)
except:
  print('Error. Stat are storing into a file: ' + dataToSend)
else:
  print(response.text)


