from PyQt4 import QtGui,QtCore
from PyQt4 import Qt as qt
import circle
class QtCircle(QtGui.QWidget):
    def __init__(self,radius,width):
        QtGui.QWidget.__init__(self)
        self.connect(self,QtCore.SIGNAL("show_circle"),self.show_)
        self.connect(self,QtCore.SIGNAL("hide_circle"),self.hide)
        self.connect(self,QtCore.SIGNAL("move_circle"),self.move)
        self.setWindowFlags(
            qt.Qt.FramelessWindowHint
            | qt.Qt.WindowStaysOnTopHint
        #    | qt.Qt.Popup
            | qt.Qt.Tool
        )
        self.setAttribute(qt.Qt.WA_X11DoNotAcceptFocus)

        region=QtGui.QRegion(0,0,radius*2,radius*2,QtGui.QRegion.Ellipse)
        region-=QtGui.QRegion(width,width,radius*2-2*width,2*radius-2*width,QtGui.QRegion.Ellipse)
        self.setMask(region)
        self.resize(radius*2,radius*2)

    def show_(self,x,y,r,g,b):
        p=QtGui.QPalette(QtGui.QColor( r,g,b))
        self.move(x,y)
        self.setPalette(p)
        self.show()


class Circle(circle.Circle):
    def __init__(self,radius=20,width=3):
        circle.Circle.__init__(self,radius,width)

        self._circle=QtCircle(radius,width)

    def show_circle(self,x,y,r=255,g=0,b=0):
        try:
            #because we can't modify safely Widget in non-main-loop thread
            #so we delegate main-loop thread to do this for us
            self._circle.emit(QtCore.SIGNAL( "show_circle"),x-self._radius,y-self._radius,r,g,b)
        except:
            pass
    def hide_circle(self):
        try:
            self._circle.emit(QtCore.SIGNAL("hide_circle"))
        except:
            pass
    def move_circle(self,x,y):
        self._circle.emit(QtCore.SIGNAL("move_circle"),x-self._radius,y-self._radius)
