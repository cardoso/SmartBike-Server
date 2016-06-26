from smartbike.server.sbclienthandler import SBClientPacket

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Set up socket")


server_address = ('localhost', 7948)

sock.connect(server_address)
print("Connected to ", server_address)

try:
    out_packet = SBClientPacket.bike_handshake
    sock.sendall(out_packet)

    while out_packet != SBClientPacket.disconnect:
        in_packet = sock.recv(16)
        print("Received: ", in_packet)

        out_packet = input("Packet to send: ")
        sock.sendall(out_packet.encode())
finally:
    print("Closing socket")
    sock.close()
