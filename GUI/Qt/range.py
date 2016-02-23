# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore

from GUI.Qt import QtHelper as helper
from py import localization as local
from py.configdata import Range as r;
from py.configdata import RecordConfig as rconfig;

lang=local.Local()
_ = helper.get_text_fn(lang)


class Range(QtGui.QDialog):

    def __init__(self):
        super(Range, self).__init__()
        self.setWindowTitle(_("Range"))
        # I don't know where is Qt::WA_TranslucentBackground,but I know the value of it is 120
        self.setAttribute(120);



    def closeEvent(self, QCloseEvent):
       self.x_= self.x()
       self.y_= self.y()

    def get_range(self):
        self.exec_()
        g=self.geometry();
        return rconfig(r(g.x(),g.y(),g.width(),g.height()))




if __name__ == "__main__":
    app=QtGui.QApplication([])
    r=Range()
    r.move(0,20)
    r.show()
    app.exec_()
    print r.frameGeometry()
    print r.geometry()


