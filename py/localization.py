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


_languages = []


def __init():
    list_file = os.path.dirname(__file__) + "lang/lang_list"
    if os.path.exists(list_file):
        with open(list_file) as f:
            for line in f.readlines():
                idx = line.find(":")
                _languages.append((line[:idx], line[idx + 1:]))
    else:
        path = os.path.dirname(__file__) + "/lang"
        for f in os.listdir(path):
            _languages.append((f, f))


def set_location(l):
    Local.Lang=l

def get_all_languages():
    return _languages


__init()


if __name__=="__main__":
    print get_all_languages()