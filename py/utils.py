import datetime
import time


class Time:
    """
    Time consumption
    
    """
    def __init__(self):
        self.start_time = Time.__current();
        self.delta = 0
        self.state = "stopped"

    def get(self):
        if self.state == "time":
            s = Time.__current() - self.start_time + self.delta
            m = s / 60
            s = s % 60
            self.last = "{0:02d}:{1:02d}".format(m, s)
            return self.last
        elif self.state == "paused":
            return self.last
        else:
            return "00:00"

    def pause(self):
        self.delta += Time.__current() - self.start_time
        self.state = "paused"

    def start(self):
        self.start_time = Time.__current()
        self.state = "time"

    def reset(self):
        self.delta = 0
        self.state = "stopped"

    def stop(self):
        self.state = "stopped"

    @staticmethod
    def __current():
        now = datetime.datetime.now()
        return now.hour * 3600 + now.minute * 60 + now.second


def __test():
    t = Time()

    while True:
        time.sleep(1)
        print t.get()


if __name__ == "__main__":
    import threading

    threading.Thread(target=__test).start()
    e = threading.Event()
    e.set()
