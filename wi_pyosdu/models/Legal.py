class Legal:
  legaltags = ['osdu-pvn-legal']
  otherRelevantDataCountries = ['VN']

  def __init__(self, legaltags = [], otherRelevantDataCountries = []):
    self.legaltags = self.legaltags + legaltags
    self.otherRelevantDataCountries = self.otherRelevantDataCountries + otherRelevantDataCountries
