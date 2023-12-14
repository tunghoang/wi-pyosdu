from .utils import OSDU_KINDS, OSDU_ID_PREFIXES
from .Record import Record

class Well(Record):
  def __init__(self, wellId, name, description, basinId=None):
    super().__init__(OSDU_KINDS['Well'], id = f'{OSDU_ID_PREFIXES["Well"]}:{wellId}', data = {
      "FacilityID": wellId, 
      "FacilityName": name, 
      "FacilityDescription": description,
      "VerticalMeasurements": [{
        "VerticalMeasurementID": f"{name}-VerticalMeasurementID",
        "VerticalMeasurement": 12345.6,
        "VerticalMeasurementTypeID": "osdu:reference-data--VerticalMeasurementType:PBD:",
        "VerticalMeasurementPathID": "osdu:reference-data--VerticalMeasurementPath:MD:",
        "VerticalMeasurementSourceID": "osdu:reference-data--VerticalMeasurementSource:DRL:",
        "VerticalMeasurementUnitOfMeasureID": "osdu:reference-data--UnitOfMeasure:m:",
        "VerticalCRSID": "osdu:reference-data--CoordinateReferenceSystem:BoundProjected:EPSG::32021_EPSG::15851:",
        "VerticalReferenceID": f"{name}-VerticalReferenceID",
        "VerticalMeasurementDescription": "Example VerticalMeasurementDescription"
      }]
    })
