from abc import ABCMeta,abstractmethod
class IScreenPaintListener:
    @abstractmethod
    def on_paint(self,x,y,w,h):
        pass