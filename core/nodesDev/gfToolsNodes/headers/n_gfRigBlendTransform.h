#pragma once

#include <vector>
#include <algorithm>
#include <cstdint>

#include <maya\MPxNode.h>

#include <maya\MFnNumericAttribute.h>
#include <maya\MFnUnitAttribute.h>
#include <maya\MFnCompoundAttribute.h>
#include <maya\MFnEnumAttribute.h>
#include <maya\MFloatVector.h>
#include <maya\MVector.h>
#include <maya\MEulerRotation.h>
#include <maya\MQuaternion.h>


struct VisibilityData {
	bool visibility;
	bool reverseVisibility;
};


class BlendTransform : public MPxNode {
public:
	BlendTransform();
	virtual ~BlendTransform();

	virtual MPxNode::SchedulingType schedulingType() {
		return MPxNode::SchedulingType::kParallel;
	}

	virtual MStatus								compute(const MPlug& plug, MDataBlock& dataBlock);
	static MStatus								initialize();
	static void*								creator();

	static VisibilityData						visibilityCalculation(float blender);
public:
	const static MString						kNODE_NAME;
	const static MString						kNODE_CLASSIFY;
	const static MTypeId						kNODE_ID;

	static MObject								inBlender;
	static MObject								inRotInterp;
	static MObject								inTrans1;
	static MObject								inRot1;
	static MObject								inSca1;
	static MObject								inTransform1;
	static MObject								inTrans2;
	static MObject								inRot2;
	static MObject								inSca2;
	static MObject								inTransform2;
	static MObject								outTrans;
	static MObject								outRot;
	static MObject								outSca;
	static MObject								outVis;
	static MObject								outRevVis;
};