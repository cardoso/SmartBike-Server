import socketserver
import threading


class SBClientState:
    """ This class acts as an enum of the possible states of clients. """
    disconnected = -1
    waiting_handshake = 0
    connected = 1


class SBClientType:
    """ This class acts as an enum of the possible types of clients. """
    unknown = -1
    bike = 0
    user = 1


class SBClientBase:
    """ This class must be inherited by clients (bike, user). """

    """ Initialize all properties here. """
    def __init__(self, handler):
        self.handler = handler
        self.state = SBClientState.waiting_handshake
        self.type = SBClientType.unknown
        self.threadid = threading.current_thread().name

        pass

    """ Called after client handler receives a packet. """
    def did_receive_packet(self, packet):
        pass

    """ Called before client is disconnected. """
    def will_disconnect(self):
        pass

    """ Called after client is disconnected. """
    def did_disconnect(self):
        pass


class SBBike(SBClientBase):
    """ This class handles requests from a bike. """

    """ Initialize all properties here. """
    def __init__(self, handler):
        SBClientBase.__init__(self, handler)

        self.state = SBClientState.connected
        self.type = SBClientType.bike

        self.location = (0.0, 0.0, 0.0)
        self.speed = 0.0
        self.locked = False

    """ Called after client handler receives a packet. """
    def did_receive_packet(self, packet):
        print("Bike: {}".format(packet))
        self.handler.request.sendall(b"OKBIKE")


class SBUser(SBClientBase):
    """ This class handles requests from a user. """

    """ Initialize all properties here. """
    def __init__(self, handler):
        SBClientBase.__init__(self, handler)

        self.state = SBClientState.connected
        self.type = SBClientType.user

    """ Called after client handler receives a packet. """
    def did_receive_packet(self, packet):
        print("User: {}".format(packet))
        self.handler.request.sendall(b"OKUSER")


class SBClientPacket:
    """ This class acts as an enum of the possible packets sent by clients. """

    user_handshake = b"HSUSER"
    bike_handshake = b"HSBIKE"
    disconnect = b"DC!"


class SBClientHandler(socketserver.StreamRequestHandler):
    """ This class handles requests from any client. """

    """ Called before the handle() method to perform any initialization actions
        required. """
    def setup(self):
        socketserver.StreamRequestHandler.setup(self)

        self.client = SBClientBase(self)
        self.max_packet_length = 1024

        self.server.client_connected(self.client)

    """ This method must do all the work required to service a request. """
    def handle(self):
        while self.client.state != SBClientState.disconnected:
            if self.client.state == SBClientState.waiting_handshake:
                self.handshake()
            else:
                packet = self.receive_packet()
                if packet != b"" and packet != SBClientPacket.disconnect:
                    self.client.did_receive_packet(packet)
                else:
                    self.client.state = SBClientState.disconnected
                    self.server.client_disconnected(self.client)

    """ This method listens for a packet """
    def receive_packet(self):
        return self.request.recv(self.max_packet_length)

    """ This method handles a 'handshake'.
        It identifies the type of client and authenticates it. """
    def handshake(self):
        packet = self.receive_packet()
        if packet == SBClientPacket.bike_handshake:
            self.client = SBBike(self)
            self.request.sendall(b"OKBIKE")
        elif packet == SBClientPacket.user_handshake:
            self.client = SBUser(self)
            self.request.sendall(b"OKUSER")
        else:
            self.client.state = SBClientState.disconnected

    """ Called after the handle() method to perform any clean-up actions
        required. """
    def finish(self):
        socketserver.StreamRequestHandler.finish(self)
