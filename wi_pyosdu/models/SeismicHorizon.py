from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class SeismicHorizon(Record):
  def __init__(self, bin_grid_id, horizon_id):
    super().__init__(
      OSDU_KINDS['SeismicHorizon'], 
      id=f"{OSDU_ID_PREFIXES['SeismicHorizon']}:{bin_grid_id}.{horizon_id}", 
      data = {
        "BinGridID": f"{OSDU_ID_PREFIXES['SeismicBinGrid']}:{bin_grid_id}:", 
        "Name": horizon_id
      }
  )
