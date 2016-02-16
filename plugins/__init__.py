"""
Plugins for screen recorder
"""
from abc import ABCMeta, abstractmethod
import threading

class Plugin(object):
    """
    Plugin for screen recorder
    A plugin can be run while screen recording to doing some thing like hint mouse clicked
    Any plugin run in special thread.
    """
    __metaclass__ = ABCMeta
    def __init__(self,program_cfg={},user_cfg={},run_in_thread=False):
        """
        :param program_cfg:Program configuration which only can be modified by programing
        :param user_cfg: User configuratoin which can be modified by User
        :return:
        """
        self._program_cfg=program_cfg
        self._user_cfg=user_cfg
        self.name="Plugin"
        self.thread_flag=threading.Event()
        self._run_in_thread=run_in_thread
        self._running=False



    def run(self,record_config):
        if self._run_in_thread:
            self.record_config=record_config
            self._plugin_thread=threading.Thread(group=None,target=self._run,name=self._name)
            self._plugin_thread.start()
        else:
            self._run()

    def stop(self):
        self.thread_flag.isSet()
        self._stop()

    def _stop(self):
        self._running=False



    def _run(self):
        """
        override in subclass
        :return:
        """
        """
        :return:
        """
        self._running=True


    def get_cfg(self):
        return self._program_cfg

    def get_user_cfg(self):
        return self._user_cfg

