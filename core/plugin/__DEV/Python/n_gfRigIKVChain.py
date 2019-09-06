# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

Redistribution:
    Something here.

Maya Node:
    [This is a prototype version of the gfRigIKVChainSolver node. You should be using the related C++ version.]
    This node is a test node and only performs test operations with one input value.
    https://www.desmos.com/calculator/wthlznq4aj

Requirements:
    Maya 2017 or above.

Todo:
    * Create and develop the stretchMult attrs.
    * Create and develop the squashMult attrs.
    * Create and develop the slidePv attr.

This code supports Pylint. Rc file in project.
"""

import math
import maya.api._OpenMaya_py2 as om2


def maya_useNewAPI():
    """ Function to Maya recognize the use of the Python API 2.0. """
    # pylint: disable=C0103, W0107
    pass


def INPUT_ATTR(FNATTR):
    """ Configure a input attribute. """
    # pylint: disable=C0103
    FNATTR.writable = True
    FNATTR.readable = True
    FNATTR.storable = True
    FNATTR.keyable = True


def OUTPUT_ATTR(FNATTR):
    """ Configure a output attribute. """
    # pylint: disable=C0103
    FNATTR.writable = False
    FNATTR.readable = True
    FNATTR.storable = False
    FNATTR.keyable = False


class IKVChainSolver(om2.MPxNode):
    """ Main class of gfRigIKVChainSolver node. """

    kNodeName = ""
    kNodeClassify = ""
    kNodeID = ""

    inRoot = om2.MObject()
    inHandle = om2.MObject()
    inUpVector = om2.MObject()
    inPreferredAngle = om2.MObject()
    inPvMode = om2.MObject()
    inTwist = om2.MObject()
    inHierarchyMode = om2.MObject()
    inRestLength1 = om2.MObject()
    inRestLength2 = om2.MObject()
    inCompressionLimit = om2.MObject()
    inSoftness = om2.MObject()
    inStretch = om2.MObject()
    inClampStretch = om2.MObject()
    inClampValue = om2.MObject()
    inSquash = om2.MObject()
    outChain = om2.MObject()

    def __init__(self):
        """ Constructor. """
        om2.MPxNode.__init__(self)

    @staticmethod
    def creator():
        """ Maya creator function. """
        return IKVChainSolver()

    @staticmethod
    def initialize():
        """
        Defines the set of attributes for this node. The attributes declared in this function are assigned
        as static members to IKVChainSolver class. Instances of IKVChainSolver will use these attributes to create plugs
        for use in the compute() method.
        """
        mAttr = om2.MFnMatrixAttribute()
        nAttr = om2.MFnNumericAttribute()
        uAttr = om2.MFnUnitAttribute()
        eAttr = om2.MFnEnumAttribute()

        IKVChainSolver.inRoot = mAttr.create("root", "root", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inHandle = mAttr.create("handle", "handle", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inUpVector = mAttr.create("upVector", "up", om2.MFnMatrixAttribute.kFloat)
        INPUT_ATTR(mAttr)

        IKVChainSolver.inPreferredAngle = uAttr.create("preferredAngle", "pa", om2.MFnUnitAttribute.kAngle, 0.0)
        uAttr.setMin(0.0)
        uAttr.setMax(2.0 * math.pi)
        INPUT_ATTR(uAttr)

        IKVChainSolver.inPvMode = eAttr.create("pvMode", "pvm", 0)
        eAttr.addField("Manual", 0)
        eAttr.addField("Auto", 1)
        INPUT_ATTR(eAttr)

        IKVChainSolver.inTwist = uAttr.create("twist", "tw", om2.MFnUnitAttribute.kAngle, 0.0)
        INPUT_ATTR(uAttr)

        IKVChainSolver.inHierarchyMode = nAttr.create("hierarchyMode", "hm", om2.MFnNumericData.kBoolean, True)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLength1 = nAttr.create("restLength1", "rl1", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inRestLength2 = nAttr.create("restLength2", "rl2", om2.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0.001)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inCompressionLimit = nAttr.create("compressionLimit", "cl", om2.MFnNumericData.kFloat, 0.1)
        nAttr.setMin(0.001)
        nAttr.setMax(0.4)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSoftness = nAttr.create("softness", "soft", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setSoftMax(0.4)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inStretch = nAttr.create("stretch", "st", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inClampStretch = nAttr.create("clampStretch", "cst", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inClampValue = nAttr.create("clampValue", "cstv", om2.MFnNumericData.kFloat, 1.5)
        nAttr.setMin(1.0)
        nAttr.setSoftMax(1.8)
        INPUT_ATTR(nAttr)

        IKVChainSolver.inSquash = nAttr.create("squash", "sq", om2.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        INPUT_ATTR(nAttr)

        IKVChainSolver.outChain = mAttr.create("outChain", "oc", om2.MFnMatrixAttribute.kFloat)
        mAttr.array = True
        OUTPUT_ATTR(mAttr)

        IKVChainSolver.addAttribute(IKVChainSolver.inRoot)
        IKVChainSolver.addAttribute(IKVChainSolver.inHandle)
        IKVChainSolver.addAttribute(IKVChainSolver.inUpVector)
        IKVChainSolver.addAttribute(IKVChainSolver.inPreferredAngle)
        IKVChainSolver.addAttribute(IKVChainSolver.inPvMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inTwist)
        IKVChainSolver.addAttribute(IKVChainSolver.inHierarchyMode)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLength1)
        IKVChainSolver.addAttribute(IKVChainSolver.inRestLength2)
        IKVChainSolver.addAttribute(IKVChainSolver.inCompressionLimit)
        IKVChainSolver.addAttribute(IKVChainSolver.inSoftness)
        IKVChainSolver.addAttribute(IKVChainSolver.inStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampStretch)
        IKVChainSolver.addAttribute(IKVChainSolver.inClampValue)
        IKVChainSolver.addAttribute(IKVChainSolver.inSquash)
        IKVChainSolver.addAttribute(IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRoot, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHandle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inUpVector, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPreferredAngle, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inPvMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inTwist, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inHierarchyMode, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLength1, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inRestLength2, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inCompressionLimit, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSoftness, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampStretch, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inClampValue, IKVChainSolver.outChain)
        IKVChainSolver.attributeAffects(IKVChainSolver.inSquash, IKVChainSolver.outChain)

    def compute(self, plug, dataBlock):
        """
        Node computation method:
            * plug is a connection point related to one of our node attributes (either an input or an output).
            * dataBlock contains the data on which we will base our computations.
        """
        # pylint: disable=R0201
        if plug != IKVChainSolver.outChain:
            return om2.kUnknownParameter

        # Get basis matrix
        pvMode = dataBlock.inputValue(IKVChainSolver.inPvMode).asShort()
        mRoot = dataBlock.inputValue(IKVChainSolver.inRoot).asFloatMatrix()
        mHandle = dataBlock.inputValue(IKVChainSolver.inHandle).asFloatMatrix()
        mUpVector = dataBlock.inputValue(IKVChainSolver.inUpVector).asFloatMatrix()
        prefAngle = dataBlock.inputValue(IKVChainSolver.inPreferredAngle).asAngle().asRadians()
        twist = dataBlock.inputValue(IKVChainSolver.inTwist).asAngle().asRadians()
        vRoot = om2.MFloatVector(mRoot[12], mRoot[13], mRoot[14])
        vHandle = om2.MFloatVector(mHandle[12], mHandle[13], mHandle[14])
        vUpVector = om2.MFloatVector(mUpVector[12], mUpVector[13], mUpVector[14])
        vXDirection = vHandle - vRoot
        xDist = vXDirection.length()
        nXAxis = vXDirection.normal()
        if pvMode == 0:
            vUpDirection = vUpVector - vRoot
            vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis)
            nYAxis = vYDirection.normal()
        else:
            nYAxis = om2.MFloatVector(math.cos(prefAngle), 0.0, math.sin(prefAngle))
        nZAxis = nXAxis ^ nYAxis
        basis = [nXAxis.x, nXAxis.y, nXAxis.z, 0.0,
                 nYAxis.x, nYAxis.y, nYAxis.z, 0.0,
                 nZAxis.x, nZAxis.y, nZAxis.z, 0.0,
                 vRoot.x, vRoot.y, vRoot.z, 1.0]
        mBasisLocal = om2.MFloatMatrix(basis)
        mTwist = om2.MFloatMatrix()
        mTwist[5] = math.cos(twist)
        mTwist[6] = math.sin(twist)
        mTwist[9] = -math.sin(twist)
        mTwist[10] = math.cos(twist)
        if pvMode == 0:
            mBasis = mBasisLocal
        else:
            mBasis = mTwist * mBasisLocal

        # Solve triangle
        l1 = dataBlock.inputValue(IKVChainSolver.inRestLength1).asFloat()  # UpperArm
        l2 = dataBlock.inputValue(IKVChainSolver.inRestLength2).asFloat()  # Forearm
        compressionLimit = dataBlock.inputValue(IKVChainSolver.inCompressionLimit).asFloat()  # Rigid
        softValue = dataBlock.inputValue(IKVChainSolver.inSoftness).asFloat()
        l1m = l1 # * stretchMult1
        l2m = l2 # * stretchMult2
        chainLength = l1m + l2m
        l3rigid = max(min(xDist, chainLength), chainLength * compressionLimit)
        dc = chainLength
        da = (1.0 - softValue) * dc
        if xDist > da and softValue > 0:
            ds = dc - da
            l3soft = ds * (1.0 - math.pow(math.e, (da - xDist) / ds)) + da
            l3 = l3soft
        else:
            l3 = l3rigid

        # Angle mesurement
        hierarchyMode = dataBlock.inputValue(IKVChainSolver.inHierarchyMode).asBool()
        betaCos = (math.pow(l1m, 2.0) + math.pow(l3, 2.0) - math.pow(l2m, 2.0)) / (2.0 * l1m * l3)
        if betaCos < -1.0:
            betaCos = -1.0
        beta = math.acos(betaCos)
        betaSin = math.sin(beta)
        gammaCos = (math.pow(l1m, 2.0) + math.pow(l2m, 2.0) - math.pow(l3, 2.0)) / (2.0 * l1m * l2m)
        if gammaCos > 1.0:
            gammaCos = 1.0
        gamma = math.acos(gammaCos)
        if hierarchyMode:
            gammaComplement = gamma - math.pi
        else:
            gammaComplement = gamma + beta - math.pi
        gammaComplementCos = math.cos(gammaComplement)
        gammaComplementSin = math.sin(gammaComplement)
        alpha = math.pi - beta - gamma
        alphaCos = math.cos(alpha)
        alphaSin = math.sin(alpha)

        # Cartoony features
        stretch = dataBlock.inputValue(IKVChainSolver.inStretch).asFloat()
        if stretch > 0.0:
            clampStretch = dataBlock.inputValue(IKVChainSolver.inClampStretch).asFloat()
            clampStretchValue = dataBlock.inputValue(IKVChainSolver.inClampValue).asFloat()
            squash = dataBlock.inputValue(IKVChainSolver.inSquash).asFloat()
            if xDist > da and softValue > 0:
                scaleFactor = xDist / l3soft
            else:
                scaleFactor = xDist / chainLength
            if xDist >= da:
                clampFactor = (1.0 - clampStretch) * scaleFactor + clampStretch * min(scaleFactor, clampStretchValue)
                stretchFactor = (1.0 - stretch) + stretch * clampFactor
            else:
                stretchFactor = 1.0
            squashFactor = (1.0 - squash) + squash * (1.0 / math.sqrt(stretchFactor))
        else:
            stretchFactor = 1.0
            squashFactor = 1.0

        # Output transforms
        outChainHdle = dataBlock.outputArrayValue(IKVChainSolver.outChain)
        srtList = []
        if hierarchyMode:
            mScale = om2.MFloatMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MFloatMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = gammaComplementCos
            mLocal[1] = gammaComplementSin
            mLocal[4] = -gammaComplementSin
            mLocal[5] = gammaComplementCos
            mResult = mScale * mLocal
            mResult[12] = l1m
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = alphaCos
            mLocal[1] = alphaSin
            mLocal[4] = -alphaSin
            mLocal[5] = alphaCos
            mLocal[12] = l2m
            srtList.append(mLocal)
        else:
            mScale = om2.MFloatMatrix()
            mScale[0] = stretchFactor
            mScale[5] = squashFactor
            mScale[10] = squashFactor
            mLocal = om2.MFloatMatrix()
            mLocal[0] = betaCos
            mLocal[1] = betaSin
            mLocal[4] = -betaSin
            mLocal[5] = betaCos
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = om2.MFloatMatrix()
            mLocal[0] = gammaComplementCos
            mLocal[1] = gammaComplementSin
            mLocal[4] = -gammaComplementSin
            mLocal[5] = gammaComplementCos
            mLocal[12] = betaCos * l1m * stretchFactor
            mLocal[13] = betaSin * l1m * stretchFactor
            mResult = mScale * mLocal * mBasis
            srtList.append(mResult)
            mLocal = mHandle
            mLocal[12] = mBasis[12] + mBasis[0] * l3 * stretchFactor
            mLocal[13] = mBasis[13] + mBasis[1] * l3 * stretchFactor
            mLocal[14] = mBasis[14] + mBasis[2] * l3 * stretchFactor
            mResult = mScale * mLocal
            srtList.append(mResult)
        for i in range(len(outChainHdle)):
            outChainHdle.jumpToLogicalElement(i)
            resultHdle = outChainHdle.outputValue()
            if i < len(outChainHdle) and i < len(srtList):
                resultHdle.setMFloatMatrix(srtList[i])
            else:
                resultHdle.setMFloatMatrix(om2.MFloatMatrix())
        outChainHdle.setAllClean()