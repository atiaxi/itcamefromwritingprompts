try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Important distutils stuff:
#   This file from https://docs.python.org/2/distutils/
#   https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html

setup(
    name="itcamefromwritingprompts",
    version="1.0",
    description= "Build and display a markov model based on /r/writingprompts",
    author="Roger Ostrander",
    author_email="atiaxi@gmail.com",
    url="http://itcamefromwritingprompts.com",
    packages=['icfwp'],
    install_requires=[
        'flask>=0.10.1',
        'praw>=2.1.21',
        'pytz>=2015.2',
    ],
)
