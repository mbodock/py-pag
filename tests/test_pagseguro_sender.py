# encoding: utf-8

import mock

from py_pag.pagseguro import PagSeguroSender
from py_pag.exceptions import ApiErrorException, UnauthorizedException

from .base_test_case import BaseTestCase
from .utils import *


class PagSeguroSenderTestCase(BaseTestCase):
    def setUp(self):
        self.data = {
            'name': 'User Name',
            'ddd': '38',
            'phone': '22222222',
            'email': 'email@teste.com',
            'city': 'City Name',
            'uf': 'MG',
        }

    def test_get_dict(self):
        sender = PagSeguroSender(**self.data)
        expected = {
            'senderName': self.data['name'],
            'senderAreaCode': self.data['ddd'],
            'senderPhone': self.data['phone'],
            'senderEmail': self.data['email'],
            'senderAddressCity': self.data['city'],
            'senderAddressState': self.data['uf'],
            'senderAddressCountry': 'BRA',
        }
        self.assertEqual(expected, sender.get_dados())

    def test_with_invalid_name(self):
        self.data['name'] = 'this name is really really long even for crazy standads'
        with self.assertRaises(ValueError):
            sender = PagSeguroSender(**self.data)

    def test_with_invalid_ddd(self):
        self.data['ddd'] = '1235'
        with self.assertRaises(ValueError):
            sender = PagSeguroSender(**self.data)

    def test_with_invalid_phone(self):
        self.data['phone'] = '112331241231'
        with self.assertRaises(ValueError):
            sender = PagSeguroSender(**self.data)

    def test_with_invalid_city(self):
        self.data['city'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit amet.'
        with self.assertRaises(ValueError):
            sender = PagSeguroSender(**self.data)

    def test_with_invalid_uf(self):
        self.data['uf'] = 'VAC'
        with self.assertRaises(ValueError):
            sender = PagSeguroSender(**self.data)
