# encoding: utf-8

import unittest

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.item = {
            'id': 'id',
            'description': 'item description',
            'quantity': 1,
            'amount': 3.14,
        }
