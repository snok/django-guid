from setuptools import setup, find_packages

from django_guid import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()
with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

setup(
    name='django-guid',
    version=__version__,
    description='Middleware that makes a request GUID available from anywhere and injects it into your logs.',
    include_package_data=True,
    long_description=readme + '\n\n' + changelog,
    license='BSD',
    author='Jonas Krüger Svensson',
    author_email='jonas-ks@hotmail.com',
    url='https://github.com/JonasKs/django-guid',
    download_url='https://pypi.python.org/pypi/django-guid',
    packages=find_packages(exclude=['']),
    install_requires=['Django>=2.2'],
    keywords=['django', 'logging', 'request', 'web', 'uuid', 'guid', 'correlation', 'correlation-id'],
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
