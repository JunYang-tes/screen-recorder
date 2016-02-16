import os
import logging

__plugins={}
__plugin_names=[]

def __get_all():
    path=os.path.dirname(__file__)
    for i in os.listdir(path):
        if os.path.isdir(path+"/"+i):
            m=vars(__import__("plugins."+i))
            try:
                __plugins[i]=m.get(i).Plugin
                __plugin_names.append(i)
            except:
                pass
    """
    m=vars(__import__("plugins"))
    for k in m:
        #how to determin if m[k] is instance of module ? isinstance(m[k],what?)
        if str(type(m[k]))=="<type 'module'>" and m[k].__name__.startswith("plugins"):
        #if isinstance(m[k],Module) and m[k].__name__.startswith("plugins"):
            if k in __plugins:
                logging.WARN("duplicated plugin:"+k)
            else:
                __plugins[k]=m[k]
                __plugin_names.append(k)
    """


def get_plugin_instance(name,program_cfg={},user_cfg={}):
    if name in __plugins:
        return __plugins[name](program_cfg,user_cfg)

def get_all_plugin():
    ret=[]
    return ret+__plugin_names

__get_all()