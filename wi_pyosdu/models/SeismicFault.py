from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class SeismicFault(Record):
  def __init__(self, bin_grid_id, fault_id):
    super().__init__(
      OSDU_KINDS['SeismicFault'], 
      id=f"{OSDU_ID_PREFIXES['SeismicFault']}:{bin_grid_id}.{fault_id}", 
      data = {
        "BinGridID": f"{OSDU_ID_PREFIXES['SeismicBinGrid']}:{bin_grid_id}:", 
        "Name": fault_id
      }
  )
