from setuptools import setup, find_packages

setup(
    name='py-pag',
    version='0.1.0',
    description='PagSeguro lib that suports manual subscriptions',
    url='',
    author='Mbodock',
    author_email='mbodock@gmail.com',
    license='MIT',
    classifiers=[
        'Developer Status :: 4 - Beta',
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
