# -*- coding: utf-8 -*-
import gettext, os
import logging

class Local:
    Lang = "zh_CN"

    def __init__(self,filepath=None):
        try:
            if filepath is None:
                import sys
                f = sys._getframe().f_back
                dirname = os.path.dirname(__file__)[:-2]
                filepath = f.f_code.co_filename.lstrip(dirname)
            filename=Local.__get_file_name(filepath)
            self._ = Local.__get_local_strings(Local.Lang, filepath)
        except Exception as e:
            logging.warn(e)

    @staticmethod
    def __get_file_name(path):
        idx=path.rindex('/')
        return path[idx+1:]

    def _(self,string):
        return string

    @staticmethod
    def __get_local_strings(lang,file):
        current_dir = os.path.dirname(os.path.realpath(__file__))+'/lang'
        return gettext.translation(file, current_dir, [lang, "English"]).gettext

def set_location(l):
    Local.Lang=l

def get_all_languages():
    ret=[]
    path=os.path.dirname(__file__)+"/lang"
    for f in os.listdir(path):
        ret.append(f)
    return ret


if __name__=="__main__":
    print get_all_languages()