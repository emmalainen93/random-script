from pymel.core import *
import pymel.core as pm
import maya.cmds as cmds
import random as rand

#------functions------
def buildSections():
    for f in range(1,3):
        duplicate()
        floor = pm.ls(sl=True)
        roomSize = floor[0].getBoundingBox(space='world')
        height = abs(roomSize[0][1] - roomSize[1][1])
        sections.append(floor[0])
        move(0, height, 0, relative = True)


def selectRandom(baseObjs):
    nextObject = rand.choice(baseObjs)
    #get meshIndex for original mesh, to find bBox & offset values
    mIndex = baseObjs.index(nextObject)
    pm.select(nextObject)
    duplicate()
    return mIndex 


def calcObjOffset(objOffset, obj):
    bBox = obj.getBoundingBox(space='world')
    #calculate half w/h/d to use as offset between mesh and wall 
    offsetX = (abs(bBox[0][0] - bBox[1][0])) /2
    offsetY = abs(bBox[0][1] - bBox[1][1])
    offsetZ = (abs(bBox[0][2] - bBox[1][2])) /2
    objOffset.append(offsetX)
    objOffset.append(offsetY)
    objOffset.append(offsetZ)


def checkIntersection(aDuplBox, aDuplBoxes, aMesh, aRoombBox, wall):
    tries = 0
    maxTries = 10
    intersection = False
    maxbBoxes = len(aDuplBoxes)
    aBoxCount  = 0
    
    while tries < maxTries and aBoxCount < maxbBoxes:
        
        #check intersection with other  objects
        for boxNr in range(0, len(aDuplBoxes)): 
            if aDuplBox.intersects(aDuplBoxes[boxNr], tol=0.0):
                intersection = True
                break
                
        if intersection == True:
            #update bBox value
            aDuplBox = placeObj(aRoombBox, aMesh, wall)
            intersection = False
            tries += 1
            if tries == maxTries:
                pm.delete()
                    
        else:
            aBoxCount += 1
            tries = 0
            break
    return aDuplBox


def placeObj(roomBox, mesh, wall):
    wt = 0.6 #wall thickness, for pre-created level
    #move mesh to new random pos
    if wall == 'b':
        cmds.move(rand.uniform((roomBox[0][0] + offsetX),(roomBox[1][0] - offsetX)),rand.uniform((roomBox[0][1]),(roomBox[1][1] - offsetY)),(roomBox[0][2] + offsetZ + wt), worldSpace=True)
    elif wall == 'r':
        cmds.move((roomBox[1][0] - offsetZ - wt),rand.uniform((roomBox[0][1] + offsetY),(roomBox[1][1] - offsetY)),rand.uniform((roomBox[0][2] + offsetX),(roomBox[1][2] - offsetX)), worldSpace=True)
    elif wall == 'l':
        cmds.move((roomBox[0][0] + offsetZ + wt),rand.uniform((roomBox[0][1] + offsetY),(roomBox[1][1] - offsetY)),rand.uniform((roomBox[0][2] + offsetX),(roomBox[1][2] - offsetX)), worldSpace=True)

    duplBox = mesh[0].getBoundingBox(space='world')
    return duplBox


#-----create list of sections-----
def listWalls():
	sections = pm.ls(sl=True)
	return sections

#------get list of base-objekts to place randomly on walls------
def listPlaceables():
	baseObjs = pm.ls(sl=True)
	return baseObjs

#-----list manually placed meshes to avoid-----
def listPlaced():
	prevMeshes = pm.ls(sl=True)
	return prevMeshes

def setNr(nr):
	randomNr = nr
	return randomNr


