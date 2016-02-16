from PyQt4 import QtCore

from py import localization as local

lang = local.Local()

def _(string):
    s=QtCore.QString(lang._(string))
    return unicode(s,'utf-8')