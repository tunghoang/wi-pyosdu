from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class SeismicBinGrid(Record):
  def __init__(self, bin_grid_id):
    super().__init__(
      OSDU_KINDS['SeismicBinGrid'], 
      id=f"{OSDU_ID_PREFIXES['SeismicBinGrid']}:{bin_grid_id}", 
      data = {
        "BinGridName": bin_grid_id, 
        "BinGridTypeID": 'osdu:reference-data--SeismicBinGridType:Proc:',
        "Name": bin_grid_id
      }
  )
