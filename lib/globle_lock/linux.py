import fcntl

__dict = {}


def lock(id):
    fp = open(id, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        __dict[id] = fp
    except IOError:
        return False
    return True


def unlock(id):
    if id in __dict:
        __dict[id].close()
