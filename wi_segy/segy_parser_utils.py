import segyio
import openvds
import re

class SegyParserUtils:
    def __init__(self, segfile, parse_type):
        self.parse_type = parse_type
        self.headers = self.parse_text_header(segfile)
    
    def parse_text_header(self, segyfile):
        if self.parse_type == 'segy':
            raw_header = segyfile.text[0]
        elif self.parse_type == 'vds':
            raw_header = segyfile.getMetadata("SEGY", "TextHeader", openvds.core.MetadataType.BLOB).decode('cp500')
        raw_header = segyio.tools.wrap(raw_header)
        lines = raw_header.split('\n')
        # lines = re.split(r"C\s*\d+", raw_header)
        clean_header = {}
        for i, line in enumerate(lines):
            key = "C" + str(i + 1).rjust(2, '0')
            match = re.search(r"\d+\s+(.*)", line)
            if match:
                line = match.group(1)
            clean_header[key] = line.strip()
        return clean_header   

    def regex_str_attr(self, attr):
        for c in self.headers:
            line = self.headers[c]
            if attr in line:
                m = re.match(f"^.*{attr}\s*:?\s+(\S+).*$", line)
                if m:
                    return m.group(1)
        return None

    def regex_number_attr(self, attr, reg=None):
        if reg == None:
            reg = attr
        for c in self.headers:
            line = self.headers[c]
            if attr in line:
                m = re.match(f"^.*{reg}\s*:?\s+(-?\d+.?\d+).*$", line)
                if m:
                    return self.convert_to_number(m.group(1))
        return None

    def convert_to_number(self, string):
        try:
            number = int(string)
            return number
        except ValueError:
            try:
                number = float(string)
                return number
            except ValueError:
                return None
    
    def utm_to_latlng(self, zone, easting, northing, northernHemisphere=True):
        if not northernHemisphere:
            northing = 10000000 - northing

        a = 6378137
        e = 0.081819191
        e1sq = 0.006739497
        k0 = 0.9996

        arc = northing / k0
        mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

        ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

        ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

        cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
        cc = 151 * math.pow(ei, 3) / 96
        cd = 1097 * math.pow(ei, 4) / 512
        phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

        n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

        r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
        fact1 = n0 * math.tan(phi1) / r0

        _a1 = 500000 - easting
        dd0 = _a1 / (n0 * k0)
        fact2 = dd0 * dd0 / 2

        t0 = math.pow(math.tan(phi1), 2)
        Q0 = e1sq * math.pow(math.cos(phi1), 2)
        fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

        fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

        lof1 = _a1 / (n0 * k0)
        lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
        lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
        _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
        _a3 = _a2 * 180 / math.pi

        latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

        if not northernHemisphere:
            latitude = -latitude

        longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

        return (latitude, longitude)
