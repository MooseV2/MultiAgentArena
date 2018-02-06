class WebSocketClient {
  constructor(uri) {
    this.uri = "ws://localhost:8765";
    this.websocket = new WebSocket(this.uri);
    this.websocket.onopen = (e) => this.onOpen(e);
    this.websocket.onclose = (e) => this.onClose(e);
    this.websocket.onmessage = (e) => this.onMessage(e);
    this.websocket.onerror = (e) => this.onError(e);
  }

  onOpen(e) {
    console.log("Connection opened");
  }
  onClose(e) {
    console.log("Connection closed");
  }
  onMessage(e) {
    console.log(`Connection sent '${e.data}'`);
  }
  onError(e) {
    console.log(`Connection error '${e.data}'`);
    console.log(e);
  }

  send(message) {
    this.websocket.send(message);
  }
};