from PyQt4 import QtGui, QtCore
import py.localization as local
import QtHelper as helper
import py.localization as local
import py.RecorderFactory as RecorderFactory
import GUI.GUIFactory as GUIFactory
from py import recorder
import py.configuration as cfg

lang = local.Local()
_ = helper.get_text_fn(lang)


def _fromUtf8(string):
    return string


def _translate(_1, string, _2):
    return _(string)


class Config(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self._init_combox(self.cb_language,
                          local.get_all_languages(),
                          lambda t: t[1],
                          lambda t: True if t[0] == cfg.cfg.get("language") else False
                          )
        self._init_combox(self.cb_recorder,
                          RecorderFactory.get_all_recorder(),
                          lambda t: None if isinstance(t, recorder.StepRecorder) else str(t),
                          lambda t: True if t.name == cfg.cfg.recorder.name else False
                          )
        self._init_combox(self.cb_gui, GUIFactory.get_all_gui(),
                          select_this=lambda t: True if t == cfg.cfg.get("GUI") else False
                          )

    def _init_combox(self, cb, itrable, strfn=str, select_this=None):
        idx = 0
        select = 0
        for v in itrable:
            string = strfn(v)
            if string is not None:
                string = _(string)
                data = QtCore.QVariant(v)
                cb.addItem(string, v)
            if select_this(v):
                select = idx
            idx += 1
        cb.setCurrentIndex(select)


    def closeEvent(self, QCloseEvent):
        data = self.cb_language.itemData(self.cb_language.currentIndex()).toPyObject()
        cfg.cfg.set("language", data[0])
        local.set_location(data[0])

        data = self.cb_recorder.itemData(self.cb_recorder.currentIndex()).toPyObject()
        cfg.cfg.recorder = data
        cfg.cfg.set("screen_recorder", data.name)

        data = self.cb_gui.itemData(self.cb_gui.currentIndex()).toPyObject()
        data = str(data)  # I dont know why data is an instance of QString now
        cfg.cfg.set("GUI", data)

        cfg.cfg.save()


    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(372, 179)
        Form.setWindowTitle(_fromUtf8("Config"))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.cb_recorder = QtGui.QComboBox(self.tab)
        self.cb_recorder.setObjectName(_fromUtf8("cb_recorder"))
        self.gridLayout.addWidget(self.cb_recorder, 0, 1, 1, 1)
        self.cb_gui = QtGui.QComboBox(self.tab)
        self.cb_gui.setObjectName(_fromUtf8("cb_gui"))
        self.gridLayout.addWidget(self.cb_gui, 1, 1, 1, 1)
        self.cb_language = QtGui.QComboBox(self.tab)
        self.cb_language.setObjectName(_fromUtf8("cb_language"))
        self.gridLayout.addWidget(self.cb_language, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8("Global"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.label_2.setText(_translate("Form", "Language", None))
        self.label.setText(_translate("Form", "Recorder", None))
        self.label_3.setText(_translate("Form", "GUI", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Recorders", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Plugins", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "GUI", None))


if __name__ == "__main__":
    app = QtGui.QApplication([])
    Config().exec_()
    app.exec_()
