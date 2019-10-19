# Client to submit HTTP requests to a server
# David Golding 2019.

import socket

class Client:

    # Given a HTTP request, sends it to the server
    def send(self, http_request):
        self.server.sendall(http_request)
        return self.server.recv(8912)

    # Connects to a local server given the port
    def __init__(self, server_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(("localhost", server_port))

if __name__=="__main__":
    server_port = 1234
    connect = Client(server_port)
    sent = connect.send(b"GET /login/ HTTP/1.1\r\nHost: localhost:%d\r\n\r\n" \
                        % (server_port))
    print(sent)
