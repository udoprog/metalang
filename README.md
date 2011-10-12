What is metalang?
=================
Metalang is a project that generate message stubs from an language agnostic
definition.

Instead of containing homebrewn serialization, it allows you to utilize common
types of the generated language to serialize/deserialize messages.

It also introduces reflection in languages which lacks it (like c/c++) which
allows for a more lightweight (code-wise) message layer, shared over multiple
applications and languages.

The general concept follows the DRY principle, your message layer should only
be defined in one place.

Compared to protocol buffers, metalang is far less efficient but instead allows
for type information to be transferred with the messages, and an loosely
defined means of serialization which could map to anything.

Python
------
Python serializes to/from it's dict type, which can be easily packaged in the
container of your choice.

C++
---
C++ serializes from/to a dynamic\_map, which is a mapping to the specified
dynamic\_type. A header and source set of libraries which are generated which must
be compiled with the application.

The packages are resolved into namespaces.

The namespace 'metalang' is pre-defined and generated with the required stub
code.

Message Files
=============
Example File:

  package foobar
    message foo
      bool ok
      list list
      object someobject
    end

    message bar
      string name
    end
  end

The message definitions follow a simplistic grammar (defined in
metalang/grammar.py) using pyparsing.
