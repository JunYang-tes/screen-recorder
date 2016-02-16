from abc import ABCMeta, abstractmethod


class IDrawer:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def draw_line(self, pen,p1,p2):
        pass

    @abstractmethod
    def draw_arc(self, pen, rect, start_degree, stop_degree):
        pass

    @abstractmethod
    def fill_arc(self, pen, rect, start_degree, stop_degree):
        pass

    @abstractmethod
    def draw_rect(self, pen, rect):
        pass

    @abstractmethod
    def fill_rect(self, pen, rect):
        pass

    @abstractmethod
    def update(self,rect):
        pass


