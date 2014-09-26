import sys
import threading
from server import Server
import sim_server_helpers

try:
    import Queue as queue
except ImportError:
    import queue

class SimServer:

    helpers = sim_server_helpers
    def __init__(self, robot,  tracker, log_queue, simParent):
        self._robot = robot

        self._tracker = tracker
        self._logqueue = log_queue
        self._out_server_queue = queue.Queue()
        self._server_thread = Server(self._out_server_queue, log_queue)
        self._in_server_queue = self._server_thread.getOutQueue()
        self._simParent = simParent

    def set_server_log(self, show):
        self._server_thread.set_server_log(show)

    def process_queue(self):
        while not self._in_server_queue.empty():
            tpl = self.helpers.buildTuple(self._in_server_queue.get())

            if isinstance(tpl,tuple):
                name, args = tpl
                if name in self.__class__.__dict__:
                    try:
                        if args is None:
                            self.__class__.__dict__[name](self)
                        else:
                            self.__class__.__dict__[name](self,*args)
                    except TypeError as e:
                        self.log("Wrong sim_server event parameters {}{}".format(name,args))
                        raise e
                    except Exception as e:
                        self.log("EXCEPTION: {}".format(sys.exc_info()))
                        raise e

                else:
                    self.log("Unknown sim_server event '{}'".format(name))
            else:
                self.log("Wrong sim_server event format '{}'".format(tpl))


    def run(self, ipAddress, port):
        if not self._server_thread.isAlive():
            self._server_thread.setIpAddress(ipAddress)
            self._server_thread.setPort(int(port))
            self._server_thread.start()
        else:
            self.log("Server is running...")
    time_constant = 0.02 # 20 milliseconds
    def DcMotorPositionTimeCtrAll(self, left_wheel, right_wheel, run_time):
        vl = self.helpers.computeWellRotationSpeed(self._robot, left_wheel, self._robot.info.wheels.left_encoder_ticks, run_time)
        vr = self.helpers.computeWellRotationSpeed(self._robot, right_wheel, self._robot.info.wheels.right_encoder_ticks, run_time)

        self._robot.info.wheels.left_encoder_ticks = left_wheel
        self._robot.info.wheels.right_encoder_ticks = right_wheel
        nrRuns = int(run_time/self.time_constant)

        for x in range(0, nrRuns):
            self._robot.set_inputs((vl,vr))
            self._robot.move(self.time_constant)
            self._tracker.add_point(self._robot.get_pose())
            self._simParent.check_collisions()
            self._simParent.draw()

        self._out_server_queue.put("Done.")

    def get_ir_senfor_readings(self, ir_sensor_id):
        info = self._robot.get_info()
        return info.ir_sensors.readings[ir_sensor_id]

    def getLeftWellEncoderValue(self):
        info = self._robot.get_info()
        self._out_server_queue.put(info.wheels.left_ticks)

    def getRightWellEncoderValue(self):
        info = self._robot.get_info()
        self._out_server_queue.put(info.wheels.right_ticks)

    def getIR1(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(0))

    def getIR2(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(1))

    def getIR3(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(2))

    def getIR4(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(3))

    def getIR5(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(4))

    def getIR6(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(5))

    def getIR7(self):
        self._out_server_queue.put(self.get_ir_senfor_readings(6))


    def log(self, message):
        print("{}: {}".format(self.__class__.__name__,message))
        if self._logqueue is not None:
            self._logqueue.append((self,message))