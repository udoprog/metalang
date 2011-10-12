class FieldDeclMetaclass(type):
  def __init__(cls, name, bases, dct):
    for b in bases:
      b.types[cls.__fieldname__] = cls
    super(FieldDeclMetaclass, cls).__init__(name, bases, dct)

class FieldDecl:
  __metaclass__ = FieldDeclMetaclass
  __fieldname__ = None

  types = {}

  def __init__(self, t, n, line=None, text=None):
    self.field_type = t
    self.name = n
    self.line = line
    self.text = text

  @classmethod
  def register(klass, newklass):
    klass.types[newklass.__fieldname__] = newklass

  @classmethod
  def get(klass, fieldname):
    return klass.types[fieldname]

  def __repr__(self):
    return "<" + self.__class__.__name__ + " name='{1}'>".format(self.field_type, self.name)

class BoolDecl(FieldDecl):
  __fieldname__ = "bool"

class StringDecl(FieldDecl):
  __fieldname__ = "string"

class IntDecl(FieldDecl):
  __fieldname__ = "int"

class ListDecl(FieldDecl):
  __fieldname__ = "list"

class ObjectDecl(FieldDecl):
  __fieldname__ = "object"

class MessageDecl:
  def __init__(self, name, fields, line=None, text=None):
    self.name = name
    self.fields = fields
    self.line = line
    self.text = text

  def __repr__(self):
    return "<MessageDecl name='{0}' fields={1}>".format(self.name, self.fields)

class PackageDecl:
  def __init__(self, name, messages, line=None, text=None):
    self.name = name
    self.messages = dict()
    self.line = line
    self.text = text

    for m in messages:
      if m.name in self.messages:
        raise RuntimeError, "Duplicate message '{0}' in package '{1}'".format(m.name, self.name)
      self.messages[m.name] = m

  def __repr__(self):
    return "<PackageDecl name='{0}' messages={1}>".format(self.name, self.messages)
