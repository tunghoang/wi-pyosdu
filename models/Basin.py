from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class Basin(Record):
  def __init__(self, basinId, name, description):
    super().__init__(OSDU_KINDS['Basin'], id=f"{OSDU_ID_PREFIXES['Basin']}:{basinId}", data = {"BasinID": basinId, "BasinName": name, "BasinDescription": description})
