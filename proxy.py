# HTTP proxy for intercepting HTTP requests & responses.
# David Golding 2019.

# Note: Only designed for testing purposes and won't catch a number of
# exceptions that are likely to occur in a TCP connection.

# With thanks to George Schizas - https://gist.github.com/gschizas/3731989

import socket, select, random, threading

class Proxy:

    # Creates a connection with the HTTP request destination
    def createForward(self, port):
        forward = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        forward.connect(("localhost", port))
        return forward

    # Creates the server to allow clients to connect
    def createServer(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', port))
        server.listen(10)
        return server

    # When a new client joins, create add their details and map the new client
    # to a desination socket
    def addConnection(self, new_client):
        self.current_connections.append(new_client)
        new = self.createForward(self.forward_port)
        self.current_connections.append(new)
        self.channel[new_client] = new
        self.channel[new] = new_client

    # Checks the connection hasn't been dropped, and if it hasn't sends the data
    # to a socket
    def forward(self, data, sock):
        if len(data) == 0:
            self.channel[sock].close()
            sock.close()
            forward = self.channel[sock]
            del self.channel[forward]
            del self.channel[sock]
            self.current_connections.remove(forward)
            self.current_connections.remove(sock)
        print(data)
        self.channel[sock].sendall(data)

    # Continously accepts new connections and checks for new data
    def start(self):
        while True:
            # Determines whether the sockets are ready based on the
            # current connections (blocking)
            read_sockets, write_sockets, error_sockets = \
                select.select(self.current_connections,[],[])
            # Accepts new connections and forwards existing ones
            for sock in read_sockets:
                if sock == self.server:
                    conn, addr = self.server.accept()
                    self.addConnection(conn)
                    break
                data = sock.recv(8912)
                print(data)
                self.forward(data, sock)

    # Requires the port to forward data to (forward_port) and the port for
    # the server to run on (server_port) - both local
    def __init__(self, forward_port, server_port):
        self.forward_port = forward_port
        self.server_port = server_port
        self.channel = {}
        self.server = self.createServer(self.server_port)
        self.current_connections = [self.server]

if __name__ == '__main__':
    # Starts the proxy
    proxy = Proxy(4567, 1234)
    proxy.start()
