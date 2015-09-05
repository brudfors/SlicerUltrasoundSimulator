import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# UltrasoundSimulator
#

class UltrasoundSimulator(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Ultrasound Simulator" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Brudfors"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (UC3M)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# UltrasoundSimulatorWidget
#

class UltrasoundSimulatorWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...
    self.iconsPath = "H:/src/S4Mods/UltrasoundSimulator/UltrasoundSimulator/Resources/Icons"
    # Used Icons
    self.recordIcon = qt.QIcon(self.iconsPath + '/icon_Record.png')
    self.playIcon = qt.QIcon(self.iconsPath + '/icon_Play.png')
    self.stopIcon = qt.QIcon(self.iconsPath + '/icon_Stop.png')
    self.restartIcon = qt.QIcon(self.iconsPath + '/icon_Restart.png')
    self.openIcon = qt.QIcon(self.iconsPath + '/icon_Open.png')
    
    #
    # Parameters Area
    #
    self.calibrate1CollapsibleButton = ctk.ctkCollapsibleButton()
    self.calibrate1CollapsibleButton.text = "Calibrate I"
    self.layout.addWidget(self.calibrate1CollapsibleButton)

    # Layout within the dummy collapsible button
    calibrate1FormLayout = qt.QFormLayout(self.calibrate1CollapsibleButton)

    #
    # transform selector
    #
    self.IMUTransformSelector = slicer.qMRMLNodeComboBox()
    self.IMUTransformSelector.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.IMUTransformSelector.selectNodeUponCreation = False
    self.IMUTransformSelector.addEnabled = False
    self.IMUTransformSelector.removeEnabled = False
    self.IMUTransformSelector.noneEnabled = False
    self.IMUTransformSelector.showHidden = False
    self.IMUTransformSelector.showChildNodeTypes = False
    self.IMUTransformSelector.setMRMLScene( slicer.mrmlScene )
    self.IMUTransformSelector.setToolTip( "Select the IMU orientation transform." )
    calibrate1FormLayout.addRow("Orientation Transform: ", self.IMUTransformSelector)

    # Calibration info
    self.calibrationInstructionsGroupBox = qt.QGroupBox()
    self.calibrationInstructionsGroupBox.setLayout(qt.QVBoxLayout())
    self.calibrationInstructionsLabel01 = qt.QLabel("Initialize calibration")
    self.calibrationInstructionsLabel01.setStyleSheet("QLabel {color: #000000; text-decoration: underline;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel01)
    self.calibrationInstructionsLabel02 = qt.QLabel("Select Orientation Transform and press Start Calibration.")
    self.calibrationInstructionsLabel02.setWordWrap(True)
    self.calibrationInstructionsLabel02.setStyleSheet("QLabel {color: #A0A0A0;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel02)
    
    self.calibrationInstructionsLabel11 = qt.QLabel("Place initial fiducials")
    self.calibrationInstructionsLabel11.setStyleSheet("QLabel {color: #000000; text-decoration: underline;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel11)
    self.calibrationInstructionsLabel12 = qt.QLabel("Scroll through the slice views, locate the sphere numbered 1, press the point in the center of the sphere.")
    self.calibrationInstructionsLabel12.setWordWrap(True)
    self.calibrationInstructionsLabel12.setStyleSheet("QLabel {color: #A0A0A0;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel12)
    
    self.calibrationInstructionsLabel21 = qt.QLabel("Align calibration model")
    self.calibrationInstructionsLabel21.setWordWrap(True)
    self.calibrationInstructionsLabel21.setStyleSheet("QLabel {color: #000000; text-decoration: underline;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel21)
    self.calibrationInstructionsLabel22 = qt.QLabel("Use sliders (LR, PA, IS) and the scroll wheel, in order to align the digit inside sphere 1. \nWhen finished, press Calibration Model Aligned.")
    self.calibrationInstructionsLabel22.setWordWrap(True)
    self.calibrationInstructionsLabel22.setStyleSheet("QLabel {color: #A0A0A0;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel22)
    
    self.calibrationInstructionsLabel31 = qt.QLabel("Place calibration fiducials")
    self.calibrationInstructionsLabel31.setWordWrap(True)
    self.calibrationInstructionsLabel31.setStyleSheet("QLabel {color: #000000; text-decoration: underline;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel31)
    self.calibrationInstructionsLabel32 = qt.QLabel("Scroll through the slice views, locate the sphere numbered 2, press the point in the center of the sphere.")
    self.calibrationInstructionsLabel32.setWordWrap(True)
    self.calibrationInstructionsLabel32.setStyleSheet("QLabel {color: #A0A0A0;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel32)
    
    self.calibrationInstructionsLabel41 = qt.QLabel("Calculate calibration transform")
    self.calibrationInstructionsLabel41.setWordWrap(True)
    self.calibrationInstructionsLabel41.setStyleSheet("QLabel {color: #000000; text-decoration: underline;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel41)
    self.calibrationInstructionsLabel42 = qt.QLabel("Press Calculate Calibration Transform")
    self.calibrationInstructionsLabel42.setWordWrap(True)
    self.calibrationInstructionsLabel42.setStyleSheet("QLabel {color: #A0A0A0;}")
    self.calibrationInstructionsGroupBox.layout().addWidget(self.calibrationInstructionsLabel42)
    
    calibrate1FormLayout.addRow("Calibration Steps:", self.calibrationInstructionsGroupBox) 
    
    buttonHeight = 35
    
    # Start/Stop/Restart calibration Button  
    calibrateControlsLayout = qt.QHBoxLayout()
    calibrate1FormLayout.addRow(calibrateControlsLayout)
    self.startCalibrationButton = qt.QPushButton("  Start Calibration")
    self.startCalibrationButton.setCheckable(False)
    self.startCalibrationButton.setIcon(self.playIcon)
    self.startCalibrationButton.setEnabled(False)
    self.startCalibrationButton.setToolTip("Start calibration of the Ultrasound Simulator")
    self.startCalibrationButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.startCalibrationButton.setFixedHeight(buttonHeight)
    calibrateControlsLayout.addWidget(self.startCalibrationButton)
    self.stopCalibrationButton = qt.QPushButton("  Stop Calibration")
    self.stopCalibrationButton.setCheckable(False)
    self.stopCalibrationButton.setIcon(self.stopIcon)
    self.stopCalibrationButton.setEnabled(False)
    self.stopCalibrationButton.setToolTip("Stop calibration of the Ultrasound Simulator")
    self.stopCalibrationButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.stopCalibrationButton.setFixedHeight(buttonHeight)
    calibrateControlsLayout.addWidget(self.stopCalibrationButton)
    self.restartCalibrationButton = qt.QPushButton("  Restart Calibration")
    self.restartCalibrationButton.setCheckable(False)
    self.restartCalibrationButton.setIcon(self.restartIcon)
    self.restartCalibrationButton.setEnabled(False)
    self.restartCalibrationButton.setToolTip("Restart calibration of the Ultrasound Simulator")
    self.restartCalibrationButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.restartCalibrationButton.setFixedHeight(buttonHeight)
    calibrateControlsLayout.addWidget(self.restartCalibrationButton)  
    
    # qMRMLTransformSliders widget      
    self.w = slicer.qMRMLTransformSliders()
    self.w.CoordinateReference = self.w.GLOBAL
    self.w.TypeOfTransform = self.w.ROTATION
    calibrate1FormLayout.addRow(self.w)
    
    alignButtonLayout = qt.QHBoxLayout()
    calibrate1FormLayout.addRow(alignButtonLayout)
    self.alignedButton = qt.QPushButton("Calibration Model Aligned")
    self.alignedButton.setCheckable(False)
    self.alignedButton.setEnabled(False)
    self.alignedButton.setToolTip("Calibration model aligned")
    self.alignedButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.alignedButton.setFixedHeight(buttonHeight)
    alignButtonLayout.addWidget(self.alignedButton)
            
    self.calculateTransformButton = qt.QPushButton("Calculate Calibration Transform")
    self.calculateTransformButton.setCheckable(False)
    self.calculateTransformButton.setEnabled(False)
    self.calculateTransformButton.setToolTip("Calculate calibration transform")
    self.calculateTransformButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.calculateTransformButton.setFixedHeight(buttonHeight)
    alignButtonLayout.addWidget(self.calculateTransformButton) 

    #
    # Calibrate 2 Area
    #
    self.calibrate2CollapsibleButton = ctk.ctkCollapsibleButton()
    self.calibrate2CollapsibleButton.text = "Calibrate II"
    self.layout.addWidget(self.calibrate2CollapsibleButton)

    # Layout within the dummy collapsible button
    calibrate2FormLayout = qt.QFormLayout(self.calibrate2CollapsibleButton)

    self.calibrate2Button = qt.QPushButton("Calibrate")
    self.calibrate2Button.setCheckable(False)
    self.calibrate2Button.setEnabled(True)
    self.calibrate2Button.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.calibrate2Button.setFixedHeight(buttonHeight)
    calibrate2FormLayout.addWidget(self.calibrate2Button)

    #    
    # Simulator Area
    #
    simulatorCollapsibleButton = ctk.ctkCollapsibleButton()
    simulatorCollapsibleButton.text = "Simulate Ultrasound"
    self.layout.addWidget(simulatorCollapsibleButton)

    # Layout within the dummy collapsible button
    simulatorFormLayout = qt.QFormLayout(simulatorCollapsibleButton)
  
    self.calibrationStatusLabel = qt.QLabel("Run calibration!")
    self.calibrationStatusLabel.setStyleSheet("QLabel {color: #FF0000;}")
    simulatorFormLayout.addRow("Calibration Status: ", self.calibrationStatusLabel)
  
    # Start/Stop/Restart calibration Button  
    simulatorControlsLayout = qt.QHBoxLayout()
    simulatorFormLayout.addRow(simulatorControlsLayout)
    self.loadSampleVolumeButton = qt.QPushButton("  Load Sample Volume")
    self.loadSampleVolumeButton.setCheckable(False)
    self.loadSampleVolumeButton.setEnabled(False)
    self.loadSampleVolumeButton.setIcon(self.openIcon)
    self.loadSampleVolumeButton.setToolTip("Load sample abdominal phantom")
    self.loadSampleVolumeButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.loadSampleVolumeButton.setFixedHeight(buttonHeight)
    simulatorControlsLayout.addWidget(self.loadSampleVolumeButton)
    self.runSimulatorButton = qt.QPushButton("  Run Simulator")
    self.runSimulatorButton.setCheckable(False)
    self.runSimulatorButton.setEnabled(False)
    self.runSimulatorButton.setIcon(self.playIcon)
    self.runSimulatorButton.setToolTip("Start the Ultrasound Simulator")
    self.runSimulatorButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.runSimulatorButton.setFixedHeight(buttonHeight)
    simulatorControlsLayout.addWidget(self.runSimulatorButton)
    
    # Connections
    self.calibrate2Button.connect('clicked(bool)', self.onCalibrate2Button)
    self.calculateTransformButton.connect('clicked(bool)', self.onCalculateTransformButton)
    self.alignedButton.connect('clicked(bool)', self.onAlignedButton)
    self.startCalibrationButton.connect('clicked(bool)', self.onStartCalibrationButton)
    self.restartCalibrationButton.connect('clicked(bool)', self.onRestartCalibrationButton)
    self.stopCalibrationButton.connect('clicked(bool)', self.onStopCalibrationButton)
    self.IMUTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onIMUTransformSelector)
    self.loadSampleVolumeButton.connect('clicked(bool)', self.onLoadSampleVolumeButton)
    self.runSimulatorButton.connect('clicked(bool)', self.onRunSimulatorButton)
    
    # Logic and Node members
    self.calibrationModelNode = None
    self.calibrationModelDisplayNode = None
    self.IMUTransformNode = None
    self.startFiducialNode = None
    self.endFiducialNode = None
    self.crosshairNode = None
    self.markupsModuleLogic = None
    self.tempTransform = None
    self.saveTransform = None
    self.volumeCurrentlyLoaded = None
    self.inverseTransform = None
    self.finalTransform = None
    self.translateTransform = None
    self.maskVolumeNode = None
    
    # Parameter members
    self.nbrOfFiducialsPlaced = 0
    self.nbrOfFiducialsToPlace = 3
        
    # Bool memebers
    self.calibrationInitialized = False
    self.placingFiducials = False
    self.layoutOneUpRedSliceView = False
    self.tempTransformApplied = False
    self.tempTransformAligned = False
    
    # Calibration state
    self.calibrationStateTimer = qt.QTimer()
    self.calibrationStateTimer.timeout.connect(self.calibrationStateTimeOut)
    self.currentCalibrationState = "PLACE_START_FIDUCIALS"
    
    # Layout manager
    self.applicationLogic = slicer.logic.vtkSlicerApplicationLogic()
    self.lm = slicer.app.layoutManager()
    
    # Left mouse click in Slice view observers
    self.redSliceWidget = self.lm.sliceWidget('Red')
    self.greenSliceWidget = self.lm.sliceWidget('Green')
    self.yellowSliceWidget = self.lm.sliceWidget('Yellow')
    self.redInteractor = self.redSliceWidget.sliceView().interactorStyle().GetInteractor()
    self.greenInteractor = self.greenSliceWidget.sliceView().interactorStyle().GetInteractor()
    self.yellowInteractor = self.yellowSliceWidget.sliceView().interactorStyle().GetInteractor()
    self.redInteractorObserverID = -1
    self.greenInteractorObserverID = -1
    self.yellowInteractorObserverID = -1  
    self.redSliceLogic = self.redSliceWidget.sliceLogic()
    self.redSliceNode = self.redSliceLogic.GetSliceNode()
    self.redSliceFGLayer = self.redSliceLogic.GetForegroundLayer()
    self.redSliceBGLayer = self.redSliceLogic.GetBackgroundLayer()
    self.redSliceCompositeNode = self.redSliceLogic.GetSliceCompositeNode()
    
    # For disabling mouse interaction             
    self.interactorObserverTags = []
    self.mouseEvents = ( "LeftButtonPressEvent", "LeftButtonReleaseEvent",
                         "MiddleButtonPressEvent", "MiddleButtonReleaseEvent",
                         "RightButtonPressEvent", "RightButtonReleaseEvent",
                         "MouseMoveEvent", "KeyPressEvent", "EnterEvent", "LeaveEvent",
                         "MouseWheelForwardEvent", "MouseWheelBackwardEvent" )
                                        
    # Refresh state
    self.onIMUTransformSelector()
    
  def abortEvent(self, caller=None, event=None):
    """Set the AbortFlag on the vtkCommand associated
    with the event - causes other things listening to the
    redInteractor not to receive the events"""
    # TODO: make interactorObserverTags a map to we can
    # explicitly abort just the event we handled - it will
    # be slightly more efficient
    for tag in self.interactorObserverTags:
      cmd = self.redInteractor.GetCommand(tag)
      cmd.SetAbortFlag(1)

  def onCalibrate2Button(self):
    self.inverseTransform = slicer.vtkMRMLLinearTransformNode()
    self.inverseTransform.SetName("InverseTransform")
    orientationTransform = self.IMUTransformNode
    self.inverseTransform.SetMatrixTransformFromParent(orientationTransform.GetMatrixTransformFromParent())
    self.inverseTransform.Inverse()
    slicer.mrmlScene.AddNode(self.inverseTransform)
            
    self.translateTransform = slicer.vtkMRMLLinearTransformNode()
    self.translateTransform.SetName("TranslateTransform")
    matrix = self.translateTransform.GetMatrixTransformFromParent()
    matrix.SetElement(1,3,-80)
    self.translateTransform.SetMatrixTransformToParent(matrix)
    slicer.mrmlScene.AddNode(self.translateTransform)
     
    self.probeTransform = slicer.vtkMRMLLinearTransformNode()
    self.probeTransform.SetName("ProbeTransform")
    matrix.SetElement(1,3,-60)
    self.probeTransform.SetMatrixTransformToParent(matrix)
    slicer.mrmlScene.AddNode(self.probeTransform)
    slicer.util.loadVolume("H:/src/S4Mods/UltrasoundSimulator/Data/Linear_probe.mha")
    self.maskVolumeNode = slicer.util.getNode("Linear_probe")
    self.maskVolumeNode.SetAndObserveTransformNodeID(self.probeTransform.GetID())
    
    slicer.util.loadVolume("H:/Data/CT/CT_abdominal_phantom.mha")
    self.volumeCurrentlyLoaded = slicer.util.getNode("CT_abdominal_phantom")
    
    self.volumeCurrentlyLoaded.SetAndObserveTransformNodeID(self.translateTransform.GetID())
    
    self.IMUTransformNode.SetAndObserveTransformNodeID(self.inverseTransform.GetID())
    self.translateTransform.SetAndObserveTransformNodeID(self.IMUTransformNode.GetID())
    
    self.volumeCurrentlyLoaded.GetScalarVolumeDisplayNode().SetAutoWindowLevel(False)
    self.volumeCurrentlyLoaded.GetScalarVolumeDisplayNode().SetWindowLevel(350, 40)
    
    #xyzOrigSampleVol = self.volumeCurrentlyLoaded.GetOrigin()
    #self.volumeCurrentlyLoaded.SetOrigin(xyzOrigSampleVol[0], xyzOrigSampleVol[1] - xyzOrigSampleVol[1] / 2, xyzOrigSampleVol[2])
    
    self.redSliceNode.SetSliceOrigin(0, -80, 0)
    self.redSliceNode.SetFieldOfView(180, 180,0)
    
    self.lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
    
    self.redSliceCompositeNode.SetForegroundVolumeID(self.volumeCurrentlyLoaded.GetID())
    #self.redSliceFGLayer.SetVolumeNode(self.volumeCurrentlyLoaded)
    self.redSliceCompositeNode.SetForegroundOpacity(1.0)
    self.applicationLogic.PropagateForegroundVolumeSelection() # Not working
    
    self.redSliceCompositeNode.SetBackgroundVolumeID(self.maskVolumeNode.GetID())
    #self.redSliceBGLayer.SetVolumeNode(self.maskVolumeNode)    
    self.applicationLogic.PropagateBackgroundVolumeSelection() # Not working
    
    maskVolumeDisplayNode = self.maskVolumeNode.GetVolumeDisplayNode()
    maskVolumeDisplayNode.SetLowerThreshold(10)
    maskVolumeDisplayNode.ApplyThresholdOn ()
    
    '''
    lm = slicer.app.layoutManager()
    redSliceWidget = lm.sliceWidget('Red')
    redSliceLogic = redSliceWidget.sliceLogic()
    redSliceFGLayer = redSliceLogic.GetForegroundLayer()
    redSliceBGLayer = redSliceLogic.GetBackgroundLayer()
    ctNode = getNode("CT_abdominal_phantom")
    maskNode = getNode("Rectangular_mask")
    
    a=slicer.logic.vtkSlicerApplicationLogic()
    a.PropagateForegroundVolumeSelection()
    a.PropagateBackgroundVolumeSelection()
    '''
    
  def onLoadSampleVolumeButton(self):
    self.loadSampleVolumeButton.enabled = False
    slicer.util.loadVolume(self.ultrasoundSimulatorExtPath + "/Abdominal_phantom.mha")
    self.volumeCurrentlyLoaded = getNode("Abdominal_phantom") 
    # Set W/L for volume
    self.volumeCurrentlyLoaded.GetScalarVolumeDisplayNode().SetAutoWindowLevel(False)
    self.volumeCurrentlyLoaded.GetScalarVolumeDisplayNode().SetWindowLevel(1135,197)
    self.runSimulatorButton.enabled = True  
    
  def onRunSimulatorButton(self):
    self.runSimulatorButton.enabled = False
    self.volumeCurrentlyLoaded.SetAndObserveTransformNodeID(self.IMUTransformNode.GetID())
    
    xyzOrigSampleVol = self.volumeCurrentlyLoaded.GetOrigin()
    self.volumeCurrentlyLoaded.SetOrigin(xyzOrigSampleVol[0], xyzOrigSampleVol[1] - xyzOrigSampleVol[1] / 2, xyzOrigSampleVol[2])
    
    self.redSliceNode.SetSliceOrigin(0, -(xyzOrigSampleVol[1] - xyzOrigSampleVol[1] / 2),0)
    self.redSliceNode.SetFieldOfView(200,200,0)
    
    # For disabling mouse interaction
    for e in self.mouseEvents:
      tag = self.redInteractor.AddObserver(e, self.abortEvent, 1.0)
      self.interactorObserverTags.append(tag)
      
  def onAlignedButton(self):
    self.w.setEnabled(False)
    self.alignedButton.setEnabled(False)
    self.currentCalibrationState = "PLACE_END_FIDUCIALS"
    
  def calibrationStateTimeOut(self):
    # Info
    if self.currentCalibrationState == "PLACE_START_FIDUCIALS":
      if not self.placingFiducials:
        self.calibrationInstructionsLabel12.setStyleSheet("QLabel {color: #000000}")
        self.lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
        self.markupsModuleLogic.AddNewFiducialNode("I")
        self.startFiducialNode = getNode("I")
        self.redInteractorObserverID = self.redInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.greenInteractorObserverID = self.greenInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.yellowInteractorObserverID = self.yellowInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)            
        self.placingFiducials = True
      elif self.nbrOfFiducialsPlaced == self.nbrOfFiducialsToPlace:
        self.calibrationInstructionsLabel12.setText("Scroll through the slice views, locate the sphere numbered 3, press the point in the center of the sphere.")
        self.calibrationInstructionsLabel12.setStyleSheet("QLabel {color: #000000; text-decoration: line-through;}")
        self.currentCalibrationState = "ALIGN_CALIBRATION_MODEL"
        self.redInteractor.RemoveObserver(self.redInteractorObserverID)
        self.greenInteractor.RemoveObserver(self.greenInteractorObserverID)
        self.yellowInteractor.RemoveObserver(self.yellowInteractorObserverID)
        self.redInteractorObserverID = -1
        self.greenInteractorObserverID = -1
        self.yellowInteractorObserverID = -1
        self.nbrOfFiducialsPlaced = 1  
        self.placingFiducials = False             
      else:
        self.calibrationInstructionsLabel12.setText("Scroll through the slice views, locate the sphere numbered " + str(self.nbrOfFiducialsPlaced + 1) + ", press the point in the center of the sphere.")
        return     
    # Info
    elif self.currentCalibrationState == "ALIGN_CALIBRATION_MODEL":
      if not self.tempTransformApplied:
        self.lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
        self.redSliceNode.SetSliceOffset(0)
        self.calibrationInstructionsLabel22.setStyleSheet("QLabel {color: #000000}")
        self.tempTransformApplied = True
        self.tempTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(self.tempTransform)
        self.IMUTransformNode.SetAndObserveTransformNodeID(self.tempTransform.GetID())
        self.w.setEnabled(True)
        self.w.setMRMLTransformNode(self.tempTransform)
        self.alignedButton.setEnabled(True)
      else:
        return      
    # Info
    elif self.currentCalibrationState == "PLACE_END_FIDUCIALS":
      if not self.placingFiducials:
        self.calibrationInstructionsLabel22.setStyleSheet("QLabel {color: #000000;  text-decoration: line-through;}")
        self.calibrationInstructionsLabel32.setStyleSheet("QLabel {color: #000000;}")
        self.markupsModuleLogic.AddNewFiducialNode("C")
        self.endFiducialNode = getNode("C")
        
        # Add first fiducial of Start to End since it is the same 
        ras = [0,0,0]
        self.startFiducialNode.GetNthFiducialPosition(0, ras)
        self.endFiducialNode.AddFiducial(ras[0], ras[1], ras[2])
        
        self.redInteractorObserverID = self.redInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.greenInteractorObserverID = self.greenInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.yellowInteractorObserverID = self.yellowInteractor.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)  
        self.placingFiducials = True
      elif self.nbrOfFiducialsPlaced == self.nbrOfFiducialsToPlace:
        self.calibrationInstructionsLabel32.setText("Scroll through the slice views, locate the sphere numbered 3, press the point in the center of the sphere.")
        self.calibrationInstructionsLabel32.setStyleSheet("QLabel {color: #000000; text-decoration: line-through;}")
        self.currentCalibrationState = "CALCULATE_START_TO_END"
        self.redInteractor.RemoveObserver(self.redInteractorObserverID)
        self.greenInteractor.RemoveObserver(self.greenInteractorObserverID)
        self.yellowInteractor.RemoveObserver(self.yellowInteractorObserverID)
        self.redInteractorObserverID = -1
        self.greenInteractorObserverID = -1
        self.yellowInteractorObserverID = -1
        self.nbrOfFiducialsPlaced = 0  
        self.placingFiducials = False
      else:
        self.calibrationInstructionsLabel32.setText("Scroll through the slice views, locate the sphere numbered " + str(self.nbrOfFiducialsPlaced + 1) + ", press the point in the center of the sphere.")
        return        
    # Info
    elif self.currentCalibrationState == "CALCULATE_START_TO_END":
      self.calibrationInstructionsLabel42.setStyleSheet("QLabel {color: #000000;}")
      self.calculateTransformButton.setEnabled(True)         
    # Info
    elif self.currentCalibrationState == "APPLY_AND_FINALIZE_CALIBRATION":
      if self.saveTransform.GetMatrixTransformToParent().GetElement(0,0) != 1.0:
        self.IMUTransformNode.SetAndObserveTransformNodeID(self.saveTransform.GetID())
        self.loadSampleVolumeButton.enabled = True
        self.calibrationStateTimer.stop()    
        slicer.mrmlScene.RemoveNode(self.tempTransform)
        self.tempTransform = None       
        slicer.mrmlScene.RemoveNode(self.calibrationModelNode)
        self.calibrationModelNode = None  
        slicer.mrmlScene.RemoveNode(self.startFiducialNode)
        self.startFiducialNode = None       
        slicer.mrmlScene.RemoveNode(self.endFiducialNode)
        self.endFiducialNode = None
        self.startToEndTransformCalculated = False
        self.tempTransformApplied = False
        self.calibrate1CollapsibleButton.collapsed = True
        self.calibrationStatusLabel.setText("Calibration completed")
        self.calibrationStatusLabel.setStyleSheet("QLabel {color: #000000;}")
           
  def onCalculateTransformButton(self): 
    self.calibrationInstructionsLabel42.setStyleSheet("QLabel {color: #000000;  text-decoration: line-through;}")
    self.calculateTransformButton.setEnabled(False)   
    self.saveTransform = slicer.vtkMRMLLinearTransformNode()
    self.saveTransform.SetName("EndToStartTransform")
    slicer.mrmlScene.AddNode(self.saveTransform)
    logic = UltrasoundSimulatorLogic()  
    logic.calculateStartToEnd(self.saveTransform, self.startFiducialNode, self.endFiducialNode)
    self.currentCalibrationState = "APPLY_AND_FINALIZE_CALIBRATION" 

  # Events
  def leftButtonPressEvent(self, caller=None, event=None):
    ras=[0,0,0]
    self.crosshairNode.GetCursorPositionRAS(ras)
    self.markupsModuleLogic.AddFiducial(ras[0], ras[1], ras[2])
    self.nbrOfFiducialsPlaced += 1    
      
  def onStartCalibrationButton(self):    
    self.calibrationInstructionsLabel02.setStyleSheet("QLabel {color: #000000; text-decoration: line-through;}")
    self.startCalibrationButton.setEnabled(False)
    self.initializeCalibration()
    self.calibrationStateTimer.start(200)
           
  def onStopCalibrationButton(self):
    pass
    
  def onRestartCalibrationButton(self):
    slicer.mrmlScene.Clear(0)

  def onIMUTransformSelector(self):
    if self.IMUTransformSelector.currentNode():
      self.calibrationInstructionsLabel02.setStyleSheet("QLabel {color: #000000;}")
      self.IMUTransformNode = self.IMUTransformSelector.currentNode()
      self.startCalibrationButton.enabled = self.IMUTransformNode
    
  def initializeCalibration(self):
    slicer.util.loadModel("H:/src/S4Mods/UltrasoundSimulator/Data/Calibration_model.stl")
    self.calibrationModelNode = getNode("Calibration_model")      
    self.calibrationModelDisplayNode = self.calibrationModelNode.GetModelDisplayNode()
    self.calibrationModelDisplayNode.SliceIntersectionVisibilityOn()
    self.calibrationModelDisplayNode.SetColor(1,0,0) 
    self.calibrationModelNode.SetAndObserveTransformNodeID(self.IMUTransformNode.GetID())
    self.markupsModuleLogic = slicer.modules.markups.logic()   
    self.crosshairNode = slicer.util.getNode('crosshair')    
    self.calibrationInitialized = True  

#
# UltrasoundSimulatorLogic
#

class UltrasoundSimulatorLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def calculateStartToEnd(self, saveTransform, startFiducialNode, endFiducialNode):
    logging.info("calculateEndToStart")
    parameters = {}
    rms = 0
    parameters["fixedLandmarks"] = endFiducialNode.GetID()
    parameters["movingLandmarks"] = startFiducialNode.GetID()
    parameters["saveTransform"] = saveTransform.GetID()
    parameters["rms"] = rms 
    fidReg = slicer.modules.fiducialregistration
    slicer.cli.run(fidReg, None, parameters)
    return
    
  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() == None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('UltrasoundSimulatorTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class UltrasoundSimulatorTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_UltrasoundSimulator1()

  def test_UltrasoundSimulator1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = UltrasoundSimulatorLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
