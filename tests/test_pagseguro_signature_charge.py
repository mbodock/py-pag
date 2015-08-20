# encoding: utf-8

import mock

from py_pag.pagseguro import PagSeguroSignatureCharger
from py_pag.exceptions import ApiErrorException, UnauthorizedException

from .base_test_case import BaseTestCase
from .utils import *

class PagseguroSignatureChargeTestCase(BaseTestCase):
    def setUp(self):
        self.data = {
            'token': 'TOK3NP4G5UR0',
            'email': 'email@teste.com',
            'code': '766B9C-AD4B044B04DA-77742F5FA653-E1AB24',
            'items': [{
                'id': 'item id',
                'description': 'item description',
                'quantity': 1,
                'amount': 3.14,
            }],
            'reference': 'Internal REference',
        }

    @mock.patch('requests.post', mock.Mock(side_effect=post_fake_unauthorized))
    def test_charge_invalid_token(self):
        charger = PagSeguroSignatureCharger(**self.data)
        with self.assertRaises(UnauthorizedException):
            code, date = charger.charge()

    @mock.patch('requests.post', mock.Mock(side_effect=get_fake_charger))
    def test_charge(self):
        charger = PagSeguroSignatureCharger(**self.data)
        code, date = charger.charge()

    @mock.patch('requests.post', mock.Mock(side_effect=get_fake_charger_error))
    def test_charge_error(self):
        charger = PagSeguroSignatureCharger(**self.data)
        with self.assertRaises(ApiErrorException):
            code, date = charger.charge()
