#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.testing
from system.main import make_app as get_app


class HelloTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return get_app()

    def assertIn(self, str1, str2):
        self.assertTrue(str1 in str2)

    def test_home(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertIn("Welcome", response.body.decode('utf-8'))
        self.assertEqual(response.code, 200)
