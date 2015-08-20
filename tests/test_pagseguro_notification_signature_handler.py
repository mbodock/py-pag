# encoding: utf-8

import mock

from py_pag.pagseguro import PagSeguroNotificationSignatureHandler
from py_pag.exceptions import ApiErrorException, NotificationNotFoundException

from .base_test_case import BaseTestCase
from .utils import *


class PagSeguroNotificationSignatureTestCase(BaseTestCase):
    def setUp(self):
        self.data = {
            'email': 'email@teste.com',
            'token': 'TOK3NP4G5UR0',
            'code': '766B9C-AD4B044B04DA-77742F5FA653-E1AB24',
        }

    @mock.patch('requests.get', mock.Mock(side_effect=get_fake_signature_notification))
    def test_get_notification_response(self):
        handler = PagSeguroNotificationSignatureHandler(**self.data)
        response = handler.get_notification_response()
        self.assertEqual(response.status.lower(), u'active')
