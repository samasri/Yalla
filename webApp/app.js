const express = require("express");
const app = express();
const PORT = 8080; // default port 8080

const http = require('http');

const hostname = '0.0.0.0'
const port = 8080;

app.set("view engine", "ejs");

app.use(express.static('static')); // Tell NodeJS where to find the JS/CSS files

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

app.get("/", (req, res) => {
  res.render("login", {"user": "user"});
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
