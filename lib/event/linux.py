try:
    from Xlib import X, XK, display
    from Xlib.ext import record
    from Xlib.protocol import rq
except:
    raise Exception("python-xlib not found")

import EventArgs
import threading

class Observer(EventArgs.Observer):

    def __init__(self,cb,event_type=EventArgs.EventType.MOUSE | EventArgs.EventType.KEYBOARD):
        #super(Observer, self).__init__(cb)
        EventArgs.Observer.__init__(self,cb)
        self.event_type=event_type
        self.display = display.Display()
        if not self.display.has_extension("RECORD"):
            raise Exception("RECORD extension not found")
        self.ctx=self.display.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])
        th=threading.Thread(target=self.__thread_method)
        th.setDaemon(True)
        th.start()

    def __this_cb(self,reply):
        if self.event_handler_cb is None:
            return
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            return
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)

            if event.type == X.KeyPress and self.event_type & EventArgs.EventType.KEYDOWN:
                key=self.display.keycode_to_keysym(event.detail,0)
                if key:
                    key_str=Observer.lookup_key_str(key)
                    self.event_handler_cb(EventArgs.Keyboard(key_str,True))
            elif event.type == X.KeyRelease and self.event_type & EventArgs.EventType.KEYUP:
                key=self.display.keycode_to_keysym(event.detail,0)
                if key:
                    key_str=Observer.lookup_key_str(key)
                    self.event_handler_cb(EventArgs.Keyboard(key_str,False))
            elif event.type == X.ButtonPress and self.event_type & EventArgs.EventType.MOUSE_DOWN:
                if event.detail!=4 and event.detail!=5 : # 4 or 5 means wheel
                    self.event_handler_cb(
                        EventArgs.MouseButtonEvent(
                            event.root_x,
                            event.root_y,
                            event.detail,True))
            elif event.type == X.ButtonRelease and self.event_type & EventArgs.EventType.MOUSE_UP:
                if event.detail!=4 and event.detail!=5 : # 4 or 5 means wheel
                    self.event_handler_cb(
                        EventArgs.MouseButtonEvent(
                            event.root_x,event.root_y,event.detail,False))
                elif event.detail==4:
                    self.event_handler_cb(EventArgs.MouseWheelEvent(event.root_x,event.root_y,EventArgs.MouseWheelEvent.UP))
                elif event.detail==5:
                    self.event_handler_cb(EventArgs.MouseWheelEvent(event.root_x,event.root_y,EventArgs.MouseWheelEvent.DOWN))
            elif event.type == X.MotionNotify and self.event_type & EventArgs.EventType.MOUSE_MOVE:
                self.event_handler_cb(EventArgs.MouseMoveEvent(event.root_x,event.root_y))

    @staticmethod
    def lookup_key_str(key_code):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == key_code:
                return name[3:]
        return  "Unknow"

    def __thread_method(self):
        self.display.record_enable_context(self.ctx, self.__this_cb)

    def __del__(self):
        self.display.record_free_context(self.ctx)
import Interface
class ScreenPaintListener(Interface.IScreenPaintListener):
    def __init__(self):
        raise Exception("Not implement")
    def on_paint(self,x,y,w,h):
        pass