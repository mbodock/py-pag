# encoding: utf-8

import mock

from py_pag.pagseguro import PagSeguroSignature
from py_pag.exceptions import ApiErrorException, UnauthorizedException

from .base_test_case import BaseTestCase
from .utils import *


class PagSeguroSignatureTestCase(BaseTestCase):
    def setUp(self):
        self.data = {
            'token': 'token',
            'email': 'email@email.com',
            'name': 'Signature name',
            'description': 'the description',
            'price': 3.14,
        }
    def test_create_name_to_long(self):
        with self.assertRaises(ValueError):
            singature = PagSeguroSignature(
                token='token',
                email='email@email.com',
                name='This name is really long for a signature on pagseguro it has more than 100 characteres just to test the validation',
                description='the description',
                price=3.14,
        )

    def test_create_description_really_long(self):
        self.data['description'] = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas in
        orci sed arcu ullamcorper rhoncus quis vitae massa. Proin elit tortor,
        imperdiet vitae imperdiet non, dignissim sit amet massa. Ut accumsan mi
        vel arcu volutpat.
        """
        with self.assertRaises(ValueError):
            singature = PagSeguroSignature(**self.data)

    def test_create_with_price_int(self):
        self.data['price'] = 230
        with self.assertRaises(ValueError):
            singature = PagSeguroSignature(**self.data)

    def test_create_with_invalid_period(self):
        with self.assertRaises(ValueError):
            singature = PagSeguroSignature(period='INVALID', **self.data)

    def test_get_dados(self):
        signature = PagSeguroSignature(**self.data)
        signature.set_sender('comprador@teste.com.br', 'Comprador de teste')
        signature.set_redirect_url('urldeteste.com')
        self.assertIn('preApprovalName', signature.get_dados())
