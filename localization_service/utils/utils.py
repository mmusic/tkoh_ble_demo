import threading
import ctypes


def kill_thread(thread: threading.Thread):
    if not thread.is_alive():
        print("thread is dead already")
        return

    thread_id = thread.ident

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_id), ctypes.py_object(ValueError))

    if res == 0:
        raise ValueError("incorrect thread_id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')



