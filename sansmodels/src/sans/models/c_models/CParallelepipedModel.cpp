/**
	This software was developed by the University of Tennessee as part of the
	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
	project funded by the US National Science Foundation.

	If you use DANSE applications to do scientific research that leads to
	publication, we ask that you acknowledge the use of the software with the
	following sentence:

	"This work benefited from DANSE software developed under NSF award DMR-0520547."

	copyright 2008, University of Tennessee
 */

/** CParallelepipedModel
 *
 * C extension 
 *
 * WARNING: THIS FILE WAS GENERATED BY WRAPPERGENERATOR.PY
 *          DO NOT MODIFY THIS FILE, MODIFY parallelepiped.h
 *          AND RE-RUN THE GENERATOR SCRIPT
 *
 */
 
extern "C" {
#include <Python.h>
#include "structmember.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "parallelepiped.h"
}

#include "models.hh"
#include "dispersion_visitor.hh"

/// Error object for raised exceptions
static PyObject * CParallelepipedModelError = NULL;


// Class definition
typedef struct {
    PyObject_HEAD
    /// Parameters
    PyObject * params;
    /// Dispersion parameters
    PyObject * dispersion;
    /// Underlying model object
    ParallelepipedModel * model;
    /// Log for unit testing
    PyObject * log;
} CParallelepipedModel;


static void
CParallelepipedModel_dealloc(CParallelepipedModel* self)
{
    self->ob_type->tp_free((PyObject*)self);
    

}

static PyObject *
CParallelepipedModel_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CParallelepipedModel *self;
    
    self = (CParallelepipedModel *)type->tp_alloc(type, 0);
   
    return (PyObject *)self;
}

static int
CParallelepipedModel_init(CParallelepipedModel *self, PyObject *args, PyObject *kwds)
{
    if (self != NULL) {
    	
    	// Create parameters
        self->params = PyDict_New();
        self->dispersion = PyDict_New();
        self->model = new ParallelepipedModel();
        
        // Initialize parameter dictionary
        PyDict_SetItemString(self->params,"scale",Py_BuildValue("d",1.000000));
        PyDict_SetItemString(self->params,"longer_edgeB",Py_BuildValue("d",75.000000));
        PyDict_SetItemString(self->params,"longuest_edgeC",Py_BuildValue("d",400.000000));
        PyDict_SetItemString(self->params,"parallel_phi",Py_BuildValue("d",1.000000));
        PyDict_SetItemString(self->params,"parallel_theta",Py_BuildValue("d",1.000000));
        PyDict_SetItemString(self->params,"background",Py_BuildValue("d",0.000000));
        PyDict_SetItemString(self->params,"short_edgeA",Py_BuildValue("d",35.000000));
        PyDict_SetItemString(self->params,"contrast",Py_BuildValue("d",0.000005));
        // Initialize dispersion / averaging parameter dict
        DispersionVisitor* visitor = new DispersionVisitor();
        PyObject * disp_dict;
        disp_dict = PyDict_New();
        self->model->short_edgeA.dispersion->accept_as_source(visitor, self->model->short_edgeA.dispersion, disp_dict);
        PyDict_SetItemString(self->dispersion, "short_edgeA", disp_dict);
        disp_dict = PyDict_New();
        self->model->longer_edgeB.dispersion->accept_as_source(visitor, self->model->longer_edgeB.dispersion, disp_dict);
        PyDict_SetItemString(self->dispersion, "longer_edgeB", disp_dict);
        disp_dict = PyDict_New();
        self->model->longuest_edgeC.dispersion->accept_as_source(visitor, self->model->longuest_edgeC.dispersion, disp_dict);
        PyDict_SetItemString(self->dispersion, "longuest_edgeC", disp_dict);
        disp_dict = PyDict_New();
        self->model->parallel_phi.dispersion->accept_as_source(visitor, self->model->parallel_phi.dispersion, disp_dict);
        PyDict_SetItemString(self->dispersion, "parallel_phi", disp_dict);
        disp_dict = PyDict_New();
        self->model->parallel_theta.dispersion->accept_as_source(visitor, self->model->parallel_theta.dispersion, disp_dict);
        PyDict_SetItemString(self->dispersion, "parallel_theta", disp_dict);


         
        // Create empty log
        self->log = PyDict_New();
        
        

    }
    return 0;
}

