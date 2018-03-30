const express = require('express')
const socket = require('socket.io')
const fs = require('fs')

// Read Scenerio File as a json object.
// Ensure all iterations are place inside [] 
// and not {} in the json file.
const content = fs.readFileSync("dummy.json");
const array_content = JSON.parse(content)

const app = express()
const server = app.listen(3000)

app.use(express.static('public'))

console.log("Server Running...")

// Socket Time
const io = socket(server)

io.on('connection', function (socket) {
  socket.emit('connected_server', 'Server Connected!');

  socket.on('connected_client', (data) => {
    console.log(data);

    // send file content
    socket.emit('transfer_file', array_content)
  });
});