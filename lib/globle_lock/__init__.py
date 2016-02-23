import sys

mswindows = (sys.platform == "win32")
is_linux = (sys.platform.startswith("linux"))


def lock(id):
    if is_linux:
        import linux
        return linux.lock(id)
    if mswindows:
        import win32
        return win32.lock(id)


def unload(id):
    if is_linux:
        import linux
        linux.unlock(id)
    if mswindows:
        import win32
        win32.unlock()
