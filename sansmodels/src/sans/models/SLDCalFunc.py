#!/usr/bin/env python

##############################################################################
#	This software was developed by the University of Tennessee as part of the
#	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
#	project funded by the US National Science Foundation.
#
#	If you use DANSE applications to do scientific research that leads to
#	publication, we ask that you acknowledge the use of the software with the
#	following sentence:
#
#	"This work benefited from DANSE software developed under NSF award DMR-0520547."
#
#	copyright 2008, University of Tennessee
##############################################################################


""" 
Provide functionality for a C extension model

:WARNING: THIS FILE WAS GENERATED BY WRAPPERGENERATOR.PY
         DO NOT MODIFY THIS FILE, MODIFY ../c_extensions/sld_cal.h
         AND RE-RUN THE GENERATOR SCRIPT

"""

from sans.models.BaseComponent import BaseComponent
from sans.models.sans_extension.c_models import CSLDCalFunc
import copy    

def create_SLDCalFunc():
    obj = SLDCalFunc()
    #CSLDCalFunc.__init__(obj) is called by SLDCalFunc constructor
    return obj

class SLDCalFunc(CSLDCalFunc, BaseComponent):
    """ 
    Class that evaluates a SLDCalFunc model. 
    This file was auto-generated from ../c_extensions/sld_cal.h.
    Refer to that file and the structure it contains
    for details of the model.
    List of default parameters:
         fun_type        = 0.0 
         npts_inter      = 21.0 
         shell_num       = 0.0 
         nu_inter        = 2.5 
         sld_left        = 0.0 [1/A^(2)]
         sld_right       = 0.0 [1/A^(2)]

    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        #apply(CSLDCalFunc.__init__, (self,)) 
        CSLDCalFunc.__init__(self)
        
        ## Name of the model
        self.name = "SLDCalFunc"
        ## Model description
        self.description ="""To calculate sld values"""
       
        ## Parameter details [units, min, max]
        self.details = {}
        self.details['fun_type'] = ['', None, None]
        self.details['npts_inter'] = ['', None, None]
        self.details['shell_num'] = ['', None, None]
        self.details['nu_inter'] = ['', None, None]
        self.details['sld_left'] = ['[1/A^(2)]', None, None]
        self.details['sld_right'] = ['[1/A^(2)]', None, None]

        ## fittable parameters
        self.fixed=['</text>']
        
        ## non-fittable parameters
        self.non_fittable = []
        
        ## parameters with orientation
        self.orientation_params = []

    def __setstate__(self, state):
        """
        restore the state of a model from pickle
        """
        self.__dict__, self.params, self.dispersion = state
        
    def __reduce_ex__(self, proto):
        """
        Overwrite the __reduce_ex__ of PyTypeObject *type call in the init of 
        c model.
        """
        state = (self.__dict__, self.params, self.dispersion)
        return (create_SLDCalFunc,tuple(), state, None, None)
        
    def clone(self):
        """ Return a identical copy of self """
        return self._clone(SLDCalFunc())   
       	
   
    def run(self, x=0.0):
        """ 
        Evaluate the model
        
        :param x: input q, or [q,phi]
        
        :return: scattering function P(q)
        
        """
        
        return CSLDCalFunc.run(self, x)
   
    def runXY(self, x=0.0):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q, or [qx, qy]
        
        :return: scattering function P(q)
        
        """
        
        return CSLDCalFunc.runXY(self, x)
        
    def evalDistribution(self, x=[]):
        """ 
        Evaluate the model in cartesian coordinates
        
        :param x: input q[], or [qx[], qy[]]
        
        :return: scattering function P(q[])
        
        """
        return CSLDCalFunc.evalDistribution(self, x)
        
    def calculate_ER(self):
        """ 
        Calculate the effective radius for P(q)*S(q)
        
        :return: the value of the effective radius
        
        """       
        return CSLDCalFunc.calculate_ER(self)
        
    def set_dispersion(self, parameter, dispersion):
        """
        Set the dispersion object for a model parameter
        
        :param parameter: name of the parameter [string]
        :param dispersion: dispersion object of type DispersionModel
        
        """
        return CSLDCalFunc.set_dispersion(self, parameter, dispersion.cdisp)
        
   
# End of file
