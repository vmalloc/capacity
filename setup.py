import os
import platform
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "capacity", "__version__.py")) as version_file:
    exec(version_file.read())

_INSTALL_REQUIREMENTS = []
if platform.python_version() < '2.7':
    _INSTALL_REQUIREMENTS.append('unittest2')

setup(name="capacity",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          ],
      description="Data types to describe capacity",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      install_requires=_INSTALL_REQUIREMENTS,
      scripts=[],
      )
