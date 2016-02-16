# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
from PyQt4 import Qt as qt
import os
import threading
import py.localization as l
_=l.Local()._

class RecordControl(QtGui.QDialog):
    def __init__(self):
        super(RecordControl,self).__init__()
        """
        state can be:
        wait_start
        recording
        paused
            -----------------------------
            ↓               |           |
        wait_start ---> recording ---> paused
                            ↑           |
                            -------------
        """
        self.state="wait_start"
        self.setupUi(self)
        self.setAttribute(262144)#qt.Qt.WindowStaysOnTopHint)
        

    def exec_(self):
        self.start_time_report()
        super(RecordControl, self).exec_()


        
    def setupUi(self, Dialog):
        Dialog.setObjectName(_("Dialog"))
        Dialog.resize(243, 47)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName(_("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_("label"))
        self.horizontalLayout.addWidget(self.label)
        self.btn_start = QtGui.QPushButton(Dialog)
        self.btn_start.setObjectName(_("btn_start"))
        self.horizontalLayout.addWidget(self.btn_start)
        self.btn_pause = QtGui.QPushButton(Dialog)
        self.btn_pause.setObjectName(_("btn_pause"))
        self.horizontalLayout.addWidget(self.btn_pause)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.connectSlot()
    
    def connectSlot(self):
        self.connect(self.btn_start, QtCore.SIGNAL("clicked()"),self.btn_start_click)
        self.connect(self.btn_pause, QtCore.SIGNAL("clicked()"),self.btn_pause_click)

    def btn_start_click(self):
        if self.state == "wait_start":
            if os.path.exists(self.config.saveto):
                os.remove(self.config.saveto)
            self.time.reset()
            self.time.start()
            self.on_start(self.config)
            self.state="recording"
            self.setWindowTitle(_("Recording"))
            self.btn_start.setText(_("Stop"))
        else:
            self.__stop()
            #self.time.stop()
            #self.on_stop()
            #self.setWindowTitle(_("Record Control"))
            #self.btn_start.setText(_("Start"))
            #self.state="wait_start"
    def __stop(self):
        self.time.stop()
        self.on_stop()
        self.setWindowTitle(_("Record Control"))
        self.btn_start.setText(_("Start"))
        self.state="wait_start"
    def btn_pause_click(self):
        print "test"
        if self.state == "recording":
            #pase
            self.on_pause()
            self.state="paused"
            self.time.pause()
            self.setWindowTitle(_("Paused"))
            self.btn_pause.setText(_("Restart"))
        elif self.state=="paused":
            #restart
            self.on_restart()
            self.state="recording"
            self.time.start()
            self.setWindowTitle(_("Recording"))
            self.btn_pause.setText(_("Pause"))

    def set_on_start(self,fun):
        self.on_start=fun

    def set_on_stop(self,fun):
        self.on_stop=fun

    def set_on_pause(self,fun):
        self.on_pause=fun

    def set_on_restart(self,fun):
        self.on_restart=fun

    def set_config(self,config):
        self.config=config

    def closeEvent(self,e):
        if self.thread_stop is not None:
            self.thread_stop.set()
        self.x_=self.frameGeometry().x()
        self.y_=self.frameGeometry().y()
        if self.state=="recording":
            self.__stop()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_("Record Control"))
        self.label.setText("00:00")
        self.btn_start.setText(_("Start"))
        self.btn_pause.setText(_("Pause"))

    def start_time_report(self):
        self.thread_stop=threading.Event()
        self.timer_thread=threading.Thread(target=self.time_report,name="Time-Report")
        self.timer_thread.setDaemon(False)
        self.timer_thread.start()


    def time_report(self):
        import py.utils as utils
        import time;
        t=utils.Time()
        self.time=t
        while not self.thread_stop.isSet():
            time.sleep(1)
            self.label.setText(t.get())
        print "report thread stopped"