static PyMemberDef CParallelepipedModel_members[] = {
    {"params", T_OBJECT, offsetof(CParallelepipedModel, params), 0,
     "Parameters"},
	{"dispersion", T_OBJECT, offsetof(CParallelepipedModel, dispersion), 0,
	  "Dispersion parameters"},     
    {"log", T_OBJECT, offsetof(CParallelepipedModel, log), 0,
     "Log"},
    {NULL}  /* Sentinel */
};

/** Read double from PyObject
    @param p PyObject
    @return double
*/
double CParallelepipedModel_readDouble(PyObject *p) {
    if (PyFloat_Check(p)==1) {
        return (double)(((PyFloatObject *)(p))->ob_fval);
    } else if (PyInt_Check(p)==1) {
        return (double)(((PyIntObject *)(p))->ob_ival);
    } else if (PyLong_Check(p)==1) {
        return (double)PyLong_AsLong(p);
    } else {
        return 0.0;
    }
}


/**
 * Function to call to evaluate model
 * @param args: input q or [q,phi]
 * @return: function value
 */
static PyObject * run(CParallelepipedModel *self, PyObject *args) {
	double q_value, phi_value;
	PyObject* pars;
	int npars;
	
	// Get parameters
	
	    // Reader parameter dictionary
    self->model->scale = PyFloat_AsDouble( PyDict_GetItemString(self->params, "scale") );
    self->model->longer_edgeB = PyFloat_AsDouble( PyDict_GetItemString(self->params, "longer_edgeB") );
    self->model->longuest_edgeC = PyFloat_AsDouble( PyDict_GetItemString(self->params, "longuest_edgeC") );
    self->model->parallel_phi = PyFloat_AsDouble( PyDict_GetItemString(self->params, "parallel_phi") );
    self->model->parallel_theta = PyFloat_AsDouble( PyDict_GetItemString(self->params, "parallel_theta") );
    self->model->background = PyFloat_AsDouble( PyDict_GetItemString(self->params, "background") );
    self->model->short_edgeA = PyFloat_AsDouble( PyDict_GetItemString(self->params, "short_edgeA") );
    self->model->contrast = PyFloat_AsDouble( PyDict_GetItemString(self->params, "contrast") );
    // Read in dispersion parameters
    PyObject* disp_dict;
    DispersionVisitor* visitor = new DispersionVisitor();
    disp_dict = PyDict_GetItemString(self->dispersion, "short_edgeA");
    self->model->short_edgeA.dispersion->accept_as_destination(visitor, self->model->short_edgeA.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "longer_edgeB");
    self->model->longer_edgeB.dispersion->accept_as_destination(visitor, self->model->longer_edgeB.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "longuest_edgeC");
    self->model->longuest_edgeC.dispersion->accept_as_destination(visitor, self->model->longuest_edgeC.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "parallel_phi");
    self->model->parallel_phi.dispersion->accept_as_destination(visitor, self->model->parallel_phi.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "parallel_theta");
    self->model->parallel_theta.dispersion->accept_as_destination(visitor, self->model->parallel_theta.dispersion, disp_dict);

	
	// Get input and determine whether we have to supply a 1D or 2D return value.
	if ( !PyArg_ParseTuple(args,"O",&pars) ) {
	    PyErr_SetString(CParallelepipedModelError, 
	    	"CParallelepipedModel.run expects a q value.");
		return NULL;
	}
	  
	// Check params
	if( PyList_Check(pars)==1) {
		
		// Length of list should be 2 for I(q,phi)
	    npars = PyList_GET_SIZE(pars); 
	    if(npars!=2) {
	    	PyErr_SetString(CParallelepipedModelError, 
	    		"CParallelepipedModel.run expects a double or a list of dimension 2.");
	    	return NULL;
	    }
	    // We have a vector q, get the q and phi values at which
	    // to evaluate I(q,phi)
	    q_value = CParallelepipedModel_readDouble(PyList_GET_ITEM(pars,0));
	    phi_value = CParallelepipedModel_readDouble(PyList_GET_ITEM(pars,1));
	    // Skip zero
	    if (q_value==0) {
	    	return Py_BuildValue("d",0.0);
	    }
		return Py_BuildValue("d",(*(self->model)).evaluate_rphi(q_value,phi_value));

	} else {

		// We have a scalar q, we will evaluate I(q)
		q_value = CParallelepipedModel_readDouble(pars);		
		
		return Py_BuildValue("d",(*(self->model))(q_value));
	}	
}

