import plugins
import lib.event
import Qt
import lib.event.EventArgs as event_args


class Plugin(plugins.GlobalSingletonPlugin, lib.event.MouseListener):

    def __init__(self,program_cfg={},user_cfg={}):
        plugins.GlobalSingletonPlugin.__init__(self, "MouseClickHint", program_cfg, user_cfg)
        self.name="MouseClickHint"
        lib.event.MouseListener.__init__(self)
        self.start_listen()
        self.__circle=Qt.Circle(20,3)

    def _on_up(self,event):
        self.__circle.hide_circle()

    def _on_down(self,event):
        if self._running:
            r=255 if event.button ==event_args.MouseButtonEvent.LEFT else 0
            g=255 if event.button == event_args.MouseButtonEvent.MIDDLE else 0
            b=255 if event.button == event_args.MouseButtonEvent.RIGHT else 0
            self.__circle.show_circle(event.x,event.y,r,g,b)

    def _on_move(self,event):
        if self._running:
            self.__circle.move_circle(event.x,event.y)

if __name__=="__main__":
    from PyQt4 import QtGui
    app=QtGui.QApplication([])
    Plugin().run(None)
    app.exec_()