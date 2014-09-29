import sys
import socket
from time import sleep

class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1',10001)
        print('connecting ro %s port %s' % server_address)
        self._sock.connect(server_address)

    def run(self):
        while True:
            self.send_and_receive('DcMotorPositionTimeCtrAll;3000;3000;1')
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;10000;10000;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;10000;15000;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;10000;20000;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;20000;30000;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;0;0;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;10000;10000;1')
            self.read_sensors()
            self.send_and_receive('DcMotorPositionTimeCtrAll;30000;10000;1')
            self.read_sensors()


            self.send_and_receive('getLeftWheelEncoderValue;')
            self.send_and_receive('getRightWheelEncoderValue;')

    def read_sensors(self):
        self.send_and_receive('getIR1;')
        self.send_and_receive('getIR2;')
        self.send_and_receive('getIR3;')
        self.send_and_receive('getIR4;')
        self.send_and_receive('getIR5;')
        self.send_and_receive('getIR6;')
        self.send_and_receive('getIR7;')


        self.send_and_receive('getSonar1;')
        self.send_and_receive('getSonar2;')
        self.send_and_receive('getSonar3;')

    def send_and_receive(self,message):
        print('sending %s' % message)
        self._sock.sendall(message.encode('utf8'))

        data = self._sock.recv(1024)
        print('received {}'.format(data))

        sleep(0.1)


client = Client()
client.run()