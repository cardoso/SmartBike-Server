from socketserver import ThreadingMixIn, TCPServer

from smartbike.server.sbclienthandler import SBClientHandler


class SBServer(ThreadingMixIn, TCPServer):
    """ This class opens a threaded TCPServer and forwards connections to a
        client handler. """

    """ Initialize all properties here. """
    def __init__(self, server_address):
        TCPServer.__init__(self, server_address, SBClientHandler)

        self.daemon_threads = True

    """ Starts the TCPServer """
    def start(self):
        TCPServer.serve_forever(self)

    """ Called after a client has connected. """
    def client_connected(self, client):
        print("Client connected. ThreadId: {}".format(client.threadid))

    """ Called after a client has disconnected. """
    def client_disconnected(self, client):
        print("Client disconnected. ThreadId: {}".format(client.threadid))


