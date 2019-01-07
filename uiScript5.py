from pymel import*
import pymel.core as pm
import maya.cmds as cmds

import ModuleScript as ms
reload(ms)


def listPlaceables(*args): #wants *args, but does not need to use it
    print 'Listing placeables' #'%s' %(args, )
    #put placeables in list
    placeables=[]
    placeables = ms.listPlaceables()
    placeableList.append(placeables)
    
    
def listWalls(*args):
    print 'Listing walls'
    #put walls in list
    walls=[]
    walls = ms.listWalls()
    wallsList.append(walls)


def listPlacedMeshes(*args):
    print'Listing already placed meshes'
    #put placed meshes in list
    placed=[]
    placed = ms.listPlaced()
    placedList.append(placed)

def sliderNr(value):
    ms.setNr(value)

def placeRandom(*args):
    print'place radom meshes'
    ms.placeRandom()



pm.window(title="Place random meshes", widthHeight=(495,450))


row1 = pm.rowColumnLayout(numberOfRows=3)

row2=pm.rowColumnLayout(numberOfRows=3, parent=row1)
textForm = pm.formLayout(parent=row2)
textLine = pm.text(label='Select objects and press button to add to list:', align='left')
pm.formLayout(textForm, edit=True, attachForm=[(textLine, 'top', 10),(textLine, 'left', 10), (textLine,'bottom',15)])

row11 = pm.rowColumnLayout(numberOfColumns=3, columnSpacing=[(1,35), (2,60), (3,60)], rowOffset=[(1,'bottom',10)], parent=row2)
placeableButton = pm.button(label = 'List placeables', command=listPlaceables, width = 100)
wallsButton = pm.button(label = 'List walls', command=listWalls, width = 100)
placedButton = pm.button(label = 'List placed', command=listPlacedMeshes, width = 100)

row12 = pm.rowColumnLayout(numberOfColumns=3, columnSpacing=[(1,10), (2,10), (3,10)], parent=row2)
placeableList = pm.textScrollList(numberOfRows = 18, parent = row12, width = 150)
wallsList = pm.textScrollList(numberOfRows = 18, parent = row12, width = 150)
placedList = pm.textScrollList(numberOfRows = 18, parent = row12, width = 150)


formSlider = pm.formLayout(numberOfDivisions = 100, parent=row1)
slider = pm.intSliderGrp(field=True, label='Nr of objects to place:', minValue=1, maxValue=50, fieldMinValue=1, fieldMaxValue=50, step=1, changeCommand=sliderNr)
pm.formLayout(formSlider, edit=True, attachForm=[(slider, 'top', 10)])


form = pm.formLayout(numberOfDivisions = 100, parent=row1)
scriptButton = pm.button(label = 'Place random', width=100, command=placeRandom)
pm.formLayout(form, edit=True, attachForm=[(scriptButton, 'top', 20),(scriptButton, 'left', 200)])


pm.showWindow()


