import sys
import unittest
import numpy as np

from unittest.mock import MagicMock

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtTest import QTest, QSignalSpy

# set up import paths
import path_prepare

import sas.qtgui.Utilities.ObjectLibrary as ObjectLibrary
import sas.qtgui.Utilities.GuiUtils as GuiUtils
from sas.qtgui.Perspectives.Fitting import FittingUtilities
from sas.qtgui.Plotting.PlotterData import Data1D

# Local
from sas.qtgui.Perspectives.Fitting.ConstraintWidget import ConstraintWidget
from sas.qtgui.Perspectives.Fitting.Constraint import Constraint
from sas.qtgui.Perspectives.Fitting.FittingPerspective import FittingWindow
from sas.qtgui.Perspectives.Fitting.FittingWidget import FittingWidget

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

class ConstraintWidgetTest(unittest.TestCase):
    '''Test the ConstraintWidget dialog'''
    def setUp(self):
        '''Create ConstraintWidget dialog'''
        class dummy_manager(object):
            def communicator(self):
                return GuiUtils.Communicate()
            communicate = GuiUtils.Communicate()

        '''Create the perspective'''
        self.perspective = FittingWindow(dummy_manager())
        ConstraintWidget.updateSignalsFromTab = MagicMock()

        self.widget = ConstraintWidget(parent=self.perspective)

        # Example constraint object
        self.constraint1 = Constraint(parent=None, param="test", value="7.0", min="0.0", max="inf", func="M1.sld")
        self.constraint2 = Constraint(parent=None, param="poop", value="7.0", min="0.0", max="inf", func="7.0")

    def tearDown(self):
        '''Destroy the GUI'''
        self.widget.close()
        self.widget = None

    def testDefaults(self):
        '''Test the GUI in its default state'''
        self.assertIsInstance(self.widget, QtWidgets.QWidget)
        # Default title
        self.assertEqual(self.widget.windowTitle(), "Constrained and Simultaneous Fit")
        # Dicts
        self.assertIsInstance(self.widget.available_constraints, dict)
        self.assertIsInstance(self.widget.available_tabs, dict)
        # TableWidgets
        self.assertEqual(self.widget.tblTabList.columnCount(), 4)
        self.assertEqual(self.widget.tblConstraints.columnCount(), 1)
        # Data accept 
        self.assertFalse(self.widget.acceptsData())
        # By default, the constraint table is disabled
        self.assertFalse(self.widget.tblConstraints.isEnabled())

    def testOnFitTypeChange(self):
        ''' test the single/batch fit switch '''
        self.widget.initializeFitList = MagicMock()
        # Assure current type is Single
        self.assertEqual(self.widget.currentType, "FitPage")
        # click on "batch"
        QTest.mouseClick(self.widget.btnBatch, QtCore.Qt.LeftButton)
        QtWidgets.QApplication.processEvents()
        # See what the current type is now
        self.assertEqual(self.widget.currentType, "BatchPage")
        # See if the list is getting initialized
        self.assertTrue(self.widget.initializeFitList.called)
        # Go back to single fit
        QTest.mouseClick(self.widget.btnSingle, QtCore.Qt.LeftButton)
        QtWidgets.QApplication.processEvents()
        # See what the current type is now
        self.assertEqual(self.widget.currentType, "FitPage")

    def testGetTabsForFit(self):
        ''' Test the fitting tab list '''
        self.assertEqual(self.widget.getTabsForFit(), [])
        # add one tab
        self.widget.tabs_for_fitting = {"foo": True}
        self.assertEqual(self.widget.getTabsForFit(), ['foo'])
        # add two tabs
        self.widget.tabs_for_fitting = {"foo": True, "bar": True}
        self.assertEqual(self.widget.getTabsForFit(), ['foo', 'bar'])
        # disable one tab
        self.widget.tabs_for_fitting = {"foo": False, "bar": True}
        self.assertEqual(self.widget.getTabsForFit(), ['bar'])

    def testIsTabImportable(self):
        ''' tab checks for consistency '''
        test_tab = MagicMock(spec=FittingWidget)
        test_tab.data_is_loaded = False
        test_tab.kernel_module = None
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)

        self.assertFalse(self.widget.isTabImportable(None))
        self.assertFalse(self.widget.isTabImportable("BatchTab1"))
        self.widget.currentType = "Batch"
        self.assertFalse(self.widget.isTabImportable("BatchTab"))
        self.widget.currentType = "test"
        self.assertFalse(self.widget.isTabImportable("test_tab"))
        test_tab.data_is_loaded = True
        self.assertTrue(self.widget.isTabImportable("test_tab"))

    def testOnTabCellEdit(self):
        ''' test what happens on monicker edit '''
        # Mock a tab
        test_tab = MagicMock(spec=FittingWidget)
        test_tab.data_is_loaded = False
        test_tab.kernel_module = MagicMock()
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)
        self.widget.updateFitLine("test_tab")

        # disable the tab
        self.widget.tblTabList.item(0, 0).setCheckState(0)
        self.assertEqual(self.widget.tabs_for_fitting["test_tab"], False)
        self.assertFalse(self.widget.cmdFit.isEnabled())
        # enable the tab
        self.widget.tblTabList.item(0, 0).setCheckState(2)
        self.assertEqual(self.widget.tabs_for_fitting["test_tab"], True)
        self.assertTrue(self.widget.cmdFit.isEnabled())

    def testUpdateFitLine(self):
        ''' See if the fit table row can be updated '''
        # mock a tab
        test_tab = MagicMock(spec=FittingWidget)
        test_tab.data_is_loaded = False
        test_tab.kernel_module = MagicMock()
        test_tab.kernel_module.name = "M1"
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)

        # Add a tab without an constraint
        self.widget.updateFitLine("test_tab")
        self.assertEqual(self.widget.tblTabList.rowCount(), 1)
        # Constraint tab should be empty
        self.assertEqual(self.widget.tblConstraints.rowCount(), 0)

        # Add a second tab with an active constraint
        test_tab.getComplexConstraintsForModel = MagicMock(
            return_value=[('scale', self.constraint1.func)])
        test_tab.getFullConstraintNameListForModel = MagicMock(
            return_value=[('scale', self.constraint1.func)])
        test_tab.getConstraintObjectsForModel = MagicMock(
            return_value=[self.constraint1])
        self.widget.updateFitLine("test_tab")
        # We should have 2 tabs in the model tab
        self.assertEqual(self.widget.tblTabList.rowCount(), 2)
        # One constraint in the constraint tab
        self.assertEqual(self.widget.tblConstraints.rowCount(), 1)
        # Constraint should be active
        self.assertEqual(self.widget.tblConstraints.item(0, 0).checkState(), 2)
        # Check the text
        self.assertEqual(self.widget.tblConstraints.item(0, 0).text(),
                         test_tab.kernel_module.name +
                         ":" +
                         "scale" +
                         " = " +
                         self.constraint1.func)
        # Add a tab with a non active constraint
        test_tab.getComplexConstraintsForModel = MagicMock(return_value=[])
        self.widget.updateFitLine("test_tab")
        # There should be two constraints now
        self.assertEqual(self.widget.tblConstraints.rowCount(), 2)
        # Added constraint should not be checked since it isn't active
        self.assertEqual(self.widget.tblConstraints.item(1, 0).checkState(), 0)

    def testUpdateFitList(self):
        ''' see if the fit table can be updated '''
        # mock a tab
        test_tab = MagicMock(spec=FittingWidget)
        test_tab.data_is_loaded = False
        test_tab.kernel_module = MagicMock()
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)

        # Fit button should be disabled if no tabs are present
        ObjectLibrary.listObjects =MagicMock(return_value=False)
        self.widget.initializeFitList()
        self.assertEqual(self.widget.available_tabs, {})
        self.assertEqual(self.widget.available_constraints, {})
        self.assertEqual(self.widget.tblConstraints.rowCount(), 0)
        self.assertEqual(self.widget.tblTabList.rowCount(), 0)
        self.assertFalse(self.widget.cmdFit.isEnabled())

        # Add a tab
        self.widget.isTabImportable = MagicMock(return_value=True)
        ObjectLibrary.listObjects = MagicMock(return_value=[test_tab])
        self.widget.updateFitLine = MagicMock()
        self.widget.updateSignalsFromTab = MagicMock()
        self.widget.initializeFitList()
        self.widget.updateFitLine.assert_called_once()
        self.widget.updateSignalsFromTab.assert_called_once()
        self.assertTrue(self.widget.cmdFit.isEnabled())

        # Check if the tab list gets ordered
        self.widget.isTabImportable = MagicMock(return_value=True)
        ObjectLibrary.listObjects = MagicMock(return_value=[test_tab])
        self.widget.updateFitLine = MagicMock()
        self.widget.updateSignalsFromTab = MagicMock()
        self.widget._row_order = [test_tab]
        self.widget.orderedSublist = MagicMock()
        self.widget.initializeFitList()
        self.widget.orderedSublist.assert_called_with([test_tab], [test_tab])


    def testOnAcceptConstraint(self):
        ''' test if a constraint can be added '''
        # mock a tab
        test_tab = MagicMock(spec=FittingWidget)
        test_tab.data_is_loaded = False
        test_tab.kernel_module = MagicMock()
        test_tab.kernel_module.name = "M1"
        test_tab.getSymbolDict = MagicMock(return_value = {})
        test_tab.addConstraintToRow = MagicMock()
        test_tab.changeCheckboxStatus = MagicMock()
        test_tab.getRowFromName = MagicMock(return_value=1)
        test_tab.changeCheckboxStatus = MagicMock()
        test_tab.getConstraintsForModel = MagicMock(return_value=[('sld',
                                                                  'sld_solvent*5')])

        self.widget.getObjectByName = MagicMock(return_value=test_tab)
        self.widget.getTabsForFit = MagicMock(return_value=[test_tab])
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)

        FittingUtilities.checkConstraints = MagicMock(return_value=[])

        # add a constraint
        self.widget.onAcceptConstraint(("M1", self.constraint1))
        FittingUtilities.checkConstraints.assert_called_with({}, [('M1.sld',
                                                                  'sld_solvent*5'),
                                                                  ('M1.test',
                                                                   'M1.sld')])
        test_tab.addConstraintToRow.assert_called_with(self.constraint1, 1)
        test_tab.changeCheckboxStatus.assert_called_with(1, True)

        # add an invalid constraint
        QtWidgets.QMessageBox.critical = MagicMock()
        test_tab.addConstraintToRow = MagicMock()
        test_tab.changeCheckboxStatus = MagicMock()
        FittingUtilities.checkConstraints = MagicMock(return_value="foo")
        self.widget.onAcceptConstraint(("M1", self.constraint1))
        QtWidgets.QMessageBox.critical.assert_called_with(self.widget,
                                                          "Inconsistent "
                                                          "constraint",
                                                          "foo",
                                                          QtWidgets.QMessageBox.Ok)
        self.assertFalse(test_tab.addConstraintToRow.called)
        self.assertFalse(test_tab.changeCheckboxStatus.called)

    def testFitComplete(self):
        ''' test the handling of fit results'''
        self.widget.getTabsForFit = MagicMock(return_value=[[None], [None]])
        spy = QSignalSpy(self.widget.parent.communicate.statusBarUpdateSignal)
        # test handling of fit error
        result = MagicMock()
        result[0][0][0].success = False
        result[0][0][0].mesg = [ValueError, None]
        self.widget.fitComplete(result)
        self.assertEqual(spy[0][0], 'Fitting failed. Please ensure '
                                    'correctness of chosen constraints.')

        # test a successful fit
        result[0][0][0].success = True
        test_tab = MagicMock()
        test_tab.kernel_module.name = 'M1'
        test_tab.fitComplete = MagicMock()
        result[0][0][0].model.name = 'M1'
        self.widget.tabs_for_fitting = {"test_tab": test_tab}
        ObjectLibrary.getObject = MagicMock(return_value=test_tab)
        self.widget.fitComplete(result)
        self.assertEqual(test_tab.fitComplete.call_args[0][0][1], result[1])
        self.assertEqual(test_tab.fitComplete.call_args[0][0][0],
                         [[result[0][0][0]]])
