from math import *
props = fp.PropertiesList
if not 'pitch' in  props:
	fp.addProperty("App::PropertyLength","pitch","params","params").pitch=5.0
pitch = float(fp.pitch)
if not 'precision' in props:
	fp.addProperty("App::PropertyInteger","precision","params","params").precision=32
fn = fp.precision
if not 'height' in props:
	fp.addProperty("App::PropertyLength","height","params","params").height=16.0
height = float(fp.height)
if not 'radius' in props:
	fp.addProperty("App::PropertyLength","radius","params","params").radius=16.0
radius = float(fp.radius)
if not 'rope_radius' in props:
	fp.addProperty("App::PropertyLength","rope_radius","params","params").rope_radius=1.0
rope_radius = float(fp.rope_radius)

import time
t = time.time()

angle = degrees(asin(pitch / (radius * 2.0 * pi)))
slope = FreeCAD.Rotation(FreeCAD.Vector(1,0,0),angle)
v = slope.multVec(FreeCAD.Vector(0,1,0))
base = Part.makeCircle(rope_radius,FreeCAD.Vector(radius,0,0),v)
base = Part.makePolygon([FreeCAD.Vector(radius+rope_radius,0,rope_radius),FreeCAD.Vector(radius+rope_radius,0,-rope_radius),FreeCAD.Vector(radius-rope_radius,0,-rope_radius),FreeCAD.Vector(radius-rope_radius,0,rope_radius),FreeCAD.Vector(radius+rope_radius,0,rope_radius)])

v = FreeCAD.Vector(0,0,rope_radius)
poly = [FreeCAD.Vector(10,0,-rope_radius), FreeCAD.Vector(10,0,rope_radius)]
for i in range(0,-180-30, -60):
	poly.append(FreeCAD.Rotation(0,i,0).multVec(v))
poly.append(poly[0])

base = Part.makePolygon(poly)
base.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0), angle)
base.translate(FreeCAD.Vector(radius,0,0))
#base.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0),1)

poly=[]
for i in range(0,-360, -60):
	poly.append(FreeCAD.Rotation(0,i,0).multVec(v))
poly.append(poly[0])

fixation = Part.makePolygon(poly)
fixation.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(1,0,0), angle)
fixation.translate(FreeCAD.Vector(radius,0,0))

wires1 = []
parts = int(ceil(fn/3.0))
for i in range(0,parts+1):
	circle = fixation.copy()
	circle.rotate(FreeCAD.Vector(radius*0.33,0,0),FreeCAD.Vector(0,0,1), (-i*360.0/fn))
	circle.translate(FreeCAD.Vector(0,0,-i * pitch/fn))
	wires1.append(circle)
fixation = circle.copy()

axe = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),(-(parts)*360.0/fn)).multVec(FreeCAD.Vector(1,0,0))
center = FreeCAD.Vector(radius*0.33,0,-2*pitch)
parts = int(ceil(fn/4.0))
for i in range(0,parts+1):
	circle = fixation.copy()
	circle.rotate(center,axe, (i*360.0/fn))
	wires1.append(circle)


wires2 = []
parts = int(ceil(fn * height/pitch))
for i in range(0,parts+1):
	circle = base.copy()
	circle.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1), i*360.0/fn)
	circle.translate(FreeCAD.Vector(0,0,i * pitch/fn))
	wires2.append(circle)
FreeCAD.Console.PrintMessage( '\ncircles ')
FreeCAD.Console.PrintMessage( time.time() -t)
t = time.time()



r = FreeCAD.Rotation(FreeCAD.Vector(0,0,1), i*360.0/fn)
r = r.multiply(slope)
v = r.multVec(FreeCAD.Vector(0,1,0))
circle = circle.copy()
circle.translate(v*2.0*radius)
wires2.append(circle)
loft1 = Part.makeLoft(wires1,True,True)
loft2 = Part.makeLoft(wires2,True,True)

fp.Shape = loft1.fuse(loft2)
FreeCAD.Console.PrintMessage( '\nshape ')
FreeCAD.Console.PrintMessage( time.time()-t)
t = time.time()
