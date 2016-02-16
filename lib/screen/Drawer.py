import sys
import Interface

__mswindows = (sys.platform == "win32")

if __mswindows:
    import win32 as platform

__linux = (sys.platform.startswith("linux"))
if __linux:
    import linux as platform

class Pen:
    def __init__(self,r=255,g=255,b=255,a=255,width=1):
        self.width=width
        self.r=r
        self.g=g
        self.b=b
        self.a=a
    def __str__(self):
        return "(%d %d %d %d)" %(self.a,self.r,self.g,self.b)

class Rect:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def contains(self,rect):
        """
        Determinate a rectangle is contained in this rectangle
        :param rect:
        :return:
        """
        if rect.x>= self.x and rect.y>=self.y and rect.width<=self.width and rect.height<=self.height:
            return True
        return False
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return "(%d,%d)" %(self.x,self.y)



class ScreenDrawer(Interface.IDrawer):
    def __init__(self):
        self.__impl=platform.ScreenDrawer()
        pass;
    def draw_line(self,pen,p1,p2):
        self.__impl.draw_line(pen,p1,p2)
    def draw_arc(self,pen,rect,start_degree,stop_degree):
        self.__impl.draw_arc(pen,rect,start_degree,stop_degree)

    def fill_arc(self, pen, rect, start_degree, stop_degree):
        self.__impl.fill_arc(pen,rect,start_degree,stop_degree)


    def draw_rect(self, pen, rect):
        self.__impl.draw_rect(pen,rect)


    def fill_rect(self, pen, rect):
        self.__impl.fill_rect(pen,rect)

    def update(self,rect):
        pass
