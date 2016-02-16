import os
import py.localization as l
_=l.Local()._;

guiImpl = "Qt"


def setGUIImpl(impl="Qt"):
    path=os.path.dirname(__file__)
    if not os.path.exists(path+"/"+impl) and not os.path.exists(impl+"/check.py"):
        raise Exception(_("No such GUI implication :"+impl))
    if getStaticFunction(_("Check"),"check")() is False:
        raise Exception(_("GUI implication check not pass"))

def getClass(className):
    module_name=(className[0].lower())+ className[1:]
    m=vars(__import__("GUI."+guiImpl+"."+module_name))
    quiImplm=vars(m.get(guiImpl))
    class_module=vars(quiImplm.get(module_name))
    return class_module.get(className)

def getStaticFunction(class_,fun):
    if isinstance(class_,str):
        class_=getClass(class_)
    if class_ is None:
        raise Exception("No such class")
    f=vars(class_).get(fun)
    if f is None:
        raise Exception("No such function")
    if not isinstance(f,staticmethod):
        raise  Exception(fun +" is not a static method")

    return vars(class_).get(fun).__func__


def getInstance(className="",*args,**kwargs):
    return getClass(className)(*args,**kwargs)

def get_all_gui():
    ret=[]
    path=os.path.dirname(__file__)
    for f in os.listdir(path):
        ret.append(f)
    return ret

