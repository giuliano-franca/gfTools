# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

====================================================================================================

Disclaimer:
    THIS PLUGIN IS JUST A PROTOTYPE. YOU MUST USE THE C++ RELEASE PLUGIN FOR PRODUCTION.
    YOU CAN FIND THE C++ RELEASE PLUGIN FOR YOUR SPECIFIC PLATFORM IN RELEASES FOLDER:
    "gfTools > plug-ins > release"

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Description:
    Convert euler rotation to vector.

Attributes:
    * Euler: The euler rotation to be converted to vector.
    * Out Vector: The output vector converted from an euler rotation.

Todo:
    * NDA

Sources:
    * NDA

This code supports Pylint. Rc file in project.
"""
import maya.api._OpenMaya_py2 as om2


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=invalid-name, unnecessary-pass
    pass


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=invalid-name
    FNATTR.writable = True
    FNATTR.readable = True
    FNATTR.storable = True
    FNATTR.keyable = True


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=invalid-name
    FNATTR.writable = False
    FNATTR.readable = True
    FNATTR.storable = False
    FNATTR.keyable = False


class EulerToVector(om2.MPxNode):
    """ Main class of gfUtilEulerToVector node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inEuler = om2.MObject()
    outVector = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return EulerToVector()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to EulerToVector class. Instances of EulerToVector will use these attributes to create plugs
        for use in the compute() method.
        """
        uAttr = om2.MFnUnitAttribute()
        nAttr = om2.MFnNumericAttribute()

        eulerX = uAttr.create("eulerX", "ex", om2.MFnUnitAttribute.kAngle, 0.0)
        eulerY = uAttr.create("eulerY", "ey", om2.MFnUnitAttribute.kAngle, 0.0)
        eulerZ = uAttr.create("eulerZ", "ez", om2.MFnUnitAttribute.kAngle, 0.0)
        EulerToVector.inEuler = nAttr.create("euler", "e", eulerX, eulerY, eulerZ)
        INPUT_ATTR(nAttr)

        outVectorX = nAttr.create("outVectorX", "ovx", om2.MFnNumericData.kDouble, 0.0)
        outVectorY = nAttr.create("outVectorY", "ovy", om2.MFnNumericData.kDouble, 0.0)
        outVectorZ = nAttr.create("outVectorZ", "ovz", om2.MFnNumericData.kDouble, 0.0)
        EulerToVector.outVector = nAttr.create("outVector", "ov", outVectorX, outVectorY, outVectorZ)
        OUTPUT_ATTR(nAttr)

        EulerToVector.addAttribute(EulerToVector.inEuler)
        EulerToVector.addAttribute(EulerToVector.outVector)
        EulerToVector.attributeAffects(EulerToVector.inEuler, EulerToVector.outVector)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=no-self-use
        if plug != EulerToVector.outVector:
            return om2.kUnknownParameter

        vEuler = dataBlock.inputValue(EulerToVector.inEuler).asVector()
        eEuler = om2.MEulerRotation(
            om2.MAngle(vEuler.x, om2.MAngle.kRadians).asDegrees(),
            om2.MAngle(vEuler.y, om2.MAngle.kRadians).asDegrees(),
            om2.MAngle(vEuler.z, om2.MAngle.kRadians).asDegrees(),
            om2.MEulerRotation.kXYZ
        )

        outVectorHandle = dataBlock.outputValue(EulerToVector.outVector)
        outVectorHandle.setMVector(eEuler.asVector())
        outVectorHandle.setClean()