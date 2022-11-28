""" Modbus TCP Client and data forwareder """

import requests
import json

url = "http://193.225.33.218:5000/storedata/Btr23AC"

payload = json.dumps({
  "date": "YY.mm.dd hh-ii-ss",
  "measures": [
    {
      "id": "1",
      "value": "3.17"
    },
    {
      "id": "2",
      "value": "12.64"
    },
    {
      "id": "3",
      "value": "8.23"
    }
  ]
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
