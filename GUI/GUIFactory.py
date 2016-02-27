import os
import py.localization as l
_=l.Local()._;

guiImpl = "Qt"


def checkImpl(impl):
    path = os.path.dirname(__file__)
    if not os.path.exists(path + "/" + impl) and not os.path.exists(impl + "/check.py"):
        return False
    try:
        if getStaticFunction("Check", "check", impl)() is False:
            return False
    except ImportError:
        return False
    return True

def setGUIImpl(impl="Qt"):
    if checkImpl(impl):
        guiImpl = "Qt"
    else:
        raise Exception(_("No such GUI implication or check not pass"))
        # path=os.path.dirname(__file__)
        # if not os.path.exists(path+"/"+impl) and not os.path.exists(impl+"/check.py"):
        #    raise Exception(_("No such GUI implication :") + impl)
        # if getStaticFunction("Check", "check")() is False:
        #   raise Exception(_("GUI implication check not pass"))


def getClass(className,impl=guiImpl):
    module_name= (className[0].lower()) + className[1:]
    m = vars(__import__("GUI." + impl + "." + module_name))
    quiImplm = vars(m.get(impl))
    class_module=vars(quiImplm.get(module_name))
    return class_module.get(className)


def getStaticFunction(class_, fun,impl=guiImpl):
    if isinstance(class_, str):
        class_ = getClass(class_,impl)
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
        if os.path.isdir(path + "/" + f):
            if checkImpl(f):
                ret.append(f)
    return ret

