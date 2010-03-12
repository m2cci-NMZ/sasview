"""
    Adapters for fitting module
"""
from danse.common.plottools.plottables import Data1D as PlotData1D
from danse.common.plottools.plottables import Data2D as PlotData2D
from danse.common.plottools.plottables import Theory1D as PlotTheory1D

from DataLoader.data_info import Data1D as LoadData1D
from DataLoader.data_info import Data2D as LoadData2D

import copy

class Data1D(PlotData1D, LoadData1D):
    
    def __init__(self,x=[],y=[],dx=None,dy=None):
        PlotData1D.__init__(self, x, y, dx, dy)
        LoadData1D.__init__(self, x, y, dx, dy)
        self.id= None
        self.group_id =None
        self.is_data = True
    
    def copy_from_datainfo(self, data1d):
        """
            copy values of Data1D of type DataLaoder.Data_info
        """
        self.x  = copy.deepcopy(data1d.x)
        self.dx = copy.deepcopy(data1d.dx)
        self.y  = copy.deepcopy(data1d.y)
        self.dy = copy.deepcopy(data1d.dy)
        self.dxl = copy.deepcopy(data1d.dxl)
        self.dxw = copy.deepcopy(data1d.dxw)
    
        self.xaxis(data1d._xaxis,data1d._xunit)
        self.yaxis(data1d._yaxis,data1d._yunit)
        
    def __str__(self):
        """
            print data
        """
        _str = "%s\n" % LoadData1D.__str__(self)
      
        return _str 
class Theory1D(PlotTheory1D,LoadData1D):
    
    def __init__(self,x=[],y=[],dy=None):
        PlotTheory1D.__init__(self, x, y, dy)
        LoadData1D.__init__(self, x, y, dy)
        self.id= None
        self.group_id =None
        self.is_data = True
    
    def copy_from_datainfo(self, data1d):
        """
            copy values of Data1D of type DataLaoder.Data_info
        """
        self.x  = copy.deepcopy(data1d.x)
        self.y  = copy.deepcopy(data1d.y)
        self.dy = copy.deepcopy(data1d.dy)
   
        self.xaxis(data1d._xaxis,data1d._xunit)
        self.yaxis(data1d._yaxis,data1d._yunit)
    def __str__(self):
        """
            print data
        """
        _str = "%s\n" % LoadData1D.__str__(self)
      
        return _str 
      
class Data2D(PlotData2D,LoadData2D):
    def __init__(self,image=None,err_image=None,xmin=None,xmax=None,ymin=None,ymax=None,zmin=None,zmax=None):
        
        PlotData2D.__init__(self, image=image, err_image=err_image,xmin=xmin, xmax=xmax,
                            ymin=ymin, ymax=ymax)
        
        LoadData2D.__init__(self,data=image, err_data=err_image, qx_data=None,qy_data=None,q_data=None,mask=None)
        
    def copy_from_datainfo(self, data2d):
        """
            copy value of Data2D of type DataLoader.data_info
        """
        self.data     =  copy.deepcopy(data2d.data)
        self.qx_data     =  copy.deepcopy(data2d.qx_data)
        self.qy_data     =  copy.deepcopy(data2d.qy_data)
        self.q_data     =  copy.deepcopy(data2d.q_data)
        self.mask     =  copy.deepcopy(data2d.mask)
        self.err_data =  copy.deepcopy(data2d.err_data)
        self.x_bins     = copy.deepcopy(data2d.x_bins)
        self.y_bins     = copy.deepcopy(data2d.y_bins)
        
        self.xmin       = data2d.xmin
        self.xmax       = data2d.xmax
        self.ymin       = data2d.ymin
        self.ymax       = data2d.ymax
        
        self.xaxis(data2d._xaxis,data2d._xunit)
        self.yaxis(data2d._yaxis,data2d._yunit)
        
    def __str__(self):
        """
            print data
        """
        _str = "%s\n" % LoadData2D.__str__(self)
      
        return _str 
        