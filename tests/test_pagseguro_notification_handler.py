# encoding: utf-8

import mock

from py_pag.pagseguro import PagSeguroNotificationHandler
from py_pag.exceptions import ApiErrorException, NotificationNotFoundException

from .base_test_case import BaseTestCase
from .utils import *


class PagSeguroNotificationTestCase(BaseTestCase):
    def setUp(self):
        self.data = {
            'email': 'email@teste.com',
            'token': 'TOK3NP4G5UR0',
            'code': '766B9C-AD4B044B04DA-77742F5FA653-E1AB24',
        }

    def test_create_without_code(self):
        self.data['code'] = None
        with self.assertRaises(ValueError):
            handler = PagSeguroNotificationHandler(**self.data)

    @mock.patch('requests.get', mock.Mock(side_effect=get_fake_notification))
    def test_get_notification_response(self):
        handler = PagSeguroNotificationHandler(**self.data)
        response = handler.get_notification_response()
        self.assertEqual(response.status, u'Paga')

    @mock.patch('requests.get', mock.Mock(side_effect=get_fake_notification_not_found))
    def test_get_notification_invalid_code(self):
        handler = PagSeguroNotificationHandler(**self.data)
        with self.assertRaises(NotificationNotFoundException):
            response = handler.get_notification_response()

    @mock.patch('requests.get', mock.Mock(side_effect=post_fake_fail))
    def test_get_checkout_without_code(self):
        handler = PagSeguroNotificationHandler(**self.data)
        with self.assertRaises(ApiErrorException):
            response = handler.get_notification_response()
