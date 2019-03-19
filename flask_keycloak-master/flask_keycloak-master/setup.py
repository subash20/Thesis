"""
Flask-Keycloak
-------------

"""
from setuptools import setup


setup(
    name='Flask-Keycloak',
    version='0.1.1',
    url='',
    license='',
    author='Bibek Chitrakar',
    author_email='bibek.chitrakar@gmail.com',
    description='OIDC for Keycloak, a open source Identity and Access Management solution',
    long_description=__doc__,
    packages=["flask_keycloak"],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Login',
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)