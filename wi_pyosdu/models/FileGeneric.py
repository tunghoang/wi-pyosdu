from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class FileGeneric(Record):
  def __init__(self, filesource, name):
    super().__init__(OSDU_KINDS['FileGeneric'], id=f"{OSDU_ID_PREFIXES['FileGeneric']}:{name}", data = {
      "DatasetProperties": {
        "FileSourceInfo": {
          "FileSource": filesource,
          "Name": name
        },
      }
    })
