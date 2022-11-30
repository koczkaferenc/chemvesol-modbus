""" Modbus TCP Client and data forwarder """
import requests
import json
import os
import uuid
from datetime import datetime
from pyModbusTCP.client import ModbusClient


##################################################################################
#
##################################################################################
# If EMULATED, only random numbers will be sent
EMULATED = True
DEBUG=True
LOGFILE="/var/log/readModBus.log"

# System parameters
# ------------------------------------------------------------------------
# ModbusServer
# Modbus-TCP server address
MODBUSHOST = "192.168.10.76"
# Modbus-TCP Port
MODBUSPORT = 502
# Debug ModBus communication
MODBUSDEBUG = False

# ------------------------------------------------------------------------
# Station identifier string. It mus be set on the API side as well.
STATIONIDENTIFIER = "bRsT64wW23"
# RESTAPI Url
# URL = "http://phserver-2.linux-szerver.hu:5000/"
# TODO development server
URL = "http://193.225.33.218:5000/"
# API connection timeout in seconds
TIMEOUT = 10
# ModBus IDs
MODBUSIDS = [40000, 40001, 40002]
# Headers
HEADERS = {'Content-Type': 'application/json'}
# ModBus Spool Directory, do not change
MODBUSPOOLDIR='/var/modBusSpool'

##################################################################################
# Storing Log messages
##################################################################################
def logLine(msg):
    logFile = open(LOGFILE, 'a')
    logFile.write("L: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ": " + msg + "\n")
    logFile.close()

##################################################################################
# This function produces random data for testing.
# You can turn it off by EMULATED constant.
##################################################################################

def emulateReadModBusData():
    """ Emulates ModBus Reading Process """
    import random
    modBusData = []
    value = 0.00
    for i in MODBUSIDS:
        value = round(random.uniform(33.33, 66.66), 2)
        modBusData.append(({"id": i, "value": value}))
    return modBusData

##################################################################################
# Reading data from ModBus-TCP Source
##################################################################################

def readModBusData():
    """ Reads data from the Modbus connection and returns it in JSON format """
    # Connect to ModBus Server
    c = ModbusClient(host=MODBUSHOST, port=MODBUSPORT, auto_open=True, debug=MODBUSDEBUG)
    modBusData = []
    value = 0.00
    for i in MODBUSIDS:
        try:
            hr = c.read_holding_registers(i, 1)
            value = hr[0]
            modBusData.append(({"id": i, "value": value}))
        except:
          
            print("[%d]=%s" % (base+i, "not readable."))
    return modBusData

##################################################################################
# Creating JSON data structure
##################################################################################

def mkJsonStructure(modBusData):
    jsonArr = {}
    jsonArr["stationIdenfifier"] = STATIONIDENTIFIER
    jsonArr["date"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    jsonArr["measures"] = []
    # TODO this has to be changed
    # jsonArr["measures"].append({ "id": a1id, "value": a1value })
    jsonArr["measures"] = modBusData
    return json.dumps(jsonArr)

dataToSend = mkJsonStructure(emulateReadModBusData()) if EMULATED else mkJsonStructure(readModBusData())
logLine("INFO: " + dataToSend)
try:
    response = requests.request("POST", URL + "storedata/", headers=HEADERS, data=dataToSend, timeout=TIMEOUT)
except:
    logLine("ERR: API Server Connection error. Url: %s. UnSent data: %s." % (URL, dataToSend))
    if not os.path.exists(MODBUSPOOLDIR):
        logLine("Spool Directory Created: " + MODBUSPOOLDIR)
        os.makedirs(MODBUSPOOLDIR)
    spoolFile = open(MODBUSPOOLDIR + "/" + uuid.uuid4().hex + ".json", 'a')
    spoolFile.write(dataToSend)
    spoolFile.close()

else:
    logLine("OK: Response: " + response.text)
    numOfUnSentJsonFiles = 0
    for jsonFile in os.listdir(MODBUSPOOLDIR):
        if jsonFile.endswith(".json"):
            numOfUnSentJsonFiles += 1
    if numOfUnSentJsonFiles > 0:
        logLine("INFO: UnSent file(s) in the Spool Directory: %d" % numOfUnSentJsonFiles)