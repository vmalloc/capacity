![Build Status] (https://secure.travis-ci.org/vmalloc/capacity.png ) &nbsp; ![Version] (https://img.shields.io/pypi/v/capacity.svg )

# Overview

Capacity is a package helping you express capacity (or data size) units as Pythonic objects, and manipulate them in a useful, intuitive manner.

# Usage

Capacity units can be created by using the built-in capacity objects:

```python
>>> from capacity import *
>>> size = 2 * GiB

```

The above creates a capacity unit that represents 2GiB (2 * (1024<sup>3</sup>) bytes). Capacity already comes pre-loaded with `KiB`, `MiB`, `GiB`, `TiB`, `EiB` for binary units, and `KB`, `MB`, `GB`, `TB`, `EB` for decimal units. You even have `byte` to denote a single byte.

Capacity objects can be added, multiplied, divided and more:

```python
>>> size // GiB
2

>>> ((size * 2) // 3 * 12) % (13 * byte)
9*byte

>>> (2.51 * GiB) // GiB
2

>>> abs(10*byte - 1500*GiB)
1610612735990*byte

```

You can round units up or down to the nearest boundary:

```python
>>> (2.5 * GiB).roundup(GiB)
3*GiB
>>> (2.5 * GiB).rounddown(GiB)
2*GiB

```

Formatting is easy:

```python
>>> size = 1234567 * byte
>>> "In megabytes, we have {0:MB}".format(size)
'In megabytes, we have 1'

>>> "We have {0:MB!}".format(size) # include unit in output
'We have 1MB'

```

You can easily parse textual representations of sizes:

```python
>>> Capacity("20GB")
20*GB
>>> Capacity("20GiB")
20*GiB

```

You can even manipulate units which are not whole bytes:

```python
>>> byte / 2
4*bit

```

# License

BSD3 (See `LICENSE`)

