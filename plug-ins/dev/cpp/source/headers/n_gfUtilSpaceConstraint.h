/*
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

How to use:
    * Copy the plugin file to the MAYA_PLUG_IN_PATH.
    * To find MAYA_PLUG_IN_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_PLUG_IN_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Find the plugin file and import it. Can be:
        Windows: gfTools.mll
        OSX: gfTools.bundle
        Linux: gfTools.so

Requirements:
    * Maya 2017 or above.

Description:
    Custom aim constraint. Aim an object to another.

Attributes:
    * Up Vector Type: The type of calculation of the up vector.
    * Offset: The matrix offset between the source and target objects.
    * World Up Vector: The scene world up vector.
    * World Up Matrix: The world matrix of the up object.
    * Target World Matrix: The world matrix of the target object.
    * Target Weight: The weight of calculation.
    * Constraint World Matrix: The world matrix of the constrainted object.
    * Constraint Parent Inverse Matrix: The world inverse matrix of the parent of the constrainted object.
    * Constraint Joint Orient: The joint orient of the constrainted object (if exists).
    * Constraint Rotate Order: The rotate order of the constrainted object.
    * Constraint Parent Scale: The local scale of the parent of the constrainted object.
    * Out Constraint: The result euler rotation of the constraint.

Todo:
    * NDA

Sources:
    * NDA
*/
#pragma once

#include <vector>
#include <cstdint>
#include <algorithm>

#include <maya/MPxNode.h>

#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MVector.h>
#include <maya/MFloatVector.h>
#include <maya/MEulerRotation.h>
#include <maya/MPlugArray.h>
#include <maya/MFnDagNode.h>
#include <maya/MDagPath.h>


class SpaceConstraint : public MPxNode{
public:
    SpaceConstraint();
    virtual ~SpaceConstraint();

    virtual MStatus                     connectionMade(const MPlug &plug, 
                                                       const MPlug &otherPlug,
                                                       bool asSrc) override;
    virtual MStatus                     connectionBroken(const MPlug &plug,
                                                         const MPlug &otherPlug,
                                                         bool asSrc) override;

    virtual MStatus                     compute(const MPlug &plug, MDataBlock &dataBlock) override;
    virtual MPxNode::SchedulingType     schedulingType() const override;
    static MStatus                      initialize();
    static void*                        creator();

public:
    const static MString                kNodeName;
    const static MString                kNodeClassify;
    const static MTypeId                kNodeID;

    static MObject                      inSpace;
    static MObject                      inOffset;
    static MObject                      inTarget;
    static MObject                      inRestPose;
    static MObject                      inAutoFillOff;
    static MObject                      inSpaceMatch;
    static MObject                      outConstTrans;
    static MObject                      outConstRot;
    static MObject                      outConstSca;

private:
    void                                autoFillOffset(uint32_t &index);
    bool                                checkOutputConnections();

    short                               fLastSpace;
    MMatrix                             fOffsetMatch;
    MObject                             fConstraintObject;
};