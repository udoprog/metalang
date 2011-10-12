def read_template(name):
  import os
  f = open(os.path.join(os.path.dirname(__file__),'data',name),'r')
  try:
    return f.read()
  finally:
    f.close()

class EventEngine:
  def __init__(self):
    self.events = dict()

  def on(self, event, callback):
    try:
      self.events[event].append(callback)
    except KeyError:
      self.events[event] = [callback]

  def trigger(self, event, *args):
    if event not in self.events:
      return
    for callback in self.events[event]:
      callback(*args)

__all__ = ["read_templates", "EventEngine"]
