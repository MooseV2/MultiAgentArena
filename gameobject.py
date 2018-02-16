import weakref
class GameObject:
  _instances = set()
  def __init__(self):
    self._instances.add(weakref.ref(self))
    self.id = len(list(self.getinstances()))

  def update(self):
    pass
  
  @classmethod
  def getinstances(cls, exclude=None):
    dead = set()
    for ref in cls._instances:
      obj = ref()
      if obj is not None:
        if obj is not exclude and isinstance(obj, cls):
          yield obj
      else:
        dead.add(ref)
    cls._instances -= dead

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.id}>'