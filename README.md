What is metalang?
=================
Metalang is a project that generate message stubs from an agnostic definition.

Instead of containing homebrewn serialization, it allows you to utilize common
types of the generated language to serialize/deserialize messages.

It also introduces reflection in languages which lacks it (like c/c++) which
allows for a more lightweight message layer, shared over multiple applications.

Python
------
Python serializes to/from it's dict type, which can be easily packaged in the
container of your choice.

C++
---
C++ serializes from/to a dynamic\_map, which is a mapping to the specified
dynamic\_type. A header only set of libraries which are generated on the fly.
