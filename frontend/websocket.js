class WebSocketClient {
  constructor(parseCommand) {
    this.uri = "ws://localhost:8765";
    this.websocket = new ReconnectingWebSocket(this.uri, null, {reconnectInterval: 3000});
    this.websocket.onopen = (e) => this.onOpen(e);
    this.websocket.onclose = (e) => this.onClose(e);
    this.websocket.onmessage = (e) => this.onMessage(e);
    this.connected = false;
    this.parseCommand = parseCommand;
    this.send_queue = [];
  }

  onOpen(e) {
    document.querySelector('#conn-status').innerHTML = 'Connected'
    this.connected = true;
    console.log("Connection opened");
    this.send(JSON.stringify({'cmd': 'connected'}));
  }

  onClose(e) {
    if (this.connected) {
      this.parseCommand({'cmd': 'reset'});
      document.querySelector('#conn-status').innerHTML = 'Disconnected'
    }
    this.connected = false;
  }

  onMessage(e) {
    if (e.data == 'REQ') { // Client data is requested
      if (this.send_queue.length == 0) {
        this.send_packet('DONE');
      } else {
        this.send_packet(this.send_queue.shift());
      }
    } else this.parseCommand(JSON.parse(e.data));
  }

  send(message) {
    this.send_queue.push(message);
  }

  send_packet(message) {
    this.websocket.send(message);
  }
};