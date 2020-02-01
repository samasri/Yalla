const express = require("express");
const http = require('http');
var mysql      = require('mysql');

const app = express();
const PORT = 8080; // default port 8080
const hostname = '0.0.0.0'
const port = 8080;


app.use(express.static('static')); // Tell NodeJS where to find the JS/CSS files

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'samasri2',
  password : '1',
  database : 'yallaDb'
});
 
connection.connect();

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/views/index.html");
});

app.get("/routes", (req,res) => {
  connection.query("SELECT DISTINCT(routeID) FROM Delay", function (error, results, fields) {
    tripIDs = []
    for(var r of results) tripIDs.push(r);
    res.end(JSON.stringify(tripIDs));
  });
});

app.get("/stops", (req,res) => {
  query = `SELECT DISTINCT(Delay.stopID),lon,lat,delay,nbOfData
            FROM Delay 
            INNER JOIN Stop 
            ON Delay.stopID=Stop.StopID
            WHERE routeID='${req.query.routeID}'`
  connection.query(query, function (error, results, fields) {
    res.end(JSON.stringify(results));
  });
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
