#!/usr/bin/env python
""" 
    Provide F(x) = 1/( scale + c1*(x)^(2)+  c2*(x)^(4)) + bkd
    Teubner-Strey function as a BaseComponent model
    
"""

from sans.models.BaseComponent import BaseComponent
import math

class TeubnerStreyModel(BaseComponent):
   
    """
        Class that evaluates  the TeubnerStrey model.
        
        F(x) = 1/( scale + c1*(x)^(2)+  c2*(x)^(4)) + bkd
        
        The model has Four parameters: 
            scale  =  scale factor
            c1     =  constant
            c2     =  constant
            bkd    =  incoherent background
    """
        
    def __init__(self):
        """ Initialization """
        
        # Initialize BaseComponent first, then sphere
        BaseComponent.__init__(self)
        
        ## Name of the model
        self.name = "Teubner Strey"

        ## Define parameters
        self.params = {}
        self.params['c1']     = -30.0
        self.params['c2']     = 5000.0
        self.params['scale']  = 0.1
        self.params['bkd']    = 0.1

        ## Parameter details [units, min, max]
        self.details = {}
        self.details['c1']    = ['', None, None ]
        self.details['c2']    = ['', None, None ]
        self.details['scale'] = ['', None, None]
        self.details['bkd']   = ['cm^{-1}', None, None]
    
               
    def _TeubnerStrey(self, x):
        """
            Evaluate  F(x) = 1/( scale + c1*(x)^(2)+  c2*(x)^(4)) + bkd
           
        """
        return 1/( self.params['scale']+ self.params['c1'] * math.pow(x ,2)\
                + self.params['c2'] * math.pow(x ,4) ) + self.params['bkd']
       
   
    def run(self, x = 0.0):
        """ Evaluate the model
            @param x: simple value
            @return: (PowerLaw value)
        """
        if x.__class__.__name__ == 'list':
            return self._TeubnerStrey(x[0]*math.cos(x[1]))\
             *self._TeubnerStrey(x[0]*math.sin(x[1]))
        elif x.__class__.__name__ == 'tuple':
            raise ValueError, "Tuples are not allowed as input to BaseComponent models"
        else:
            return self._TeubnerStrey(x)
   
    def runXY(self, x = 0.0):
        """ Evaluate the model
            @param x: simple value
            @return: PowerLaw value
        """
        if x.__class__.__name__ == 'list':
            return self._TeubnerStrey(x[0])*self._TeubnerStrey(x[1])
        elif x.__class__.__name__ == 'tuple':
            raise ValueError, "Tuples are not allowed as input to BaseComponent models"
        else:
            return self._TeubnerStrey(x)
        
    def TeubnerStreyLengths(self):
        """
            Calculate the correlation length (L) 
            @return L: the correlation distance 
        """
        if (self.params['c2'] !=0) and \
        ((2*math.pow(self.params['scale'],1/2)+self.params['c1'])>= 0):
            L =  math.pow( 1/2 * math.pow( (self.params['scale']/self.params['c2']), 1/2 )\
                            +(self.params['c1']/(4*self.params['c2'])),-1/2 )
            return L
        else:
            return False
    def TeubnerStreyDistance(self):
        """
            Calculate the quasi-periodic repeat distance (D/(2*pi)) 
            @return D: quasi-periodic repeat distance
        """
        if (self.params['c2'] !=0) and \
        ((2*math.pow(self.params['scale'],1/2)-self.params['c1'])>= 0):
            D =  math.pow( 1/2 * math.pow( (self.params['scale']/self.params['c2']), 1/2 )\
                            -(self.params['c1']/(4*self.params['c2'])),-1/2 )
            return D
        else:
            return False
