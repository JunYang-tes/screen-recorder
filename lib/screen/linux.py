import Interface
from Xlib import display,X
class ScreenDrawer(Interface.IDrawer):
    def __init__(self):
        self._d=display.Display()
        self._screen=self._d.screen()
        self._win=self._screen.root
        self._colormap = self._screen.default_colormap
    def __get_gc(self,pen):
        # I don't know the relations between RGB and Xlib's color
        # but in my machine the following codes are working
        # how to apply Alpha channel?
        color=self._colormap.alloc_color(pen.r*256,pen.g*256,pen.b*256)
        gc = self._win.create_gc(
            line_width=pen.width,
            foreground = color.pixel,
            function=X.GXand,
            subwindow_mode = X.IncludeInferiors)
        return gc

    def fill_arc(self,pen,rect,start_degree,stop_degree):
        gc=self.__get_gc(pen)
        self._win.fill_arc(gc,rect.x,rect.y,rect.width,rect.height,start_degree*64,stop_degree*64)
        self._d.flush()

    def draw_arc(self,pen,rect,start_degree,stop_degree):
        gc=self.__get_gc(pen)
        self._win.arc(gc,rect.x,rect.y,rect.width,rect.height,start_degree*64,stop_degree*64)
        self._d.flush()

    def draw_line(self,Pen):
        pass

    def draw_rect(self, pen, rect):
        pass

    def fill_rect(self, pen, rect):
        pass

    def update(self,rect):
        #how to tell system (X11) to redraw (or update ,repaint) some special area?
        #like Update() method in C#
        #XClearArea
        self._win.clear_area(0,0,1,1,True)
        self._d.flush()
        pass

if __name__ =="__main__":
    d=ScreenDrawer()
    import Drawer
    p=Drawer.Pen(255,0,0)
    d.draw_arc(p,Drawer.Rect(0,0,20,20),0,360)
    input()