def placeRandom(baseObjs, sections, prevMeshes, randomNr):
	global offsetX
	global offsetY
	global offsetZ
	bMeshes=[]
	rMeshes=[]
	lMeshes=[]
	
	#list of baseObjs offsets
	baseOffsets = []
	for o in range(0, len(baseObjs)):
		objOffset=[]
		obj = baseObjs[o]
		calcObjOffset(objOffset, obj)
		baseOffsets.append(objOffset)

	prevBoxes=[]
	for p in range(0, len(prevMeshes)):
		box = prevMeshes[p].getBoundingBox(space='world')
		prevBoxes.append(box)

	#for every floor, go througt r/b/l wall & place objects
	for floors in range(0,len(sections)):
		#get bbox for current section
		roomBbox = sections[floors].getBoundingBox(space='world')

		#list boudingBoxes for this floor, for each wall
		bDuplBoxes=[]
		rDuplBoxes=[]
		lDuplBoxes=[]

		removeList=[]
		#if previously placed meshes is within current floor, add to list of meshes to avoid
		if len(prevBoxes) > 0:
			for pNr in range(0, len(prevBoxes)):
				if roomBbox.intersects(prevBoxes[pNr], tol=0.0):
					bDuplBoxes.append(prevBoxes[pNr])
					rDuplBoxes.append(prevBoxes[pNr])
					lDuplBoxes.append(prevBoxes[pNr])

					if floors <= (len(sections)-2): #if this floor is not top floor
						#print floors      
						nextRoom = sections[floors+1].getBoundingBox(space='world')
						if not nextRoom.intersects(prevBoxes[pNr], tol=0.0):
							removeList.append(prevBoxes[pNr])

			for remove in range(0, len(removeList)):
				prevBoxes.remove(removeList[remove])


		#place on back wall
		for b in range(0,randomNr):
			wall = 'b'

			#get random object & mesh index
			meshIndex = selectRandom(baseObjs)
			bMesh = pm.ls(sl=True)

			#access prevoiusly calculated offsets using mesh index
			offsetX = baseOffsets[meshIndex][0]
			offsetY = baseOffsets[meshIndex][1]
			offsetZ = baseOffsets[meshIndex][2]
			
			#place randomly on back wall & get bBox pos
			bDuplBox = placeObj(roomBbox, bMesh, wall)
			
			#check intersection, move mesh if needed
			if len(bDuplBoxes) > 0:
				bDuplBox = checkIntersection(bDuplBox, bDuplBoxes, bMesh, roomBbox, wall)

			#make sure script does not add a mesh (& bBox) that is deleted to list.
			if pm.objExists(bMesh[0]):
				#add this mesh & bBox to list
				bDuplBoxes.append(bDuplBox)
				bMeshes.append(bMesh)


		#add back wall meshes to r & l bBox list to make sure there is no intersection between wall meshes
		for t in range(0, len(bDuplBoxes)):
			rDuplBoxes.append(bDuplBoxes[t])
			lDuplBoxes.append(bDuplBoxes[t])


		#place on right wall
		for r in range(0,randomNr):

			wall = 'r'

			meshIndex = selectRandom(baseObjs)
			rMesh = pm.ls(sl=True)

			pm.rotate(0, 0, -90, r=True)

			offsetX = baseOffsets[meshIndex][0]
			offsetY = baseOffsets[meshIndex][1]
			offsetZ = baseOffsets[meshIndex][2]

			#place on wall (use offset Z for X and offset X for z, since object is rotated) & get bBox
			rDuplBox = placeObj(roomBbox, rMesh, wall)

			if len(rDuplBoxes) > 0:
				rDuplBox = checkIntersection(rDuplBox, rDuplBoxes, rMesh, roomBbox, wall)

			if pm.objExists(rMesh[0]):
				rDuplBoxes.append(rDuplBox)
				rMeshes.append(rMesh)


		#place on left wall
		for l in range(0,randomNr):

			wall = 'l'

			meshIndex = selectRandom(baseObjs)
			lMesh = pm.ls(sl=True)

			pm.rotate(0, 0, 90, r=True)

			offsetX = baseOffsets[meshIndex][0]
			offsetY = baseOffsets[meshIndex][1]
			offsetZ = baseOffsets[meshIndex][2]
			
			lDuplBox = placeObj(roomBbox, lMesh, wall)

			if len(lDuplBoxes) > 0:
				lDuplBox = checkIntersection(lDuplBox, lDuplBoxes, lMesh, roomBbox, wall)

			if pm.objExists(lMesh[0]):
				lDuplBoxes.append(lDuplBox)
				lMeshes.append(lMesh)

	print 'done!'