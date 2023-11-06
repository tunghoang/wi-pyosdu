from .Legal import Legal
from .Acl import Acl
import json

class Record:
  id = None
  kind = None
  acl = None
  legal = None
  data = None

  required_fields = ['kind', 'acl', 'legal']

  def __init__(self, kind, id=None, legal:Legal = Legal(), acl:Acl = Acl(), data = {}):
    self.id = id
    self.kind = kind
    self.acl = acl
    self.legal = legal
    self.data = data

  def is_completed(self):
    self_dict = vars(self)
    for f in self.required_fields:
      if self_dict[f] is None:
        return False
    return True
  def todict(self):
    return json.loads(self.tojson())
  def tojson(self):
    return json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)), ensure_ascii=False)
