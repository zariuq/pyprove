from setuptools import setup, find_packages

setup(name='pyprove',
      version='0.1',
      description='Automated Theorem Proving Tools',
      url='http://github.com/ai4reason/pyprove',
      author='ai4reason',
      license='GPL3',
      packages=find_packages(),
      #scripts=[
      #   'bin/greedy-cover.py'
      #],
      zip_safe=False)

