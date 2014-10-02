from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt, QSignalMapper, QSettings
from math import radians
from collections import OrderedDict
from traceback import format_exception
import sys
import global_val


class ServerDock(QtGui.QDockWidget):

    robot_changed = pyqtSignal(str,float,float,float)
    apply_robot_settings = pyqtSignal(float,float,float)
    start_server_request = pyqtSignal(str,str)
    closed = pyqtSignal(bool)
    show_server_log = pyqtSignal(bool)

    btn_default_stylesheet = """background-color: rgb(216, 229, 226);
                                border: 1px solid black;
                                text-align: left;
                                padding: 10px;"""
    btn_complete_stylesheet= """background-color: rgb(60, 255, 60);
                                border: 1px solid black;
                                text-align: left;
                                padding: 10px;"""
    btn_error_stylesheet   = """background-color: rgb(255, 60, 60);
                                border: 1px solid black;
                                text-align: left;
                                padding: 10px;"""

    def __init__(self, parent):
        """Construct a new dockwindow following the tester """


        QtGui.QDockWidget.__init__(self,'Server', parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        if not self.widget():
            self.setWidget(QtGui.QWidget(self))

        vl = QtGui.QVBoxLayout(self.widget())
        #self.widget().setLayout(vl)
        communicationGroup = QtGui.QGroupBox("Communication");
        communicationPanel = QtGui.QFrame(self)
        vl.addWidget(communicationPanel)
        vl.addWidget(communicationGroup)

        self.ipAddress = QtGui.QLineEdit('127.0.0.1',self)
        self.port = QtGui.QLineEdit('10001',self)
        self.btn_start = QtGui.QPushButton('Start server',self)
        self.btn_start.clicked.connect(self.start_server_clicked)
        self.ckBox_show_server_log = QtGui.QCheckBox('Display server log messages.',self)
        self.ckBox_show_server_log.setCheckState(True)
        self.ckBox_show_server_log.setTristate(False)
        self.ckBox_show_server_log.clicked.connect(self.show_server_log_clicked)

        fl = QtGui.QFormLayout(communicationPanel)
        fl.addRow('&IP Address:',self.ipAddress)
        fl.addRow('&Port:',self.port)
        fl.addRow(self.btn_start)
        fl.addRow(self.ckBox_show_server_log)
        communicationPanel.setLayout(fl)
        communicationGroup.setLayout(fl)

        self.robotsGroup = QtGui.QGroupBox("Robots");
        robotsPanel = QtGui.QFrame(self)

        self.xPoz = QtGui.QLineEdit("-1",parent)
        self.yPoz = QtGui.QLineEdit("-1",parent)
        self.irSigma = QtGui.QLineEdit(str(global_val.ir_sigma_deviation),parent)
        self.sonarSigma = QtGui.QLineEdit(str(global_val.sonar_sigma_deviation),parent)

        self.phi = QtGui.QSpinBox(parent)
        self.phi.setMinimum(0)
        self.phi.setMaximum(360)
        self.phi.setValue(0)
        self.btn_apply = QtGui.QPushButton('Apply settings',self)
        self.btn_apply.clicked.connect(self.apply_robot_settings_clicked)
        self.cb_robots = QtGui.QComboBox(self)
        self.cb_robots.addItems(["x80", "x80H", "i90", "DRK8080"])
        fl = QtGui.QFormLayout(robotsPanel)
        fl.addRow('Selected robot:',self.cb_robots)
        fl.addRow('X:',self.xPoz)
        fl.addRow('Y:',self.yPoz)
        fl.addRow('Orientation:',self.phi)
        fl.addRow('IR sigma deviation:',self.irSigma)
        fl.addRow('Sonar sigma deviation:',self.sonarSigma)
        fl.addRow(self.btn_apply)
        robotsPanel.setLayout(fl)
        self.robotsGroup.setLayout(fl)
        vl.addWidget(robotsPanel)
        vl.addWidget(self.robotsGroup)
        self.cb_robots.currentIndexChanged.connect(self.selected_robot_changed)
        vl.addStretch(1)

    def selected_robot_changed(self):
        self.robot_changed.emit(str(self.cb_robots.currentText()),float(self.xPoz.text()),float(self.yPoz.text()),radians(float(self.phi.text())))

    def apply_robot_settings_clicked(self):
        global_val.ir_sigma_deviation = float(self.irSigma.text())
        global_val.sonar_sigma_deviation = float(self.sonarSigma.text())
        self.apply_robot_settings.emit(float(self.xPoz.text()),float(self.yPoz.text()),radians(float(self.phi.text())))

    def start_server_clicked(self):
        #self.btn_start.setEnabled(False)
        self.start_server_request.emit(self.ipAddress.text(),self.port.text())
        if self.robotsGroup.isEnabled():
            self.btn_start.setText("Stop server")
        else:
            self.btn_start.setText("Start server")
        self.robotsGroup.setEnabled(not self.robotsGroup.isEnabled())

    def show_server_log_clicked(self):
        self.show_server_log.emit(self.ckBox_show_server_log.isChecked())

    def closeEvent(self,event):
        super(ServerDock,self).closeEvent(event)
        if event.isAccepted():
            print('closed')
            self.closed.emit(True)
