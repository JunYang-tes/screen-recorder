# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, Qt

from GUI.Qt import QtHelper as helper
from py import localization as local
from py.configdata import Range as r;
from py.configdata import RecordConfig as rconfig;
import os
import recording
import GUI.Qt.range
import config

lang = local.Local()
_ = helper.get_text_fn(lang)


class Main(QtGui.QMainWindow):
    def __init__(self, cfg={}, user_cfg={}):
        self._app = QtGui.QApplication([])
        super(Main, self).__init__()
        self.cfg = cfg
        self.user_cfg = user_cfg
        self.__folder = ""
        self.setupUi(self)
        self._record_control = recording.RecordControl()
        self._range = GUI.Qt.range.Range()
        self.connect(self.btn_saveto, QtCore.SIGNAL("clicked()"), self.select_save_to)
        self.connect(self.menuConfig, QtCore.SIGNAL("clicked()"), lambda: config().exec_())
        self._saveto = "out.gif";
        self.__restore()
        self.get_filter = None
        self.is_step_recorder = False

    def __restore(self):
        try:
            if "RecorderControl" in self.cfg:
                d = self.cfg["RecorderControl"]
                self._record_control.move(d['x'], d['y'])
            if "Range" in self.cfg:
                d = self.cfg["Range"]
                self._range.move(d['x'], d['y'])
                self._range.setBaseSize(d['w'], d['h'])
            if "Main" in self.cfg:
                d = self.cfg["Main"]
                self.__folder = d["Main"]
        except:
            pass

    def __save(self):
        d = self.cfg["RecorderControl"] = {}
        d["x"] = self._record_control.pos().x()
        d["y"] = self._record_control.pos().y()
        d = self.cfg["Range"] = {}
        # d['x']=self._range.x()
        # d['y']=self._range.y()
        # d['y']=self._range.frameGeometry().y()
        d['x'] = self._range.pos().x()
        d['y'] = self._range.pos().y()
        d['w'] = self._range.width()
        d['h'] = self._range.height()
        d = self.cfg["Main"] = {}
        d["folder"] = self.__folder

    @property
    def saveto(self):
        return self._saveto

    @saveto.setter
    def saveto(self, value):
        self._saveto = value
        self.lineEdit.setText(value)

    def closeEvent(self, e):
        self.__save()

    def set_on_start(self, func):
        self._record_control.set_on_start(func)

    def set_on_stop(self, func):
        self._record_control.set_on_stop(func)

    def set_on_pause(self, func):
        self._record_control.set_on_pause(func)

    def set_on_restart(self, fun):
        self._record_control.set_on_restart(fun)

    def set_get_filter_fn(self, fun):
        self.get_filter = fun

    def get_cfg(self):
        return self.cfg

    def get_user_cfg(self):
        return self.user_cfg

    def run(self):
        self.show()
        return self._app.exec_()

    def select_save_to(self):
        fd = QtGui.QFileDialog()
        filter = "*.*"
        if callable(self.get_filter):
            filter = self.get_filter(self.is_step_recorder);

        save_to = fd.getSaveFileName(self, _("Save to"), self.__folder, filter)
        # save_to=QtGui.QFileDialog.getSaveFileName(QWidget_parent=None,QString_caption= _("Save"),self.__folder)
        if save_to != "":
            save_to = str(save_to)
            suffix = save_to[save_to.rfind("."):]
            suffix_list = [x[x.rfind('.'):] for x in filter.split("|")]
            if suffix not in suffix_list:
                save_to += suffix_list[0]
            self.saveto = save_to

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_("MainWindow"))
        MainWindow.resize(443, 175)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_("horizontalLayout_3"))
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setObjectName(_("mainlayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_("horizontalLayout"))
        self.label_saveto = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_saveto.sizePolicy().hasHeightForWidth())
        self.label_saveto.setSizePolicy(sizePolicy)
        self.label_saveto.setObjectName(_("label_saveto"))
        self.horizontalLayout.addWidget(self.label_saveto)
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setObjectName(_("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btn_saveto = QtGui.QPushButton(self.tab)
        self.btn_saveto.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_saveto.sizePolicy().hasHeightForWidth())
        # buttons
        self.btn_saveto.setSizePolicy(sizePolicy)
        self.btn_saveto.setObjectName(_("btn_saveto"))
        self.horizontalLayout.addWidget(self.btn_saveto)
        self.btn_get_region = QtGui.QPushButton(self.tab)
        self.btn_get_region.setObjectName(_("btn_get_region"))
        self.btn_fullscreen = QtGui.QPushButton(self.tab)
        self.btn_fullscreen.setObjectName(_("btn_fullscreen"))
        self.horizontalLayout.addWidget(self.btn_get_region)
        self.horizontalLayout.addWidget(self.btn_fullscreen)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, _(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_("tab_2"))
        self.tabWidget.addTab(self.tab_2, _(""))
        self.mainlayout.addWidget(self.tabWidget)
        self.horizontalLayout_3.addLayout(self.mainlayout)
        self.tabWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 443, 24))
        self.menubar.setObjectName(_("menubar"))
        self.menuConfig = QtGui.QMenu(self.menubar)
        self.menuConfig.setObjectName(_("menuConfig"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_("actionAbout"))
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connect(self.btn_get_region, QtCore.SIGNAL("clicked()"), self.get_region_clicked)
        self.connect(self.btn_fullscreen, QtCore.SIGNAL("clicked()"), self.fullscreen)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_("Recorder"))
        self.label_saveto.setText(_("Save to"))
        self.btn_saveto.setText(_("..."))
        self.btn_get_region.setText(_("get region"))
        self.btn_fullscreen.setText(_("full screen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("Screen recorder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Step recorder"))
        self.menuConfig.setTitle(_("Config"))
        self.menuHelp.setTitle(_("Help"))
        self.actionAbout.setText(_("About"))

    def get_region_clicked(self):
        self.hide()
        self.__restore()
        self.record_config = self._range.get_range()
        file_name = str(self.lineEdit.text())
        if file_name != "":
            self.record_config.saveto = file_name
            self.__folder = os.path.dirname(file_name)
        else:
            filter = self.get_filter(self.is_step_recorder)
            suffix = filter.split("|")[0]
            suffix = suffix[suffix.rfind("."):]
            self.record_config.saveto = "out" + suffix
        self._record_control.set_config(self.record_config)
        self._record_control.exec_()
        self.__save()
        self.show()

    def fullscreen(self):
        self.hide()
        self.__restore()
        desktop = QtGui.QDesktopWidget()
        self.record_config = rconfig(r(0, 0, desktop.width(), desktop.height()))
        file_name = str(self.lineEdit.text())
        if file_name != "":
            self.record_config.saveto = file_name
            self.__folder = os.path.dirname(file_name)
        self._record_control.set_config(self.record_config)
        self._record_control.exec_()
        self.__save()
        self.show()


if __name__ == "__main__":
    # app = QtGui.QApplication([])
    win = Main()
    # win.show()
    # app.exec_()
