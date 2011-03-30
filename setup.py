
from distutils.core import setup

from capacity import __version__ as VERSION

setup(name="capacity",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.6",
          ],
      description="Data types to describe capacity",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=VERSION,
      packages=["capacity"],
      scripts=[],
      )
