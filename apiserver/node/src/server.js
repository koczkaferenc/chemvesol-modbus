/**
 * [Rest API server for Chemvesol Kft.]
 * 
 * An example for a json structure:
 */
/**
 {
    "date": "YY.mm.dd hh-ii-ss",
    "measures": [
       { "id": "1", "value": "3.14" },
       { "id": "2", "value": "12.64" },
       { "id": "3", "value": "8.23" }
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
 * http://localhost:5000/storedata/Btr23AC
 */
app.post('/storedata/:stationIdenfifier', (req, res) => {
  const stationIdentifier = req.params['stationIdenfifier'];
  const data = req.body;
  // Processing data
  answer = stationIdentifier + ' sent: ';
  for ( i of data.measures ) {
    answer += (i.id + "=" + i.value + ", ");
  }
  res.send(answer);
});

app.listen(port, () => `Server running on port ${port}`);
