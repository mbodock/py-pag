# encoding: utf-8

def post_fake(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <?xml version="1.0" encoding="ISO-8859-1"?>  
        <checkout>  
            <code>8CF4BE7DCECEF0F004A6DFA0A8243412</code>  
            <date>2010-12-02T10:11:28.000-02:00</date>  
        </checkout>
        """
        status_code = 200
    return ResponseFake()

def post_fake_without_code(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <?xml version="1.0" encoding="ISO-8859-1"?>  
        <checkout>  
            <date>2010-12-02T10:11:28.000-02:00</date>  
        </checkout>
        """
        status_code = 200
    return ResponseFake()

def post_fake_fail(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <?xml version="1.0" encoding="ISO-8859-1"?>
        <errors>
            <error>
                <code>11004</code>
                <message>Currency is required.</message>
            </error>
            <error>
                <code>11005</code>
                <message>Currency invalid value: 100</message>
            </error>
        </errors>
        """
        status_code = 400
    return ResponseFake()

def post_fake_unauthorized(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <p>Unauthorized</p>
        """
        status_code = 401
    return ResponseFake()

def get_fake_notification_not_found(*args, **kwargs):
    class ResponseFake(object):
        content = "<p>Not Found</p>"
        status_code = 404
    return ResponseFake()

def get_fake_notification(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <!--?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?-->
        <transaction>
            <date>2011-02-10T16:13:41.000-03:00</date>
            <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>
            <reference>REF1234</reference>
            <type>1</type>
            <status>3</status>
            <paymentmethod>
                <type>1</type>
                <code>101</code>
            </paymentmethod>
            <grossamount>49900.00</grossamount>
            <discountamount>0.00<discountamount>
            <creditorfees>
                <intermediationrateamount>0.40</intermediationrateamount>
                <intermediationfeeamount>1644.80</intermediationfeeamount>
            </creditorfees>
            <netamount>49900.00</netamount>
            <extraamount>0.00</extraamount>
            <installmentcount>1</installmentcount>
            <itemcount>2</itemcount>
            <items>
                <item>
                    <id>0001</id>
                    <description>Notebook Prata</description>
                    <quantity>1</quantity>
                    <amount>24300.00</amount>
                </item>
                <item>
                    <id>0002</id>
                    <description>Notebook Rosa</description>
                    <quantity>1</quantity>
                    <amount>25600.00</amount>
                </item>
            </items>
            <sender>
                <name>José Comprador</name>
                <email>comprador@uol.com.br</email>
                <phone>
                    <areacode>11</areacode>
                    <number>56273440</number>
                </phone>
            </sender>
            <shipping>
                <address>
                    <street>Av. Brig. Faria Lima</street>
                    <number>1384</number>
                    <complement>5o andar</complement>
                    <district>Jardim Paulistano</district>
                    <postalcode>01452002</postalcode>
                    <city>Sao Paulo</city>
                    <state>SP</state>
                    <country>BRA</country>
                </address>
                <type>1</type>
                <cost>21.50</cost>
            </shipping>
        </discountamount></discountamount></transaction>
        """
        status_code = 200
    return ResponseFake()

def get_fake_signature_notification(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <!--?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?-->
        <preApproval>
            <name>Seguro contra roubo do Notebook Prata</name>
            <code>C08984179E9EDF3DD4023F87B71DE349</code>
            <date>2011-11-23T13:40:23.000-02:00</date>
            <tracker>538C53</tracker>
            <status>ACTIVE</status>
            <reference>REF1234</reference>
            <lastEventDate>2011-11-25T20:04:23.000-02:00</lastEventDate>
            <charge>auto</charge>
                <sender>
                <name>Comprador Istambul</name>
                <email>c@i.com</email>
                <phone>
                <areaCode>11</areaCode>
                <number>30389678</number>
                </phone>
                <address>
                <street>ALAMEDA ITU</street>
                <number>78</number>
                <complement>ap. 2601</complement>
                <district>Jardim Paulista</district>
                <city>SAO PAULO</city>
                <state>SP</state>
                <country>BRASIL</country>
                <postalCode>01421000</postalCode>
                </address>
                </sender>
        </preApproval>
        """
        status_code = 200
    return ResponseFake()


def get_fake_charger(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <!--?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?-->
        <result>
        <transactionCode>D9AD1EA3DEB544A6A413E33BD4822225</transactionCode>
        <date>2011-08-19T14:47:59.000-03:00</date>
        </result>
        """
        status_code = 200
    return ResponseFake()

def get_fake_charger_error(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <errors>
            <error>
            <code>11004</code>
            <message>Currency is required.</message>
            </error>
            <error>
            <code>11005</code>
            <message>Currency invalid value: ValorCurrencyInvalido</message>
            </error>
        </errors>
        """
        status_code = 400
    return ResponseFake()
