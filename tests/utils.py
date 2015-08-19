# encoding: utf-8

def post_fake(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <head></head>
        <body>
            <?xml version="1.0" encoding="ISO-8859-1"?>  
            <checkout>  
                <code>8CF4BE7DCECEF0F004A6DFA0A8243412</code>  
                <date>2010-12-02T10:11:28.000-02:00</date>  
            </checkout>
        </body>
        """
    return ResponseFake()

def post_fake_without_code(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <head></head>
        <body>
            <?xml version="1.0" encoding="ISO-8859-1"?>  
            <checkout>  
                <date>2010-12-02T10:11:28.000-02:00</date>  
            </checkout>
        </body>
        """
    return ResponseFake()

def post_fake_fail(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <head></head>
        <body>
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
        </body>
        """
    return ResponseFake()

def post_fake_unauthorized(*args, **kwargs):
    class ResponseFake(object):
        content = """
        <head></head>
        <body>
            <p>Unauthorized</p>
        </body>
        """
    return ResponseFake()


