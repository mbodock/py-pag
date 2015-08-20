# encoding: utf-8
import requests
import arrow
from uuid import uuid4

from bs4 import BeautifulSoup
from unidecode import unidecode

from .exceptions import ApiErrorException, UnauthorizedException, NotificationNotFoundException


class PagSeguroBase(object):
    def __init__(self, token, email):
        self.email = email
        self.token = token
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'charset': 'UTF-8'
        }


class PagSeguroTransaction(PagSeguroBase):
    URLS = {
        'request': 'https://ws.pagseguro.uol.com.br/v2/checkout',
        'request_redirect': 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code={code}',
    }

    def __init__(self, token, email, reference=None, item=None):
        self.item = item
        self.reference = reference
        self.sender = None
        self.redirect_url = None
        self.discount = None

        if not reference:
            self.reference = str(uuid4())
        else:
            self.reference = reference

        super(PagSeguroTransaction, self).__init__(token, email)

    def set_item(self, item):
        self.item = item

    def get_reference(self):
        return self.reference

    def get_code(self, soup):
        try:
            code = str(soup.find('code').string)
        except AttributeError:
            raise ApiErrorException('Code Not Found')
        return code

    def set_discount(self, value):
        if type(value) is not float:
            raise ValueError('Price should be float')
        self.discount = value

    def get_checkout_url(self):
        response = requests.post(self.URLS['request'], data=self.get_dados(), headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.body.p is not None and str(soup.body.p.string) == u'Unauthorized':
            raise UnauthorizedException(u'invalid Token ou E-mail')
        if soup.body.errors is not None:
            code = str(soup.body.errors.error.code.string)
            message = str(soup.body.errors.error.message.string)
            raise ApiErrorException('{code} - {message}'.format(code=code, message=message))
        code = self.get_code(soup)
        return self.URLS['request_redirect'].format(code=code)

    def set_sender(self, email, name):
        if name:
            name = name[:49]
        self.sender = {'email': email, 'name': name}

    def get_dados(self):
        return self.__dict__()

    def set_redirect_url(self, url):
        self.redirect_url = url

    def __dict__(self):
        data = {
            'token': self.token,
            'email': self.email,
            'currency': 'BRL',
            'reference': self.reference,
        }

        if self.item:
            data['itemId1'] = self.item['id'],
            data['itemDescription1'] = self.item['description'],
            data['itemAmount1'] = "{0:.2f}".format(round(self.item['amount'], 2)),
            data['itemQuantity1'] = self.item['quantity'],
        if self.sender:
            data['senderEmail'] = self.sender['email'],
            data['senderName'] = self.sender['name'],
        if self.redirect_url:
            data['redirectURL'] = self.redirect_url
        if self.discount:
            data['extraAmount'] = "-{0:.2f}".format(self.discount, 2)
        return data


class PagSeguroSignature(PagSeguroTransaction):
    URLS = {
        'request': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/request',
        'request_redirect': 'https://pagseguro.uol.com.br/v2/pre-approvals/request.html?code={code}',
    }

    TIPOS_PERIODOS = ['WEEKLY', 'MONTHLY', 'BIMONTHLY', 'TRIMONTHLY', 'SEMIANNUALLY', 'YEARLY']

    def __init__(self, token, email, name, description, price, reference=None, period='MONTHLY'):
        if len(name) > 100:
            raise ValueError('Invalid name, too long')
        if len(description) > 255:
            raise ValueError('Invalid Description, too long')
        if type(price) is not float:
            raise ValueError('Price should be float')
        if period not in self.TIPOS_PERIODOS:
            raise ValueError('Invalid period')

        self.name = name
        self.description = description
        self.price = price
        self.period = period
        self._set_end_date()

        super(PagSeguroSignature, self).__init__(token, email, reference)

    def __dict__(self):
        data = {
            'token': self.token,
            'email': self.email,
            'preApprovalName': self.name,
            'preApprovalDetails': self.description,
            'preApprovalAmountPerPayment': "{0:.2f}".format(round(self.price, 2)),
            'preApprovalPeriod': self.period,
            'preApprovalMaxPaymentsPerPeriod': 1,
            'preApprovalMaxAmountPerPeriod': "{0:.2f}".format(round(self.price, 2)),
            'preApprovalMaxTotalAmount': "{0:.2f}".format(round(self.price * 12, 2)),
            'preApprovalFinalDate': self.end_date,
            'reference': self.reference
        }

        if self.sender:
            data.update({'senderEmail': self.sender['email'], 'senderName': self.sender['name']})
        if self.redirect_url:
            data['redirectURL'] = self.redirect_url
        return data

    def _set_end_date(self):
        now = arrow.now()
        next_year = now.replace(years=+1).datetime
        next_year_iso = next_year.isoformat()
        self.end_date = next_year_iso[:-13] + next_year_iso[-6:]


class PagSeguroSender(object):
    def __init__(self, name=None, ddd=None, phone=None, email=None, city=None, uf=None):
        if name and len(name) > 50:
            raise ValueError('Invalid Name')
        if ddd and len(ddd) > 2:
            raise ValueError('Invalid DDD')
        if phone and (len(phone) < 7 or len(phone) > 9):
            raise ValueError('Invalid phone')
        if city and len(city) > 60:
            raise ValueError('Invalid city name')
        if uf and len(uf) is not 2:
            raise ValueError('Invalid UF')

        self.name = name
        self.ddd = ddd
        self.phone = phone
        self.email = email
        self.city = city
        self.uf = uf
        self.country = 'BRA'

    def __dict__(self):
        return {
            'senderName': self.name,
            'senderAreaCode': self.ddd,
            'senderPhone': self.phone,
            'senderEmail': self.email,
            'senderAddressCity': self.city,
            'senderAddressState': self.uf,
            'senderAddressCountry': self.country
        }

    def get_dados(self):
        return self.__dict__()


class PagSeguroNotificationHandler(PagSeguroBase):
    URLS = {
        'check_notification': 'https://ws.pagseguro.uol.com.br/v2/transactions/notifications/{code}?email={email}&token={token}',
    }

    def __init__(self, token, email, code):
        self.code = code
        super(PagSeguroNotificationHandler, self).__init__(token, email)

    def _valid_notification(self, soup):
        if soup.p and str(soup.p.string) == 'Not Found':
            raise NotificationNotFoundException('Notification not found')

        if soup.find('error'):
            code = str(soup.body.errors.error.code.string)
            message = str(soup.body.errors.error.message.string)
            raise ApiErrorException('{code} - {message}'.format(code=code, message=message))

    def get_check_notification_url(self):
        return self.URLS['check_notification'].format(code=self.code, email=self.email, token=self.token)

    def get_notification_info(self):
        if not self.code:
            raise RuntimeError("No code provided, try get_check_notification_url the url first")
        notification_url = self.get_check_notification_url()
        response = requests.get(notification_url, headers=self.headers)
        self.notification_response = response.content
        return self.notification_response

    def get_notification_response(self):
        soup = BeautifulSoup(self.get_notification_info())
        self._valid_notification(soup)

        pagseguro_response = PagSeguroNotificationResponse(
            str(soup.code.string),
            str(soup.reference.string),
            str(soup.type.string),
            str(soup.status.string),
            str(soup.grossamount.string),
            soup.sender
        )
        return pagseguro_response


class PagSeguroNotificationSignatureHandler(PagSeguroNotificationHandler):
    URLS = {
        'check_notification': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/notifications/{code}?email={email}&token={token}',
        'check_assinatura': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/{code}?email={email}&token={token}',
        'payment': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/payment/',
    }

    def get_signature_notification_info(self):
        soup = BeautifulSoup(self.get_notification_info())
        self._valid_notification(soup)

        self.data = soup.find('preapproval')
        return self.get_signature_notification()

    def get_signature_notification(self):
        data = self.data
        signature_response = PagSeguroSignatureResponse(
            str(data.code.string),
            str(data.date.string),
            str(data.tracker.string),
            str(data.status.string),
            str(data.reference.string),
            str(data.lasteventdate.string),
            str(data.charge.string),
            data.sender
        )
        return signature_response

    def get_notification_response(self):
        return self.get_signature_notification_info()


class PagSeguroAbstractResponse(object):
    """ Abstract class for a PagSeguro Response """

    def __init__(self):
        raise NotImplementedError

    def format_sender_data(self, sender_soup):
        sender = {}
        try:
            sender['name'] = unidecode(str(sender_soup.find('name').string)),
        except:
            sender['name'] = u'Problema em identificar o nome'

        sender['name'] = str(sender_soup.find('email').string),
        return sender


class PagSeguroSignatureResponse(PagSeguroAbstractResponse):
    def __init__(self, code, date, tracker, status, reference, lasteventdate, charge, soup_sender):
        self.code = code
        self.date = arrow.get(date).datetime
        self.tracker = tracker
        self.status = status
        self.reference = reference
        self.lasteventdate = lasteventdate
        self.charge = charge
        self.sender = self.format_sender_data(soup_sender)


class PagSeguroNotificationResponse(PagSeguroAbstractResponse):
    STATUS = {
        1: u'Aguardadno pagamento',
        2: u'Em análise',
        3: u'Paga',
        4: u'Disponível',
        5: u'Em disputa',
        6: u'Devolvida',
        7: u'Cancelada',
    }

    TRANSACTION_TYPE = {
        1: 'Pagamento',
        11: 'Assinatura'
    }

    def __init__(self, code, reference, transactiontype, status, amount, soup_sender):
        self.code = code
        self.reference = reference
        self.transactiontype = self.TRANSACTION_TYPE[int(transactiontype)]
        self.status = self.STATUS[int(status)]
        self.amount = amount
        self.sender = self.format_sender_data(soup_sender)


class PagSeguroSignatureCharger(PagSeguroTransaction):
    URLS = {
        'payment': 'https://ws.pagseguro.uol.com.br/v2/pre-approvals/payment/'
    }

    def __init__(self, token, email, code, items=[], reference=None):
        super(PagSeguroSignatureCharger, self).__init__(token, email, reference)
        self.code = code
        self.items = items
        self.reference = reference

    def get_data(self):
        data = {
            'email': self.email,
            'token': self.token,
            'preApprovalCode': self.code
        }
        if self.reference:
            data['reference'] = self.reference

        data.update(self.get_items_data())
        return data

    def get_items_data(self):
        data = {}
        for index, item in enumerate(self.items):
            data['itemId{index}'.format(index=index + 1)] = item['id']
            data['itemDescription{index}'.format(index=index + 1)] = item['description']
            data['itemAmount{index}'.format(index=index + 1)] = "{:.2f}".format(item['amount'])
            data['itemQuantity{index}'.format(index=index + 1)] = item['quantity']
        return data

    def charge(self):
        response = requests.post(self.URLS['payment'], data=self.get_data(), headers=self.headers)
        soup = BeautifulSoup(response.content)
        if soup.body.p is not None and str(soup.body.p.string) == u'Unauthorized':
            raise UnauthorizedException(u'invalid Token ou E-mail')
        elif soup.body.errors is not None:
            code = str(soup.body.errors.error.code.string)
            message = str(soup.body.errors.error.message.string)
            raise ApiErrorException('{code} - {message}'.format(code=code, message=message))

        return (soup.transactionCode, soup.date)
