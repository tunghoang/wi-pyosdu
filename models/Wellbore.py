from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class Wellbore(Record):
  def __init__(self, wellboreId, name, description):
    super().__init__(
      OSDU_KINDS['Wellbore'], 
      id=f"{OSDU_ID_PREFIXES['Wellbore']}:{wellboreId}", 
      data = {
        "FacilityName": wellboreId, 
        "FacilityID": wellboreId,
        "FacilityDescription": description
      }
  )
