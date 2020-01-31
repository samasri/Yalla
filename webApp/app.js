const express = require("express");
const http = require('http');
var mysql      = require('mysql');

const app = express();
const PORT = 8080; // default port 8080
const hostname = '0.0.0.0'
const port = 8080;

app.set("view engine", "ejs");

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
  connection.query("SELECT DISTINCT(tripID) FROM trips", function (error, results, fields) {
    results = results.slice(0,5);
    tripIDs = []
    for(var r of results) tripIDs.push(r.tripID);
    res.render("login", {"tripIDs": tripIDs});
  });
});

app.get("/trips", (req,res) => {
  connection.query("SELECT DISTINCT(tripID) FROM trips", function (error, results, fields) {
    results = results.slice(0,5);
    tripIDs = []
    for(var r of results) tripIDs.push(r.tripID);
    res.end(tripIDs.toString());
  });
});

// app.get("/trip/:tripID", (req,res) => {
//   connection.query("SELECT DISTINCT(tripID) FROM trips", function (error, results, fields) {
//     results = results.slice(0,5);
//     tripIDs = []
//     for(var r of results) tripIDs.push(r.tripID);
//     res.end(tripIDs.toString());
//   });
// });

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