/**
 * Function to call to evaluate model in cartesian coordinates
 * @param args: input q or [qx, qy]]
 * @return: function value
 */
static PyObject * runXY(CParallelepipedModel *self, PyObject *args) {
	double qx_value, qy_value;
	PyObject* pars;
	int npars;
	
	// Get parameters
	
	    // Reader parameter dictionary
    self->model->scale = PyFloat_AsDouble( PyDict_GetItemString(self->params, "scale") );
    self->model->longer_edgeB = PyFloat_AsDouble( PyDict_GetItemString(self->params, "longer_edgeB") );
    self->model->longuest_edgeC = PyFloat_AsDouble( PyDict_GetItemString(self->params, "longuest_edgeC") );
    self->model->parallel_phi = PyFloat_AsDouble( PyDict_GetItemString(self->params, "parallel_phi") );
    self->model->parallel_theta = PyFloat_AsDouble( PyDict_GetItemString(self->params, "parallel_theta") );
    self->model->background = PyFloat_AsDouble( PyDict_GetItemString(self->params, "background") );
    self->model->short_edgeA = PyFloat_AsDouble( PyDict_GetItemString(self->params, "short_edgeA") );
    self->model->contrast = PyFloat_AsDouble( PyDict_GetItemString(self->params, "contrast") );
    // Read in dispersion parameters
    PyObject* disp_dict;
    DispersionVisitor* visitor = new DispersionVisitor();
    disp_dict = PyDict_GetItemString(self->dispersion, "short_edgeA");
    self->model->short_edgeA.dispersion->accept_as_destination(visitor, self->model->short_edgeA.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "longer_edgeB");
    self->model->longer_edgeB.dispersion->accept_as_destination(visitor, self->model->longer_edgeB.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "longuest_edgeC");
    self->model->longuest_edgeC.dispersion->accept_as_destination(visitor, self->model->longuest_edgeC.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "parallel_phi");
    self->model->parallel_phi.dispersion->accept_as_destination(visitor, self->model->parallel_phi.dispersion, disp_dict);
    disp_dict = PyDict_GetItemString(self->dispersion, "parallel_theta");
    self->model->parallel_theta.dispersion->accept_as_destination(visitor, self->model->parallel_theta.dispersion, disp_dict);

	
	// Get input and determine whether we have to supply a 1D or 2D return value.
	if ( !PyArg_ParseTuple(args,"O",&pars) ) {
	    PyErr_SetString(CParallelepipedModelError, 
	    	"CParallelepipedModel.run expects a q value.");
		return NULL;
	}
	  
	// Check params
	if( PyList_Check(pars)==1) {
		
		// Length of list should be 2 for I(qx, qy))
	    npars = PyList_GET_SIZE(pars); 
	    if(npars!=2) {
	    	PyErr_SetString(CParallelepipedModelError, 
	    		"CParallelepipedModel.run expects a double or a list of dimension 2.");
	    	return NULL;
	    }
	    // We have a vector q, get the qx and qy values at which
	    // to evaluate I(qx,qy)
	    qx_value = CParallelepipedModel_readDouble(PyList_GET_ITEM(pars,0));
	    qy_value = CParallelepipedModel_readDouble(PyList_GET_ITEM(pars,1));
	    return Py_BuildValue("d",(*(self->model))(qx_value,qy_value));

	} else {

		// We have a scalar q, we will evaluate I(q)
		qx_value = CParallelepipedModel_readDouble(pars);		
		
		return Py_BuildValue("d",(*(self->model))(qx_value));
	}	
}

