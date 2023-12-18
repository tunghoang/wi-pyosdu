from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record
class SeismicTraceData(Record):
  def __init__(self, bin_grid_id, trace_data_id):
    super().__init__(
      OSDU_KINDS['SeismicTraceData'], 
      id=f"{OSDU_ID_PREFIXES['SeismicTraceData']}:{bin_grid_id}.{trace_data_id}", 
      data = {
        "Name": trace_data_id,
        "BinGridID": f"{OSDU_ID_PREFIXES['SeismicBinGrid']}:{bin_grid_id}:", 
      }
    )
