import ctypes
import inspect
import json
import logging
import os
import threading

import global_var
from voiceDetect import voice_detect_func

logging.basicConfig(format='【%(asctime)s】 【%(levelname)s】 >>>  %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def print_hi():
    t = threading.Thread(target=voice_detect_func, args=())
    t.setDaemon(True)
    t.start()
    return t


def init_config():
    if os.path.exists('Hypnos.config'):
        with open('Hypnos.config', 'r') as f:
            data = json.load(f)
            global_var.Flags.dbThres = data['dbThres']
            global_var.HearFrequency.lowFre = data['lowFre']
            global_var.HearFrequency.highFre = data['highFre']


def update_config():
    with open('Hypnos.config', 'w') as f:
        data = {'dbThres': global_var.Flags.dbThres,
                'lowFre': global_var.HearFrequency.lowFre,
                'highFre': global_var.HearFrequency.highFre}
        json.dump(data, f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    update_config()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
