# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name='py-pag',
    version='0.1.0',
    description='PagSeguro lib that suports manual subscriptions',
    long_description='''
        O py-pag é uma pequena lib construída para facilitar a integração de assinaturas manuais no PagSeguro.

        O py-pag também suporta compras pontuais e suporte a notificações do pagseguro.
    ''',
    url='https://github.com/mbodock/py-pag',
    author='Mbodock',
    author_email='mbodock@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pagseguro subscription',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'arrow',
        'beautifulsoup4',
        'requests',
        'Unidecode',
    ],
)
