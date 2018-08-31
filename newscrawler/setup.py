from setuptools import setup, find_packages

setup(
    name='newscrapy',
    version='0.1',
    url='https://github.com/shiftcat',
    license='MIT',
    author='Y.Han Lee',
    author_email='shiftcat@daum.net',
    description='news crawler',
    packages=find_packages(exclude=['test']),
    long_description=open('README.MD').read(),
    zip_safe=False,
    install_requires=[
        'APScheduler == 3.5.2',
        'beautifulsoup4 == 4.6.1',
        'elasticsearch == 6.3.0',
        'gensim == 3.5.0',
        'JPype1 == 0.6.3',
        'konlpy == 0.5.1',
        'pymongo == 3.7.1',
        'Scrapy == 1.5.1',
      ],
    entry_points={'scrapy': ['settings = newscrapy.settings']},
    # setup_requires=['nose>=1.0'],
    # test_suite='nose.collector'
)
