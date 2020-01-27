#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
from contextlib import suppress

import functools
import signal
import time
import msvcrt

from hello_handler import HelloHandler
from resource_handler import ResourceHandler
from resources_handler import ResourcesHandler
from locks_handler import LocksHandler
from lock_handler import LockHandler

from lock import LOCK_MANAGER_INSTANCE

def on_every_second():
    '''
    @summary: function called by tornado/ioloop every second

    It's used to clear expired locks
    '''
    LOCK_MANAGER_INSTANCE.clean_expired_locks()
    print("chicking expired locks.\n")

def make_app():
    '''
    @summary: returns the tornado application
    @param unit_testing: if True, we add some handler for unit testing only
    @result: the tornado application
    '''
    urls = [
        tornado.web.URLSpec(r"/", HelloHandler, name="hello"),
        tornado.web.URLSpec(r"/resources/([a-zA-Z0-9]+)", ResourceHandler, name="resource"),
        tornado.web.URLSpec(r"/resources", ResourcesHandler, name="resources"),
        tornado.web.URLSpec(r"/locks/([a-zA-Z0-9]+)", LocksHandler, name="locks"),
        tornado.web.URLSpec(r"/locks/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)", LockHandler, name="lock")
        ]
    application = tornado.web.Application(urls)
    return application


def stop_application(application):
    print("Stopping webserver...")
    stop_periodicCallback()
    application.stop()
    print("Webserver stopped !")



async def periodicCallback():
    '''
    @summary: calls a function forever the server is running
    and makes milliseconds sleep between calls.
    '''
    while True:
        on_every_second()
        await asyncio.sleep(1)

def stop_periodicCallback():
    '''
    @summary: terminate the PeriodicCallback method.
    '''
    print("Stopping periodicCallback loop...")
    task.cancel()
    print("periodicCallback loop stopped !")

def get_ioloop():
    '''
    @summary: returns a configured tornado ioloop
    '''
    # made for testing only
    loop = asyncio.get_event_loop()
    return loop

if __name__ == '__main__':
    '''
    @summary: main function (starts the server)
    '''
    AsyncIOMainLoop().install()
    application = make_app()
    application.listen(8000)
    loop = asyncio.get_event_loop()
    loop.call_later(1, periodicCallback)
    task = loop.create_task(periodicCallback())

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        stop_application(application)
