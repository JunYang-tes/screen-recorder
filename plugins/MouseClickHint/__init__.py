import plugins
import lib.event
import lib.screen.Drawer as d
import lib.event.EventArgs



class Plugin(plugins.Plugin,lib.event.MouseListener,lib.event.ScreenPaintListener):
    def __init__(self,program_cfg={},user_cfg={}):
        plugins.Plugin.__init__(self,program_cfg,user_cfg)
        lib.event.MouseListener.__init__(self)
        try:
            lib.event.ScreenPaintListener.__init__(self)
        except:
            import  threading
            t=threading.Thread(target=self.__thread)
            t.setDaemon(True)
            t.start()
        self.drawer=lib.screen.Drawer.ScreenDrawer()
        self.lpen=d.Pen(255,0,0,width=3)
        self.rpen=d.Pen(0,255,0,width=3)
        self.mpen=d.Pen(0,0,255,width=3)
        self.click_region=None
        self.last_event=None
        self.radius=20

    def __thread(self):
        import time
        while True:
            time.sleep(0.1)
            if self.click_region is not None:
                self.on_paint(self.click_region.x,self.click_region.y,self.click_region.width,self.click_region.height)

    def _run(self):
        self.start_listen()
    def _stop(self):
        self.stop_listen()

    def on_paint(self,x,y,w,h):
        rect=d.Rect(x,y,w,h)
        if self.click_region!=None and rect.contains(self.click_region):
            self.__draw(self.last_event.button,self.click_region)

    def __draw(self,button,rect):
        if button==lib.event.EventArgs.MouseButtonEvent.LEFT:
            pen=self.lpen
        elif button==lib.event.EventArgs.MouseButtonEvent.RIGHT:
            pen=self.rpen
        elif button==lib.event.EventArgs.MouseButtonEvent.MIDDLE:
            pen=self.mpen
        print pen

        self.drawer.draw_arc(
                pen,
                rect,
                0,
                360
        )

    def _on_down(self,event):
        self.click_region=d.Rect(event.x-self.radius,event.y-self.radius,self.radius*2,self.radius*2)
        self.last_event=event
        if event.button== lib.event.EventArgs.MouseButtonEvent.LEFT:
            self.__draw(event.button,self.click_region)
        elif event.button==lib.event.EventArgs.MouseButtonEvent.RIGHT:
            self.__draw(event.button,self.click_region)
    def _on_up(self,event):
        self.click_region=None
        self.drawer.update(None)


    def _on_move(self,event):
        pass

    def __thread(self):
        import time
        while True:
            time.sleep(0.1)
            if self.click_region is not None:
                self.on_paint(self.click_region.x,self.click_region.y,self.click_region.width,self.click_region.height)

    def _run(self):
        self.start_listen()
    def _stop(self):
        self.stop_listen()

    def on_paint(self,x,y,w,h):
        rect=d.Rect(x,y,w,h)
        if self.click_region!=None and rect.contains(self.click_region):
            self.__draw(self.last_event.button,self.click_region)

    def __draw(self,button,rect):
        if button==lib.event.EventArgs.MouseButtonEvent.LEFT:
            pen=self.lpen
        elif button==lib.event.EventArgs.MouseButtonEvent.RIGHT:
            pen=self.rpen
        elif button==lib.event.EventArgs.MouseButtonEvent.MIDDLE:
            pen=self.mpen

        self.drawer.draw_arc(
                pen,
                rect,
                0,
                360
        )

    def _on_down(self,event):
        self.click_region=d.Rect(event.x-self.radius,event.y-self.radius,self.radius*2,self.radius*2)
        self.last_event=event
        if event.button== lib.event.EventArgs.MouseButtonEvent.LEFT:
            self.__draw(event.button,self.click_region)
        elif event.button==lib.event.EventArgs.MouseButtonEvent.RIGHT:
            self.__draw(event.button,self.click_region)
    def _on_up(self,event):
        self.click_region=None

    def _on_move(self,event):
        pass


if __name__ == "__main__":
    Plugin({},{})
    input()