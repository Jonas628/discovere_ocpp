from setuptools import setup, find_packages
import re

with open('README.md') as f:
    readme = f.read()

# extract version
with open('chargesim/chargesim/__init__.py') as file:
    for line in file.readlines():
        m = re.match("__version__ *= *['\"](.*)['\"]", line)
        if m:
            version = m.group(1)

setup(name='chargesim',
      version=version,
      description='Simulation for Smart Charging.',
      long_description=readme,
      long_description_content_type='text/markdown',
      url='https://github.com/OleBialas/chargesim.git',
      author='Ole Bialas',
      author_email='bialas@cbs.mpg.de',
      license='MIT',
      python_requires='>=3.6',
      install_requires=['websockets', 'ocpp', 'pymongo'],
      packages=find_packages(),
      package_data={'freefield': ['data/*.txt', 'data/*.wav', 'data/rcx/*']},
      include_package_data=True,
      zip_safe=False)