static PyObject * reset(CParallelepipedModel *self, PyObject *args) {
    

    return Py_BuildValue("d",0.0);
}

static PyObject * set_dispersion(CParallelepipedModel *self, PyObject *args) {
	PyObject * disp;
	const char * par_name;

	if ( !PyArg_ParseTuple(args,"sO", &par_name, &disp) ) {
	    PyErr_SetString(CParallelepipedModelError,
	    	"CParallelepipedModel.set_dispersion expects a DispersionModel object.");
		return NULL;
	}
	void *temp = PyCObject_AsVoidPtr(disp);
	DispersionModel * dispersion = static_cast<DispersionModel *>(temp);


	// Ugliness necessary to go from python to C
	    // TODO: refactor this
    if (!strcmp(par_name, "short_edgeA")) {
        self->model->short_edgeA.dispersion = dispersion;
    } else    if (!strcmp(par_name, "longer_edgeB")) {
        self->model->longer_edgeB.dispersion = dispersion;
    } else    if (!strcmp(par_name, "longuest_edgeC")) {
        self->model->longuest_edgeC.dispersion = dispersion;
    } else    if (!strcmp(par_name, "parallel_phi")) {
        self->model->parallel_phi.dispersion = dispersion;
    } else    if (!strcmp(par_name, "parallel_theta")) {
        self->model->parallel_theta.dispersion = dispersion;
    } else {
	    PyErr_SetString(CParallelepipedModelError,
	    	"CParallelepipedModel.set_dispersion expects a valid parameter name.");
		return NULL;
	}

	DispersionVisitor* visitor = new DispersionVisitor();
	PyObject * disp_dict = PyDict_New();
	dispersion->accept_as_source(visitor, dispersion, disp_dict);
	PyDict_SetItemString(self->dispersion, par_name, disp_dict);
    return Py_BuildValue("i",1);
}


static PyMethodDef CParallelepipedModel_methods[] = {
    {"run",      (PyCFunction)run     , METH_VARARGS,
      "Evaluate the model at a given Q or Q, phi"},
    {"runXY",      (PyCFunction)runXY     , METH_VARARGS,
      "Evaluate the model at a given Q or Qx, Qy"},
    {"reset",    (PyCFunction)reset   , METH_VARARGS,
      "Reset pair correlation"},
    {"set_dispersion",      (PyCFunction)set_dispersion     , METH_VARARGS,
      "Set the dispersion model for a given parameter"},
   {NULL}
};

static PyTypeObject CParallelepipedModelType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "CParallelepipedModel",             /*tp_name*/
    sizeof(CParallelepipedModel),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)CParallelepipedModel_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "CParallelepipedModel objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    CParallelepipedModel_methods,             /* tp_methods */
    CParallelepipedModel_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)CParallelepipedModel_init,      /* tp_init */
    0,                         /* tp_alloc */
    CParallelepipedModel_new,                 /* tp_new */
};


static PyMethodDef module_methods[] = {
    {NULL} 
};

/**
 * Function used to add the model class to a module
 * @param module: module to add the class to
 */ 
void addCParallelepipedModel(PyObject *module) {
	PyObject *d;
	
    if (PyType_Ready(&CParallelepipedModelType) < 0)
        return;

    Py_INCREF(&CParallelepipedModelType);
    PyModule_AddObject(module, "CParallelepipedModel", (PyObject *)&CParallelepipedModelType);
    
    d = PyModule_GetDict(module);
    CParallelepipedModelError = PyErr_NewException("CParallelepipedModel.error", NULL, NULL);
    PyDict_SetItemString(d, "CParallelepipedModelError", CParallelepipedModelError);
}

