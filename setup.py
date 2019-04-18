from setuptools import setup

setup(name='car-detector',
      long_description=open('README.md').read(),
      entry_points={
          'console_scripts': [
              'detect = app.__main__:main',
          ],
      })
