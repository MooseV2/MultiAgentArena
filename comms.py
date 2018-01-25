class Communications:
  def __init__(self):
    self.clients = {}
  
  def add_client(self, client):
    self.clients[client.id] = client

  def message_client(self, client_id, sender_id, message):
    self.clients[client_id].receive(message, sender_id)

  def message_all(self, sender_id, message):
    for clientid, obj in self.clients.items():
      obj.receive_broadcast(message, sender_id)