import sys
import socket
import threading
from manager import Manager
from time import sleep
try:
    import Queue as queue
except ImportError:
    import queue

class Server(threading.Thread):

    def __init__(self, in_server_queue, logqueue = None):
        super(Server, self).__init__()

        self.logqueue = logqueue
        self._ipAddress = None
        self._port = None
        self._out_server_queue = queue.Queue()
        self._in_server_queue = in_server_queue
        self.init_socket()
        self.show_log = True
        self.run_server = True
        self.server_manager = Manager()


    def init_socket(self):
         self._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def getOutQueue(self):
        return self._out_server_queue

    def setIpAddress(self, ipAddress):
        self._ipAddress = ipAddress

    def setPort(self,port):
        self._port = port

    def run(self):
        self._run()

    def reset(self):
        self._run()

    def _run(self):

        if self.server_manager.isServerRunning:
            self.server_manager.stop_server()
        else:
            self.server_manager.start_server()
        '''
        while self.run_server:
            try:
                self.server_address = (self._ipAddress, self._port)
                self.log('Starting up on %s port %s' % self.server_address )
                self._sock.bind(self.server_address)
                self._sock.listen(1)
                self.log('Waiting for a connection...')
                self._connection, self._client_address = self._sock.accept()
                self.log('Connection form {}'.format(self._client_address))
            except Exception as e:
                self.log("EXCEPTION: {}".format(sys.exc_info()))
                self._sock.close()
                self.init_socket()
                self.log("Socked closed")
                return

            try:
                self.listen()
            except Exception as e:
                self.log("EXCEPTION: {}".format(sys.exc_info()))
                self._sock.close()
                self.init_socket()
            '''

    def listen(self):
        while self.run_server:
            self.receive()
            while not self._out_server_queue.empty() or self._in_server_queue.empty():
                sleep(0.02)
            self.send()

    def receive(self):
        data = self._connection.recv(1024)
        if self.show_log:
            self.log('Receive: {}'.format(data))
        self._out_server_queue.put(data)

    def send(self):
        while not self._in_server_queue.empty():
            data = self._in_server_queue.get()
            if self.show_log:
                self.log('Send: {}'.format(data))
            self._connection.sendall(str(data))

    def set_server_log(self, show):
        self.show_log = show

    def set_logqueue(self,logqueue):
        self.logqueue = logqueue

    def log(self, message):
        print("{}: {}".format(self.__class__.__name__,message))
        if self.logqueue is not None:
            self.logqueue.append((self,message))