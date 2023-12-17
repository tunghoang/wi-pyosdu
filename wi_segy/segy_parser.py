from .segy_parser_utils import SegyParserUtils
import segyio
import numpy as np
import math
import openvds

class SeismicParser:
    def __init__(self, segfile):
        if type(segfile) == openvds.core.VolumeDataLayout:
            parse_type = 'vds'
            self.axis_descs = [segfile.getAxisDescriptor(dim) for dim in range(segfile.dimensionality)]
            self.axis_names = [desc.name for desc in self.axis_descs]
        else:
            parse_type = 'segy'
        self.seg = segfile
        self.parse_type = parse_type
        self.utils = SegyParserUtils(segfile, parse_type)
    
    def get_source_x(self, minmax):
        return self.utils.regex_number_attr('X', minmax)

    def get_source_y(self, minmax):
        return self.utils.regex_number_attr('Y', minmax)

    def get_lat(self, minmax):
        return self.utils.regex_number_attr('Lat', minmax)

    def get_long(self, minmax):
        return self.utils.regex_number_attr('Long', minmax)

    def get_zone(self):
        return self.utils.regex_number_attr('Zone')
    
    def get_crs(self):
        return self.utils.regex_str_attr('CRS')
    
    def get_name(self):
        return self.utils.regex_str_attr('Name')
    
    def get_scale_factor(self):
        return self.utils.regex_number_attr('Coordinate scale factor')

    def get_type(self):
        sei_type = self.utils.regex_str_attr('Type')
        if sei_type not in ['2D', '3D']:
            raise Exception('Type not valid')
        return sei_type
        
    def get_sample_domain(self):
        for c in self.utils.headers:
            line = self.utils.headers[c]
            if 'Time' in line:
                return 'Time'
            elif 'Depth' in line:
                return 'Depth'
        return None
    
    def get_sample_header(self, minmax):
        domain = self.get_sample_domain()
        if not domain:
            return None
        return self.utils.regex_number_attr(domain, minmax)
    
    def get_first_iline_header(self):
        return self.utils.regex_number_attr('First', 'inline')
        
    def get_last_iline_header(self):
        return self.utils.regex_number_attr('Last', 'inline')
        
    def get_first_xline_header(self):
        return self.utils.regex_number_attr('First', 'xline')

    def get_last_xline_header(self):
        return self.utils.regex_number_attr('Last', 'xline')
        
    def get_first_sample(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.sample() in self.axis_names:
                    raise Exception("VDS does not have sample axis")
                sample_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.sample())]
                return -sample_axis.coordinateMin
            return -self.seg.samples[0].item()
        except:
            return None
        
    def get_last_sample(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.sample() in self.axis_names:
                    raise Exception("VDS does not have sample axis")
                sample_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.sample())]
                return -sample_axis.coordinateMax
            return -self.seg.samples[-1].item()
        except:
            return None
    
    def get_sample_interval(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.sample() in self.axis_names:
                    raise Exception("VDS does not have sample axis")
                sample_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.sample())]
                return sample_axis.coordinateStep
            return (self.seg.samples[1] - self.seg.samples[0]).item()
        except:
            return None
    
    def get_first_iline(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.inline() in self.axis_names:
                    raise Exception("VDS does not have inline axis")                
                inline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.inline())]
                return inline_axis.coordinateMin
            return self.seg.ilines[0].item()
        except:
            return None
    
    def get_last_iline(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.inline() in self.axis_names:
                    raise Exception("VDS does not have inline axis")                
                inline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.inline())]
                return inline_axis.coordinateMax
            return self.seg.ilines[-1].item()
        except:
            return None
        
    def get_iline_step(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.inline() in self.axis_names:
                    raise Exception("VDS does not have inline axis")                
                inline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.inline())]
                return inline_axis.coordinateStep
            return (self.seg.ilines[1] - self.seg.ilines[0]).item()
        except:
            return None
    
    def get_vector2_iline_interval(self):
        try:
            if self.parse_type == 'vds':
                inline_spacing = self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemInlineSpacing())
                a = inline_spacing[0]
                b = inline_spacing[1]
            else:
                trace1 = self.seg.header[0]
                trace2 = self.seg.header[self.seg.xlines.size]
                x1 = trace1[segyio.TraceField.SourceX]
                y1 = trace1[segyio.TraceField.SourceY]
                x2 = trace2[segyio.TraceField.SourceX]
                y2 = trace2[segyio.TraceField.SourceY]
                a = x2 - x1
                b = y2 - y1
            return [a, b]
        except:
            return None
    
    def get_iline_interval(self):
        try:
            if self.parse_type == 'vds':
                inline_spacing = self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemInlineSpacing())
                a = inline_spacing[0]
                b = inline_spacing[1]
            else:
                trace_1 = self.seg.header[0]
                trace_2 = self.seg.header[self.seg.xlines.size]
                x1 = trace_1[segyio.TraceField.SourceX]
                y1 = trace_1[segyio.TraceField.SourceY]
                x2 = trace_2[segyio.TraceField.SourceX]
                y2 = trace_2[segyio.TraceField.SourceY]
                a = x2 - x1
                b = y2 - y1
            return math.sqrt(a**2 + b**2)
        except:
            return None
    
    def get_first_xline(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.crossline() in self.axis_names:
                    raise Exception("VDS does not have crossline axis")
                crossline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.crossline())]
                return crossline_axis.coordinateMin
            return self.seg.xlines[0].item()
        except:
            return None
        
    def get_last_xline(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.crossline() in self.axis_names:
                    raise Exception("VDS does not have crossline axis")
                crossline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.crossline())]
                return crossline_axis.coordinateMax
            return self.seg.xlines[-1].item()
        except:
            return None
    
    def get_xline_step(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.crossline() in self.axis_names:
                    raise Exception("VDS does not have crossline axis")
                crossline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.crossline())]
                return crossline_axis.coordinateStep
            return (self.seg.xlines[1] - self.seg.xlines[0]).item()
        except:
            return None
    
    def get_vector2_xline_interval(self):
        try:
            if self.parse_type == 'vds':
                crossline_spacing = self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemCrosslineSpacing())
                a = crossline_spacing[0]
                b = crossline_spacing[1]
            else:
                trace_1 = self.seg.header[0]
                trace_2 = self.seg.header[1]
                x1 = trace_1[segyio.TraceField.SourceX]
                y1 = trace_1[segyio.TraceField.SourceY]
                x2 = trace_2[segyio.TraceField.SourceX]
                y2 = trace_2[segyio.TraceField.SourceY]
                a = x2 - x1
                b = y2 - y1
            return [a, b]
        except:
            return None
    
    def get_xline_interval(self):
        try:
            if self.parse_type == 'vds':
                crossline_spacing = self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemCrosslineSpacing())
                a = crossline_spacing[0]
                b = crossline_spacing[1]
            else:
                trace_1 = self.seg.header[0]
                trace_2 = self.seg.header[1]
                x1 = trace_1[segyio.TraceField.SourceX]
                y1 = trace_1[segyio.TraceField.SourceY]
                x2 = trace_2[segyio.TraceField.SourceX]
                y2 = trace_2[segyio.TraceField.SourceY]
                a = x2 - x1
                b = y2 - y1
            return math.sqrt(a**2 + b**2)
        except:
            return None
    
    def get_rotation(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.inline() in self.axis_names or not openvds.KnownAxisNames.crossline() in self.axis_names:
                    raise Exception("VDS does not have inline and crossline axes")
                inline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.inline())]
                crossline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.crossline())]
                grid_corners = [(inline_axis.coordinateMin, crossline_axis.coordinateMin),
                               (inline_axis.coordinateMin, crossline_axis.coordinateMax)]

                origin = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemOrigin()))
                inline_spacing = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemInlineSpacing()))
                crossline_spacing = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemCrosslineSpacing()))
                corner_points = [origin + inline_spacing * inline + crossline_spacing * crossline for (inline, crossline) in grid_corners]
                a = corner_points[1][0] - corner_points[0][0]
                b = corner_points[1][1] - corner_points[0][1]
            else:
                trace_1 = self.seg.header[0]
                trace_2 = self.seg.header[self.seg.xlines.size - 1]
                x1 = trace_1[segyio.TraceField.SourceX]
                y1 = trace_1[segyio.TraceField.SourceY]
                x2 = trace_2[segyio.TraceField.SourceX]
                y2 = trace_2[segyio.TraceField.SourceY]
                a = x2 - x1
                b = y2 - y1
            if b == 0:
                return 90
            return math.degrees(math.atan(a / b))
        except:
            return None
    
    def get_vertices(self):
        try:
            if self.parse_type == 'vds':
                if not openvds.KnownAxisNames.inline() in self.axis_names or not openvds.KnownAxisNames.crossline() in self.axis_names:
                    raise Exception("VDS does not have inline and crossline axes")
                inline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.inline())]
                crossline_axis = self.axis_descs[self.axis_names.index(openvds.KnownAxisNames.crossline())]
                grid_corners = [(inline_axis.coordinateMin, crossline_axis.coordinateMin),
                                (inline_axis.coordinateMin, crossline_axis.coordinateMax),
                                (inline_axis.coordinateMax, crossline_axis.coordinateMax),
                                (inline_axis.coordinateMax, crossline_axis.coordinateMin)]

                origin = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemOrigin()))
                inline_spacing = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemInlineSpacing()))
                crossline_spacing = np.array(self.seg.getMetadata(openvds.KnownMetadata.surveyCoordinateSystemCrosslineSpacing()))
                corner_points = [(origin + inline_spacing * inline + crossline_spacing * crossline).tolist() for (inline, crossline) in grid_corners]
                return corner_points
            else:
                iline_size = self.seg.ilines.size
                xline_size = self.seg.xlines.size
                trace1 = self.seg.header[0]
                trace2 = self.seg.header[xline_size - 1]
                trace3 = self.seg.header[-1]
                trace4 = self.seg.header[xline_size * (iline_size - 1)]
                return [[trace1[segyio.TraceField.SourceX], trace1[segyio.TraceField.SourceY]],
                        [trace2[segyio.TraceField.SourceX], trace2[segyio.TraceField.SourceY]],
                        [trace3[segyio.TraceField.SourceX], trace3[segyio.TraceField.SourceY]],
                        [trace4[segyio.TraceField.SourceX], trace4[segyio.TraceField.SourceY]]]
        except:
            return None
