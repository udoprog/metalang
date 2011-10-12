class base_metaclass(type):
  def __init__(cls, name, bases, dct):
    for b in bases:
      if not hasattr(b, "__types__"):
        continue
      b.__types__[cls.__classname__] = cls
      break
    super(base_metaclass, cls).__init__(name, bases, dct)

class base:
  __metaclass__ = base_metaclass
  __classname__ = None
  __keys__      = []
  __types__     = dict()

  @classmethod
  def from_dict(klass, dct):
    def from_list(lst):
      l = list()
      for v in lst:
        if isinstance(v, list):
          l.append(from_list(v))
        elif isinstance(v, base):
          l.append(from_dict(v))
        else:
          l.append(v)
      return l

    def from_dict(dct):
      if "__class__" not in dct:
        raise RuntimeError, "Dict does not contain required key '__class__'"

      inst = klass.__types__.get(dct["__class__"])()

      for k,v in dct.items():
        if k.startswith("__"):
          continue
        if k not in inst.__keys__:
          continue
        if isinstance(v, list):
          setattr(inst, k, from_list(v))
        elif isinstance(v, dict):
          setattr(inst, k, from_dict(v))
        else:
          setattr(inst, k, v)

      return inst

    return from_dict(dct)

  def to_dict(self):
    if self.__classname__ is None:
      raise RuntimeError, "Cannot create dict from non inherited 'base' object"
    
    def to_list(lst):
      l = list()
      for v in lst:
        if isinstance(v, list):
          l.append(to_list(v))
        elif isinstance(v, base):
          l.append(to_dict(v))
        else:
          l.append(v)
      return l

    def to_dict(self):
      dct = dict()
      dct["__class__"] = self.__classname__
      for n in self.__keys__:
        if not hasattr(self, n):
          continue
        v = getattr(self,n)
        if isinstance(v, list):
          dct[n] = to_list(v)
        elif isinstance(v, base):
          dct[n] = v.to_dict()
        else:
          dct[n] = v
      return dct

    return to_dict(self)
