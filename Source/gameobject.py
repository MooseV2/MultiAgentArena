import weakref
class GameObject:
  _instances = set()
  _idcount = 10
  def __init__(self):
    self._instances.add(weakref.ref(self))
    self.id = GameObject._idcount
    GameObject._idcount += 1

  def update(self):
    pass
  
  @classmethod
  def getinstances(cls, exclude=None):
    for ref in cls._instances:
      obj = ref()
      if obj is not None:
        if obj is not exclude and isinstance(obj, cls):
          yield obj

  @classmethod
  def clearinstances(cls):
    cls._instances = set()

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.id}>'