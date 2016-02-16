class Event:
    def __init__(self,event_type):
        self.event_type=event_type

class MouseMoveEvent(Event):
    def __init__(self,x,y):
        Event.__init__(self,EventType.MOUSE_MOVE)
        self.x=x
        self.y=y

    def __str__(self):
        return "(%d , %d)" %(self.x,self.y)

class MouseButtonEvent(Event):
    LEFT=1
    MIDDLE=2
    RIGHT=3
    buttons=["","Left","Middle","Right"]
    def __init__(self,x=0,y=0,button=None,down=False):
        if down:
            _event_type=EventType.MOUSE_DOWN
        else:
            _event_type=EventType.MOUSE_UP
        Event.__init__(self,_event_type)
        self.x=x
        self.y=y
        self.button=button

    def __str__(self):
        try:
            return "(%d %d) %s" %(self.x,self.y,MouseButtonEvent.buttons[self.button])
        except:
            return "(%d , %d) %d" %(self.x,self.y,self.button)

class MouseWheelEvent(Event):
    UP=1
    DOWN=2
    directions=["","Up","Down"]
    def __init__(self,x=0,y=0,direction=UP):
        Event.__init__(self,EventType.MOUSE_WHEEL)
        self.direction=direction
        self.x=x
        self.y=y

    def __str__(self):
        return "(%d , %d) %s" %(self.x,self.y,MouseWheelEvent.directions[self.direction])

class Keyboard(Event):
    def __init__(self,key_str,key_down=False):
        Event.__init__(self,EventType.KEYBOARD)
        self.key_str=key_str
        self.key_down=key_down
    def __str__(self):
        return self.key_str + (" down " if self.key_down else " up")

class ScreenPaint(Event):
    def __init__(self,x,y,width,height):
        Event.__init__(self,EventType.SCREENPAINT)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def __str__(self):
        return "(%d %d %d %d)" %(self.x,self.y,self.width,self.height)



class EventType:
    SCREENPAINT=64
    MOUSE=15
    KEYBOARD=48
    KEYDOWN=32
    KEYUP=16
    MOUSE_WHEEL=8
    MOUSE_MOVE=4
    MOUSE_DOWN=2
    MOUSE_UP=1


class Observer:
    def __init__(self,cb):
        """
        :param cb:cb is a callback will be called when event raised
        :return:
        """
        self.event_handler_cb=cb
        print "Observer"