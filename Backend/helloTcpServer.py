import socket
from port_knock_track import PortKnock


class HelloTcpServer():
    def __init__(self, port_knock_track, stop_event):
        self.port_knock_track = port_knock_track
        self.stop_event = stop_event
        self.tcpListenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ('127.0.0.1', 8080)
        self.tcpListenSock.bind(self.serverAddr)
            
    def runServer(self):
        while not self.stop_event.is_set():
            self.tcpListenSock.listen(1)
            while True:
                connection, clientAddr = self.tcpListenSock.accept()
                # check if this client address is allowed
                # TODO use mutex
                if self.port_knock_track.checkIpAllowed(clientAddr):
                    time.sleep(2)
                    self.port_knock_track.connection_established(clientAddr)
                    # OK!
                    connection.write("Hello")
                    connection.close()
                    time.sleep(2)
                    self.port_knock_track.remove_ip(clientAddr)
                else:
                    # How about NO
                    connection.close()

