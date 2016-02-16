import os
import json
import logging


class Config:
    def __init__(self):
        path=os.path.dirname(__file__)
        try:
            with open(path+"/config") as f:
                self.cfgdata=json.load(f)
        except Exception as e:
            logging.warn("Fail to load configuration:"+str(e))
            self.__default_cfg()
        try:
            with open(path+"/usercfg") as f:
                self.user_cfg_data=json.load(f)
        except Exception as e:
            logging.warn("Fail to load user configuartion:"+str(e))
            self.__default_user_cfg()


    def __default_user_cfg(self):
        self.user_cfg_data={}
        self.user_cfg_data["gui_config"]={}
        self.user_cfg_data["plugin_config"]={}
        self.user_cfg_data[""]

    def __default_cfg(self):
        self.cfgdata={}
        self.cfgdata["gui"]="Qt"
        self.cfgdata["recorder"]="byzanz-record"
        self.cfgdata["plugin_config"]={}
        self.cfgdata["gui_config"]={}


    def get(self,key):
        if key in self.cfgdata:
            return self.cfgdata[key]
        elif key in self.user_cfg_data:
            return self.user_cfg_data[key]
        return {}
    def __cfg_item(self,key,cat):
        if cat in self.cfgdata:
            d=self.cfgdata[cat]
            if key in d:
                return d[key]
        return {}
    def __user_cfg_item(self,key,cat):
        if cat in self.user_cfg_data:
            d=self.user_cfg_data[cat]
            if key in d:
                return d[key]
        return {}

    def plugin_cfg_item(self,key):
        return self.__cfg_item(key,"plugin_config")

    def plugin_user_cfg_item(self,key):
        return self.__user_cfg_item(key,"plugin_config")

    def gui_cfg_item(self,key):
        return self.__cfg_item(key,"gui_config")

    def gui_user_cfg_item(self,key):
        return self.__user_cfg_item(key,"gui_config")

    def recorder_cfg_item(self,key):
        return self.__cfg_item(key,"recorder_config")

    def recorder_user_cfg_item(self,key):
        return self.__user_cfg_item(key,"recorder_config")

    def set(self,key,value,is_user_cfg=False):
        if is_user_cfg:
            self.user_cfg_data[key]=value
        else:
            self.cfgdata[key]=value


    def save(self):
        path=os.path.dirname(__file__)
        with open(path+"/config",'w') as f:
            json.dump(self.cfgdata,f,indent=4)
        with open(path+"/usercfg","w") as f:
            json.dump(self.user_cfg_data,f,indent=4)

cfg=Config()