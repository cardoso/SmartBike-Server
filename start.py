from smartbike.server.sbserver import SBServer


server = SBServer(("127.0.0.1", 7948))

try:
    server.start()
finally:
    server.server_close()
