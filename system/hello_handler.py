#!/usr/bin/env python
# -*- coding: utf-8 -*-

from request_handler import RequestHandler


class HelloHandler(RequestHandler):
    """Class which handles the / URL"""

    def get(self):
        '''
        @summary: deals with GET request on /
        '''
        self.write("Welcome to restful centralized exclusive locking system !")
