import EventArgs
import sys
import Interface
mswindows = (sys.platform == "win32")

if mswindows:
    import win32 as platform

linux = (sys.platform.startswith("linux"))
if linux:
    import linux as platform


class MouseListener(object):

    def __init__(self):
        self.__observer = platform.Observer(self.__cb,EventArgs.EventType.MOUSE)
        self.__listen=False

    def __cb(self,event):
        if license is False:
            return ;
        if event.event_type==EventArgs.EventType.MOUSE_DOWN:
            self._on_down(event)
        elif event.event_type==EventArgs.EventType.MOUSE_UP:
            self._on_up(event)
        elif event.event_type==EventArgs.EventType.MOUSE_MOVE:
            self._on_move(event)
        elif event.event_type==EventArgs.EventType.MOUSE_WHEEL:
            self._on_wheel(event)
    def start_listen(self):
        self.__listen=True;
    def stop_listen(self):
        self.__listen=False

    def _on_move(self,event):
        """
        event is an instance of MouseMoveEvent
        """
        pass

    def _on_down(self,event):
        """
        event is an instance of MouseButtonEvent
        """
        print event

    def _on_up(self,event):
        """
        event is an instance of MouseButtonEvent
        :param event:
        :return:
        """
        print event

    def _on_down(self,event):
        print event

    def _on_wheel(self,event):
        print event

class KeyboardListener(object):
    def __init__(self):
        self.__observer=platform.Observer(self.__cb,EventArgs.EventType.KEYBOARD)
    def __cb(self,event):
        if event.key_down:
            self._on_key_down(event)
        else:
            self._on_key_up(event)

    def _on_key_down(self,event):
        print event
    def _on_key_up(self,event):
        print event

class ScreenPaintListener(Interface.IScreenPaintListener):
    def __init__(self):
        self.__impl=platform.ScreenPaintListener()
    def on_paint(self,x,y,w,h):
        pass
if __name__ =="__main__":
    KeyboardListener()
    input()