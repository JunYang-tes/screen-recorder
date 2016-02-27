# --coding:utf-8--
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
            | qt.Qt.Popup
            #    | qt.Qt.Tool
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


class _circle_app:
    def __init__(self, r, w):
        """
        最开始打算用xlib在屏幕上绘制圆圈，但是没有找到类似Win32 API中的invalidateRect这样的函数
        因此绘制到屏幕上的圆圈不能由“我”在适当的时候“擦掉”。虽然可以通过在绘制前复制那个区域的屏幕，
        但是因为嫌麻烦而放弃了。
        然会考虑的时候直接有原型的窗口来显示这个圆圈。虽然这个圆圈窗口已经设置为不捕获输入焦点，但是
        圆圈显示的时候应用中的其他程序却要抢占输入焦点，导致其他程序不能正常的获得键盘输入。
        因此考虑这种方式，把圆圈放在单独的进程中，相当一个独立的应用，这个应用只有一个圆形窗口，而且
        该窗口设置为不捕获输入焦点。
        插件通过管道和该应用交互
        :param r:
        :param w:
        :return:
        """
        import subprocess
        self.process = subprocess.Popen(args=["python", __file__], shell=False, stdin=subprocess.PIPE)

    def show(self, x, y, r, g, b):
        self.process.stdin.write("show:%d:%d:%d:%d:%d\n" % (x, y, r, g, b))

    def move(self, x, y):
        self.process.stdin.write("move:%d:%d\n" % (x, y))

    def hide(self):
        self.process.stdin.write("hide\n")

    def __del__(self):
        self.process.stdin.write("quit\n")


class Circle(circle.Circle):
    def __init__(self,radius=20,width=3):
        circle.Circle.__init__(self,radius,width)
        self._circle = _circle_app(radius, width)

    def show_circle(self,x,y,r=255,g=0,b=0):
        try:
            self._circle.show(x - self._radius, y - self._radius, r, g, b)
            # self._circle.emit(QtCore.SIGNAL( "show_circle"),x-self._radius,y-self._radius,r,g,b)
        except:
            pass
    def hide_circle(self):
        try:
            self._circle.hide()
        except:
            pass
    def move_circle(self,x,y):
        # self._circle.emit(QtCore.SIGNAL("move_circle"),x-self._radius,y-self._radius)
        self._circle.move(x - self._radius, y - self._radius)


def main():
    app = QtGui.QApplication([])
    circle = QtCircle(20, 3)

    def control():
        while True:
            try:
                s = raw_input().split(":")
            except EOFError:
                app.exit(0)

            if s[0] == "show":
                # because we can't modify safely Widget in non-main-loop thread
                # so we delegate main-loop thread to do this for us
                circle.emit(QtCore.SIGNAL("show_circle"), int(s[1]),  # x
                            int(s[2]),  # y
                            int(s[3]),  # r
                            int(s[4]),  # G
                            int(s[5]))  # b

            elif s[0] == "hide":
                circle.emit(QtCore.SIGNAL("hide_circle"))
            elif s[0] == "move":
                circle.emit(QtCore.SIGNAL("move_circle"), int(s[1]), int(s[2]))
            elif s[0] == "quit":
                print "quit"
                app.exit(0)

    import threading
    thread = threading.Thread(target=control)
    thread.setDaemon(True)
    thread.start()
    app.exec_()


if __name__ == "__main__":
    main()
