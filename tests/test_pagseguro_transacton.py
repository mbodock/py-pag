# encoding: utf-8

import mock

from py_pagseguro.pagseguro import PagSeguroTransaction
from py_pagseguro.exceptions import ApiErrorException, UnauthorizedException

from .base_test_case import BaseTestCase
from .utils import *

class PagSeguroTransactionTestCase(BaseTestCase):
    def test_can_instantiate(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        self.assertIsInstance(transaction, PagSeguroTransaction)

    def test_transaction_creates_reference(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        self.assertTrue(transaction.get_reference())

    def test_transaction_can_have_custom_reference(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com', reference='my-reference')
        self.assertEqual('my-reference', transaction.get_reference())

    def test_get_dados_without_item(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        transaction.get_dados()

    def test_set_sender_info(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        transaction.set_sender('comprador@teste.com.br', 'Comprador de teste')
        self.assertIn('senderEmail', transaction.get_dados())
        self.assertIn('senderName', transaction.get_dados())

    def test_set_item(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        transaction.set_item(self.item)
        self.assertIn('itemId1', transaction.get_dados())

    def test_set_redirect_url(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        transaction.set_redirect_url('urldeteste.com')
        self.assertIn('redirectURL', transaction.get_dados())

    def test_set_dicount(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        transaction.set_discount(1.14)
        self.assertIn('extraAmount', transaction.get_dados())

    def test_set_discount_int(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com')
        with self.assertRaises(ValueError):
            transaction.set_discount(114)

    @mock.patch('requests.post', mock.Mock(side_effect=post_fake))
    def test_get_checkout_url(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com', reference='reference', item=self.item)
        self.assertIn('8CF4BE7DCECEF0F004A6DFA0A8243412', transaction.get_checkout_url())

    @mock.patch('requests.post', mock.Mock(side_effect=post_fake_fail))
    def test_get_checkout_url_with_error(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com', reference='reference', item=self.item)
        with self.assertRaises(ApiErrorException):
            transaction.get_checkout_url()

    @mock.patch('requests.post', mock.Mock(side_effect=post_fake_unauthorized))
    def test_get_checkout_unauthorized(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com', reference='reference', item=self.item)
        with self.assertRaises(UnauthorizedException):
            transaction.get_checkout_url()

    @mock.patch('requests.post', mock.Mock(side_effect=post_fake_without_code))
    def test_get_checkout_without_code(self):
        transaction = PagSeguroTransaction('dummy_token', 'email@test.com', reference='reference', item=self.item)
        with self.assertRaises(ApiErrorException):
            transaction.get_checkout_url()
