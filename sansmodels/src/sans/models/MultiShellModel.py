#!/usr/bin/env python
"""
	This software was developed by the University of Tennessee as part of the
	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
	project funded by the US National Science Foundation.

	If you use DANSE applications to do scientific research that leads to
	publication, we ask that you acknowledge the use of the software with the
	following sentence:

	"This work benefited from DANSE software developed under NSF award DMR-0520547."

	copyright 2008, University of Tennessee
"""

""" Provide functionality for a C extension model

	WARNING: THIS FILE WAS GENERATED BY WRAPPERGENERATOR.PY
 	         DO NOT MODIFY THIS FILE, MODIFY ..\c_extensions\multishell.h
 	         AND RE-RUN THE GENERATOR SCRIPT

"""

from sans.models.BaseComponent import BaseComponent
from sans_extension.c_models import CMultiShellModel
import copy    
    
class MultiShellModel(CMultiShellModel, BaseComponent):
    """ Class that evaluates a MultiShellModel model. 
    	This file was auto-generated from ..\c_extensions\multishell.h.
    	Refer to that file and the structure it contains
    	for details of the model.
    	List of default parameters:
         scale           = 1.0 
         core_radius     = 60.0 [A]
         s_thickness     = 10.0 [A]
         w_thickness     = 10.0 [A]
         core_sld        = 6.4e-006 [1/A�]
         shell_sld       = 4e-007 [1/A�]
         n_pairs         = 2.0 
         background      = 0.0 [1/cm]

    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        CMultiShellModel.__init__(self)
        
        ## Name of the model
        self.name = "MultiShellModel"
        ## Model description
        self.description ="""
		Model parameters:
		scale : scale factor
		core_radius : Core radius of the multishell
		s_thickness: shell thickness
		w_thickness: water thickness
		core_sld: core scattering length density
		shell_sld: shell scattering length density
		n_pairs:number of pairs of water/shell
		background: incoherent background"""
       
		## Parameter details [units, min, max]
        self.details = {}
        self.details['scale'] = ['', None, None]
        self.details['core_radius'] = ['[A]', None, None]
        self.details['s_thickness'] = ['[A]', None, None]
        self.details['w_thickness'] = ['[A]', None, None]
        self.details['core_sld'] = ['[1/A�]', None, None]
        self.details['shell_sld'] = ['[1/A�]', None, None]
        self.details['n_pairs'] = ['', None, None]
        self.details['background'] = ['[1/cm]', None, None]

		## fittable parameters
        self.fixed=['radius.width']
        
        ## parameters with orientation
        self.orientation_params =[]
   
    def clone(self):
        """ Return a identical copy of self """
        return self._clone(MultiShellModel())   
   
    def run(self, x = 0.0):
        """ Evaluate the model
            @param x: input q, or [q,phi]
            @return: scattering function P(q)
        """
        
        return CMultiShellModel.run(self, x)
   
    def runXY(self, x = 0.0):
        """ Evaluate the model in cartesian coordinates
            @param x: input q, or [qx, qy]
            @return: scattering function P(q)
        """
        
        return CMultiShellModel.runXY(self, x)
        
    def set_dispersion(self, parameter, dispersion):
        """
            Set the dispersion object for a model parameter
            @param parameter: name of the parameter [string]
            @dispersion: dispersion object of type DispersionModel
        """
        return CMultiShellModel.set_dispersion(self, parameter, dispersion.cdisp)
        
   
# End of file
