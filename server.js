const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const server = http.createServer((req, res) => {
  // Set the content type
  res.setHeader('Content-Type', 'text/html');

  // Read the HTML file
  fs.readFile(path.join(__dirname, 'index.html'), (err, htmlData) => {
    if (err) {
      // If there's an error reading the HTML file, return a 500 error
      res.writeHead(500);
      res.end('Error loading index.html');
      return;
    }

    // Read the JSON file
    fs.readFile(path.join(__dirname, 'meal_data.json'), (err, jsonData) => {
      if (err) {
        // If there's an error reading the JSON file, return a 500 error
        res.writeHead(500);
        res.end('Error loading meal_data.json');
        return;
      }

      // Serve the HTML file with JSON data embedded
      res.writeHead(200);
      res.end(htmlData.toString().replace('{{jsonData}}', JSON.stringify(JSON.parse(jsonData), null, 4)));
    });
  });
});

server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
