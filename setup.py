#!/usr/bin/env python

from setuptools import setup


requires = [req.strip() for req in open('requirements.txt', 'r').readlines()]
long_desc = open('README.md', 'r').read()

setup(
    name="python-spotify-api",
    version='0.2.1',
    description='Lightweight Spotify metadata search API wrapper',
    author='Matt Dennewitz',
    author_email='mattdennwitz@gmail.com',
    long_description=long_desc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
    keywords='spotify audio',
    url='https://github.com/mattdennewitz/python-spotify-api/',
    license='BSD',
    packages=['spotify_api'],
    install_requires=requires,
    zip_safe=False,
)
