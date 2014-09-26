from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt, QSignalMapper, QSettings
from helpers import Struct
from collections import OrderedDict
from traceback import format_exception
import sys


class ServerDock(QtGui.QDockWidget):

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

        panel = QtGui.QFrame(self)
        vl.addWidget(panel)

        self.ipAddress = QtGui.QLineEdit('127.0.0.1',self)
        self.port = QtGui.QLineEdit('10001',self)
        self.btn_start = QtGui.QPushButton('Start server',self)
        self.btn_start.clicked.connect(self.start_server_clicked)
        self.ckBox_show_server_log = QtGui.QCheckBox('Display server log messages.',self)
        self.ckBox_show_server_log.setCheckState(True)
        self.ckBox_show_server_log.setTristate(False)
        self.ckBox_show_server_log.clicked.connect(self.show_server_log_clicked)

        fl = QtGui.QFormLayout(panel)
        fl.addRow('&IP Address:',self.ipAddress)
        fl.addRow('&Port:',self.port)
        fl.addRow(self.btn_start)
        fl.addRow(self.ckBox_show_server_log)
        panel.setLayout(fl)

        vl.addStretch(1)


    def start_server_clicked(self):
        #self.btn_start.setEnabled(False)
        self.start_server_request.emit(self.ipAddress.text(),self.port.text())

    def show_server_log_clicked(self):
        self.show_server_log.emit(self.ckBox_show_server_log.isChecked())

    def closeEvent(self,event):
        super(ServerDock,self).closeEvent(event)
        if event.isAccepted():
            print('closed')
            self.closed.emit(True)
