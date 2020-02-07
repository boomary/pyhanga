__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


from setuptools import setup, find_packages

setup(
    name='pyhanga',
    packages=['pyhanga'],
    author='Sivadon Chaisiri',
    author_email='sivadon@ieee.org',    
    version=0.901,
    license='MIT',
    description = 'Custom Python-based CloudFormation Command Line Interface',
    url = 'https://github.com/boomary/pyhanga',   
    download_url = 'https://github.com/boomary/pyhanga/archive/v_901.tar.gz', 
    keywords = ['AWS', 'CloudFormation', 'CLI'],    
    install_requires=[
        'click',
        'boto3',
    ],
    include_package_data=True,   
    entry_points={
        'console_scripts': ['pyhanga=pyhanga.commands:cli']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
