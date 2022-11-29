from threading import Thread
from multiprocessing import Process, Lock

from queue import Queue, Empty
from common.event import Event
import time
from collections import defaultdict
from common.router import Router
from typing import Callable, Any


class Component:
    _components = []

    def __init_subclass__(cls, **kwargs):
        # note: It is useful for both registering subclasses in some way, and for setting default attribute values on those subclasses.
        super().__init_subclass__(**kwargs)
        Component._components.append(cls())

    def __init__(self, *args, **kwargs):  # note: for better consistency
        self.router = Router()

    def start(self):
        raise NotImplementedError

    def add_event_listener(self, event_type, callback: Callable[[Event], Any]):
        self.router.register_listener(event_type, callback)

    def add_event_publisher(self, event_type):
        return self.router.register_publisher(event_type)

    def publish(self, event: Event):  # thread safe
        self.router.dispatch_event(event)

    def remove_event_listener(self, event_type):
        # todo: For those module that enables to be unregistered
        pass

    def remove_event_publisher(self, event_type):
        pass


