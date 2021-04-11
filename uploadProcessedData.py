import serial, time, colorsys
from math import *
from vpython import canvas, sphere, color, vector, arrow, text, wtext, checkbox

window = canvas(title='3D Room Scan', width=600, height=600, background=color.white) 

showUnreliablePoints = 1
spheres = []

def showDistance():
    hudShowStrength.checked = False
    for i in spheres:
        i.setColor("distance")

def showStrength():
    hudShowDist.checked = False
    for i in spheres:
        i.setColor("strength")

def showUnreliable():
    global showUnreliablePoints
    showUnreliablePoints = 1 - showUnreliablePoints
    if showUnreliablePoints == 0:
        for i in spheres:
            i.hideUnreliable()
    elif showUnreliablePoints == 1:
        for i in spheres:
            i.showPoint()

def HSLtoRGB(value, saturation, lightness, minimum, maximum):
    HUE = (value - minimum)/(maximum-minimum)*250 # 250 is the upper end of blue hue
    R = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[0]
    G = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[1]
    B = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[2]
    print(value, minimum, maximum, HUE, saturation, lightness, R, G, B)
    return R, G, B

def getPoint(panValue, tiltValue):
    for i in spheres:
        if i.Pan == panValue and i.Tilt == tiltValue:
            return i.Dist, i.Strength

class createPoints():
    def __init__(self, X, Y, Z, DistR, DistG, DistB, StrengthR, StrengthG, StrengthB, reliable):
        self.Xpos, self.Ypos, self.Zpos = X, Y, Z
        self.DistRGB = vector(float(DistR), float(DistG), float(DistB))
        self.StrengthRGB = vector(float(StrengthR), float(StrengthG), float(StrengthB))
        self.reliable = reliable

    def hideUnreliable(self):
        if self.reliable == 0:
            self.Pos.visible = False
    
    def showPoint(self):
        self.Pos.visible = True

    def addPoint(self):
        global lineToPoint
        lineToPoint.axis=vector(self.Xpos, self.Ypos, self.Zpos)
        self.Pos = sphere(pos = vector(self.Xpos, self.Ypos, self.Zpos), radius = 1, color = vector(0,0,0), canvas = window, make_trail=False)
        self.hideUnreliable()

    def setColor(self, showBasedOn):
        if showBasedOn == "distance":
            self.RGBColor = self.DistRGB
        elif showBasedOn == "strength":
            self.RGBColor = self.StrengthRGB
        else:
            self.RGBColor = (0,0,0)

        self.Pos.color = vector(self.RGBColor[0], self.RGBColor[1], self.RGBColor[2])
    
    def getData(self):
        return str(self.Xpos) + " " + str(self.Ypos) + " " + str(self.Zpos) + " " + str(HSLtoRGB(self.Dist, 100, 50, distMinValue, distMaxValue)[0]) + " " + str(HSLtoRGB(self.Dist, 100, 50, distMinValue, distMaxValue)[1]) + " " + str(HSLtoRGB(self.Dist, 100, 50, distMinValue, distMaxValue)[2]) + " " + str(HSLtoRGB(self.Strength, 100, 50, strengthMinValue, strengthMaxValue)[0]) + " " + str(HSLtoRGB(self.Strength, 100, 50, strengthMinValue, strengthMaxValue)[1]) + " " + str(HSLtoRGB(self.Strength, 100, 50, strengthMinValue, strengthMaxValue)[2]) +"\n"

origin = sphere(pos = vector(0,0,0), radius = 3, color = color.green, canvas = window, make_trail=True)
Xaxis = arrow(pos=vector(0,0,0), axis=vector(100,0,0), shaftwidth=1, color=vector(1,0,0))
Yaxis = arrow(pos=vector(0,0,0), axis=vector(0,100,0), shaftwidth=1, color=vector(0,1,0))
Zaxis = arrow(pos=vector(0,0,0), axis=vector(0,0,100), shaftwidth=1, color=vector(0,0,1))
onX50 = text(text="50cm", align='center', color=vector(1,0,0), pos=vector(50,2,0))
onY50 = text(text="50cm", align='center', color=vector(0,1,0), pos=vector(4,50,0))
onZ50 = text(text="50cm", align='center', color=vector(0,0,1), pos=vector(0,2,50))
onX100 = text(text="100cm", align='center', color=vector(1,0,0), pos=vector(100,2,0))
onY100 = text(text="100cm", align='center', color=vector(0,1,0), pos=vector(4,100,0))
onZ100 = text(text="100cm", align='center', color=vector(0,0,1), pos=vector(0,2,100))
lineToPoint = arrow(pos=vector(0,0,0), axis=vector(0,0,0), shaftwidth=1, color=vector(0,1,1))

hudDist = wtext(pos = window.caption_anchor, text = "Distance ")
hudStrength = wtext(pos = window.caption_anchor, text = "Strength ")
hudPan = wtext(pos = window.caption_anchor, text = "Pan ")
hudTilt = wtext(pos = window.caption_anchor, text = "Tilt ")
hudShowDist = checkbox(pos = window.caption_anchor, text = "Show distance", bind=showDistance)
hudShowStrength = checkbox(pos = window.caption_anchor, text = "Show Strength", bind=showStrength)
hudShowUnreliable = checkbox(pos = window.caption_anchor, text = "Show filtered", bind=showUnreliable)
hudShowDist.checked = True
hudShowUnreliable.checked = True
hudShowDist.disabled = True
hudShowStrength.disabled = True
hudShowUnreliable.disabled = True

onX50.length *= 2
onY50.length *= 2
onZ50.length *= 2
onX100.length *= 2
onY100.length *= 2
onZ100.length *= 2

onX50.height *= 2
onY50.height *= 2
onZ50.height *= 2
onX100.height *= 2
onY100.height *= 2
onZ100.height *= 2

def main(fileLocation):
    openFile = open(fileLocation, "r")
    for line in openFile:
        temp = line.split(" ")
        spheres.append(createPoints(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9]))
        spheres[-1].addPoint()
    for i in spheres:
        i.setColor("distance") 
    hudShowDist.disabled = False
    hudShowStrength.disabled = False
    hudShowUnreliable.disabled = False