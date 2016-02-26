from abc import ABCMeta, abstractmethod
import subprocess
import signal
import logging
import shlex
import lib.event;
import os

"""Screen recorder related classes"""


class ScreenRecorder(object):
    __metaclass__ = ABCMeta

    def __init__(self,program_cfg={},user_cfg={}):
        self.program_cfg=program_cfg
        self.user_cfg=user_cfg
        self._name=""
        if "filter" in program_cfg:
            self.filter=program_cfg["filter"]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        raise Exception("Read-only property")

    @name.deleter
    def name(self):
        raise  Exception("Read-only property")

    def get_cfg(self):
        return self.program_cfg

    def get_user_cfg(self):
        return self.user_cfg

    @abstractmethod
    def start(self, config):
        """
        Start recording
        """
        pass

    @abstractmethod
    def stop(self):
        """Stop recording"""
        pass

    @abstractmethod
    def pause(self):
        """Pause recording"""
        pass

    @abstractmethod
    def restart(self):
        """restart a paused recording process"""
        pass


class ExternalRecorder(ScreenRecorder):
    """
    External program recorder
    This is an abstruct class
    Using external program to record screen and this class's propose is start a
    recording process when start() called ,stop the recording process when stop()
    called and so on.
    Subcless of this must  implements get_command_line_arg() method to provide an
    start up a command line argument string and must implements get_external_program()
    method to provide an path to external program or and external program name within
    environment PATH
    """

    def __init__(self,program_cfg={},user_cfg={}):
        ScreenRecorder.__init__(self,program_cfg,user_cfg)
        self.process = None

    def start(self, config):
        args=[self.get_external_program()]
        cmd=self.get_command_line_arg(config)
        args+=shlex.split(cmd)
        self.process = subprocess.Popen(args)
        logging.info("Started")

    def stop(self):
        if self.process is not None:
            self.process.kill()
            self.process=None
            logging.info("Recorder stopped")

    def pause(self):
        if self.process is not None:
            self.process.send_signal(signal.SIGSTOP)
            logging.info("Recorder paused")

    def restart(self):
        if self.process is not None:
            self.process.send_signal(signal.SIGCONT)
            logging.info("Recorder restarted")

    @abstractmethod
    def get_command_line_arg(self, config):
        pass

    @abstractmethod
    def get_external_program(self):
        pass


class ConfigExternalRecorder(ExternalRecorder):
    """

    """
    def __init__(self,program_cfg={},user_cfg={}):
        self.filter="*.gif"
        super(ConfigExternalRecorder, self).__init__(program_cfg,user_cfg)
        self._name = ""
        self._argument = ""
        self._program= ""



    def load(self, file_name):
        import json
        with open(file_name) as f:
            data = json.load(f)
            if "program" in data:
                self._program=data["program"]
            else:
                raise Exception("Program must set")
            self.__set(data, "name")
            self.__set(data, "argument")

    def __set(self, data, key, w=True):
        if key in data:
            setattr(self, "_"+key, data[key])
        else:
            if w:
                logging.warn("%s not set" % key)

    def get_command_line_arg(self, config):
        return self._argument.format(x=str(config.range.x),
                                     y=str(config.range.y),
                                     width=str(config.range.width),
                                     height=str(config.range.height),
                                     saveto=str(config.saveto))




    def get_external_program(self):
        return self._program

    def __str__(self):
        return self._name if self._name != "" else "(no name)"

class StepRecorder(ScreenRecorder,lib.event.MouseListener):

    def __init__(self,program_cfg={},user_cfg={}):
        ScreenRecorder.__init__(self,program_cfg,user_cfg)
        import autopy
        self.state="waiting"
        self._name="StepRecorder"

    def _on_down(self,event):
        if self.state=="recording":
            import autopy
            autopy.bitmap.capture_screen(self.region).save("%s/%d.png" %(self.tmp_dir,self.idx));
            self.idx+=1

    def _on_up(self,event):
        pass

    def start(self, config):
        self.tmp_dir="step_recorder_tmp"
        os.mkdir(self.tmp_dir)
        self.config=config
        self.state="recording"
        r=self.config.region
        self.region=((r.x,r.y),(r.width,r.height))
        self.idx=0
        if self.state=="waiting":
            pass


    def stop(self):
        """Stop recording"""
        self.state="waiting"


    def pause(self):
        """Pause recording"""
        if self.state=="recording":
            self.state="paused"


    def restart(self):
        """restart a paused recording process"""
        pass
if __name__ == "__main__":
    c = ConfigExternalRecorder()
    c.load("external_program_config/byzanz-record")




    print "OK"


