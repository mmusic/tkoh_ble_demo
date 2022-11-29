from threading import Thread
from multiprocessing import Process, Queue, set_start_method
import time
from common.router import Router
from common.component import Component
import config.common as config
import importlib

# todo: set up config, what needs to be configured?


if __name__ == "__main__":
    # reference: https://zhuanlan.zhihu.com/p/144771768
    # set_start_method('fork')  # todo: mystery, if I dont set, I can make sub-process
    Router().loop_forever(daemon=True)
    loaded_modules = []
    for m, flag in config.TO_LOAD_MODULES.items():
        if flag:
            loaded_modules.append(importlib.import_module(name=m))

    for m in Component._components:
        try:
            m.start()
        except Exception as e:
            print(e)
