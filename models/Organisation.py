from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record

class Organisation(Record):
  def __init__(self, orgId, name, description):
    super().__init__(
      OSDU_KINDS["Organisation"], 
      id = f'{OSDU_ID_PREFIXES["Organisation"]}:{orgId}', 
      data = {
        'OrganisationID': orgId,
        'OrganisationName': name,
        'OrganisationDescription': description
      }
    )
