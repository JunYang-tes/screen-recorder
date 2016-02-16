import os
import logging
import copy
from py import configuration
from py.recorder import ConfigExternalRecorder
from py.recorder import StepRecorder
"""
Recorder Factory
Get all recorders and get special one by name.
"""

__recorders = []
__path = os.path.dirname(__file__)+"/external_program_config"
for f in os.listdir(__path):
    try:
        p_cfg = configuration.cfg.recorder_cfg_item(f)
        u_cfg = configuration.cfg.recorder_user_cfg_item(f)
        c = ConfigExternalRecorder(p_cfg,u_cfg)
        c.load(__path +"/"+f)
        __recorders.append(c)
    except Exception as e:
        logging.warn("Fail to load recorder : "+f)
        logging.warn(e)
__recorders.append(StepRecorder(configuration.cfg.recorder_cfg_item("StepRecorder"),
                                configuration.cfg.recorder_cfg_item("StepRecorder")))

def get_all_recorder():
    return copy._deepcopy_list(__recorders)

def get_by_name(name):
    for r in __recorders:
        if r.name==name:
            return r
    return None



if __name__=="__main__":
    print get_all_recorder()