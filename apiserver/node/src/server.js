/**
 * [Rest API server for Chemvesol Kft.]
 * 
 * An example for a json structure:
 */
/**
 {
    "stationIdenfifier" : "Btr23CA",
    "date": "YY.mm.dd hh-ii-ss",
    "measures": [
       { "id": "A-40000", "value": "3.14" },
       { "id": "A-40001", "value": "12.64" },
       { "id": "A-40002", "value": "8.23" }
    ]
 }
 */

// The port of the API server inside the app
const port = 5000;

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


/**
 * [Receiving data]
 * http://localhost:5000/storedata/
 */
app.post('/storedata', (req, res) => {
  const stationIdenfifier = req.body['stationIdenfifier'];
  const date = req.body['date'];
  const measures = req.body['measures'];
 
  /**
  // Processing data
  answer = stationIdentifier + ' sent: ';
  for ( i of data.measures ) {
    answer += (i.id + "=" + i.value + ", ");
  }
  */
  res.send("OK");

  console.log("- Azonosito: " + stationIdenfifier);
  console.log("- Datum: " + date);
  console.log("Mért értékek:");
  for (i=0; i<measures.length; i++ )
    console.log("  - "+measures[i]["id"] + ": " + measures[i]["value"]);
});

app.listen(port, () => `Server running on port ${port}`);
