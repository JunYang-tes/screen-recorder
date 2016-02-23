from PyQt4 import QtCore
import logging


def get_text_fn(lang):
    def _(string):
        if lang:
            s = QtCore.QString(lang._(string))
            return unicode(s, 'utf-8')
        else:
            logging.warn("lang not set")
            return string

    return _
