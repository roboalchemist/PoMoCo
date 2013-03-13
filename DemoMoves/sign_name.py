# get console input from user
from Tkinter import *
import tkSimpleDialog
import time
from itertools import repeat
import math
 
# define Inverse Kinematic function for lower leg joints
# variable definitions: http://robcook.eu/hexy/inverse-kinematics-part-1/
def ikLowerLeg(x, y):
    #print "IK function called. x=", x, "y=", y
    a = 49.0
    b = 52.0
    try:
        d = math.sqrt(x*x+y*y)
        k = (d*d-b*b+a*a)/(2*d)
        m = math.sqrt(a*a-k*k)
    except ZeroDivisionError:
        print "Divide by Zero error. No valid joint solution."
        return
    except ValueError:
        print "Math function error. Probably square root of negative number. No valid joint solution."
        return
    theta = math.degrees(math.atan2(float(y),float(x))-math.atan2(m,k))
    phi   = -math.degrees(math.atan2(m,k)+math.atan2(m,(d-k)))
    returnAngles = [theta, phi]
    #print "theta=", theta, "phi=", phi
    return returnAngles        

# define Inverse Kinematic function for full leg
# variable definitions: http://robcook.eu/hexy/inverse-kinematics-part-3-full-leg-solution/
def ikFullLeg(x, y, z):
    alpha = math.degrees(math.atan2(y, x))
    lowerLegAngles = ikLowerLeg(math.sqrt(x*x+y*y)-26.0, z)
    #print "ikFullLeg ", alpha, lowerLegAngles[0], lowerLegAngles[1]
    returnAngles = [alpha, lowerLegAngles[0], lowerLegAngles[1]] 
    return returnAngles

# move LF leg in global co-ordinate system
def hexyLFleg(x,y,z):
    #print "LF leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x + 65.8
    y = y - 76.3
    # rotate to leg zero position
    legx=math.cos(-2.2829)*x-math.sin(-2.2829)*y
    legy=math.sin(-2.2829)*x+math.cos(-2.2829)*y
    # get IK solution and move leg
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.LF.hip(legAngles[0])
    hexy.LF.knee(legAngles[1])
    hexy.LF.ankle(legAngles[2])
    
# move LM leg in global co-ordinate system
def hexyLMleg(x,y,z):
    #print "LM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = -(x + 103.3)
    y = -y
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.LM.hip(legAngles[0])
    hexy.LM.knee(legAngles[1])
    hexy.LM.ankle(legAngles[2])
    
# move LB leg in global co-ordinate system
def hexyLBleg(x,y,z):
    #print "LB leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x + 65.8
    y = y + 76.3
    # rotate to leg zero position
    legx=math.cos(2.2829)*x-math.sin(2.2829)*y
    legy=math.sin(2.2829)*x+math.cos(2.2829)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.LB.hip(legAngles[0])
    hexy.LB.knee(legAngles[1])
    hexy.LB.ankle(legAngles[2])
    
# move RF leg in global co-ordinate system
def hexyRFleg(x,y,z):
    #print "RF leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 65.8
    y = y - 76.3
    # rotate to leg zero position
    legx=math.cos(-0.8587)*x-math.sin(-0.8587)*y
    legy=math.sin(-0.8587)*x+math.cos(-0.8587)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.RF.hip(legAngles[0])
    hexy.RF.knee(legAngles[1])
    hexy.RF.ankle(legAngles[2])
    
# move RM leg in global co-ordinate system
def hexyRMleg(x,y,z):
    #print "RM leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 103.3
    # rotate to leg zero position
    legAngles = ikFullLeg(x,y,-z)
    hexy.RM.hip(legAngles[0])
    hexy.RM.knee(legAngles[1])
    hexy.RM.ankle(legAngles[2])
    
# move RB leg in global co-ordinate system
def hexyRBleg(x,y,z):
    #print "RB leg"
    # translate hexy co-ordinate to leg co-ordinate
    x = x - 65.8
    y = y + 76.3
    # rotate to leg zero position
    legx=math.cos(0.8587)*x-math.sin(0.8587)*y
    legy=math.sin(0.8587)*x+math.cos(0.8587)*y
    # rotate to leg zero position
    legAngles = ikFullLeg(legx,legy,-z)
    hexy.RB.hip(legAngles[0])
    hexy.RB.knee(legAngles[1])
    hexy.RB.ankle(legAngles[2])
    
# move Hexy to position relative to "neutral" position
def hexyGlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)

# move Hexy to position relative to "neutral" position
def hexyTripod1GlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLFleg(-neuX-x, neuY-y, neuZ-z)
    hexyLBleg(-neuX-x, -neuY-y, neuZ-z)
    hexyRMleg(neuXmid-x, -y, neuZ-z)
 
# move Hexy to position relative to "neutral" position
def hexyTripod2GlobalOffset(x,y,z):
    # neutral position definintion
    neuZ = -85
    neuY = 110
    neuX = 110
    neuXmid = 150
    # move hexy to a position relative to "neutral"
    hexyLMleg(-neuXmid-x, -y, neuZ-z)
    hexyRFleg(neuX-x, neuY-y, neuZ-z)
    hexyRBleg(neuX-x, -neuY-y, neuZ-z)

def letterPath(l):
    penDownHeight = -7
                                             
    if l == "A":
        x = [-0.264, -0.010, 0.257, 0.160, -0.173]
        y = [-0.336, 0.323, -0.340, -0.101, -0.101]
    elif l == "B":
        x = [-0.198, -0.198, 0.035, 0.160, 0.049, -0.198, 0.101, 0.232, 0.101, -0.191]
        y = [-0.302, 0.284, 0.277, 0.142, 0.003, -0.000, 0.003, -0.153, -0.305, -0.309]
    elif l == "C":
        x = [0.229, 0.014, -0.218, -0.222, 0.017, 0.246]
        y = [0.135, 0.295, 0.180, -0.198, -0.316, -0.132]
    elif l == "D":
        x = [-0.212, -0.222, 0.059, 0.201, 0.246, 0.187, 0.021, -0.218]
        y = [-0.305, 0.284, 0.277, 0.184, -0.003, -0.243, -0.309, -0.305]
    elif l == "E":
        x = [0.232, -0.184, -0.187, 0.218, 0.218, 0.125, 0.125, -0.184]
        y = [-0.305, -0.302, 0.284, 0.281, 0.281, 0.003, 0.003, 0.003]
        z = [penDownHeight, penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "F":
        x = [-0.163, -0.163, 0.232, 0.232, 0.184, 0.184, -0.166]
        y = [-0.329, 0.281, 0.281, 0.281, -0.000, -0.000, 0.003]
        z = [penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "G":
        x = [0.253, 0.121, -0.111, -0.250, -0.267, -0.160, 0.059, 0.267, 0.257, 0.035]
        y = [0.125, 0.284, 0.277, 0.146, -0.097, -0.271, -0.316, -0.222, -0.049, -0.049]
    elif l == "H":
        x = [-0.218, -0.215, -0.215, 0.218, 0.215, 0.218]
        y = [0.312, -0.333, 0.010, 0.010, 0.316, -0.340]
    elif l == "I":
        x = [0.000, 0.000]
        y = [0.323, -0.340]
    elif l == "J":
        x = [0.114, 0.108, -0.031, -0.173]
        y = [0.319, -0.187, -0.326, -0.156]
    elif l == "K":
        x = [-0.198, -0.198, -0.198, 0.222, -0.042, 0.243]
        y = [0.319, -0.343, -0.108, 0.312, 0.045, -0.329]
    elif l == "L":
        x = [-0.139, -0.149, 0.232]
        y = [0.319, -0.305, -0.305]
    elif l == "M":
        x = [-0.274, -0.274, 0.003, 0.277, 0.277]
        y = [-0.340, 0.312, -0.329, 0.319, -0.340]
    elif l == "N":
        x = [-0.215, -0.212, 0.218, 0.218]
        y = [-0.336, 0.319, -0.333, 0.323]
    elif l == "O":
        x = [0.007, -0.215, -0.284, -0.198, 0.000, 0.191, 0.277, 0.201, -0.003]
        y = [0.302, 0.222, -0.024, -0.239, -0.319, -0.246, -0.003, 0.212, 0.298]
    elif l == "P":
        x = [-0.191, -0.191, 0.090, 0.225, 0.094, -0.187]
        y = [-0.340, 0.288, 0.284, 0.132, -0.038, -0.038]
    elif l == "Q":
        x = [0.156, -0.014, -0.218, -0.274, -0.208, -0.003, 0.205, 0.274, 0.149, 0.319]
        y = [-0.257, -0.316, -0.225, -0.010, 0.212, 0.288, 0.194, -0.014, -0.260, -0.368]
    elif l == "R":
        x = [-0.218, -0.218, 0.069, 0.225, 0.038, -0.215, 0.035, 0.257]
        y = [-0.329, 0.291, 0.284, 0.139, -0.017, -0.007, -0.014, -0.326]
    elif l == "S":
        x = [0.208, 0.000, -0.201, -0.111, 0.128, 0.222, 0.055, -0.160, -0.229]
        y = [0.163, 0.291, 0.173, 0.038, -0.031, -0.180, -0.316, -0.271, -0.132]
    elif l == "T":
        x = [-0.264, 0.260, -0.003, -0.003]
        y = [0.277, 0.281, 0.271, -0.333]
    elif l == "U":
        x = [-0.215, -0.212, -0.111, 0.104, 0.208, 0.215]
        y = [0.323, -0.146, -0.295, -0.302, -0.166, 0.316]
    elif l == "V":
        x = [-0.246, 0.007, 0.260]
        y = [0.319, -0.336, 0.316]
    elif l == "W":
        x = [-0.378, -0.201, 0.003, 0.205, 0.381]
        y = [0.319, -0.336, 0.323, -0.343, 0.319]
    elif l == "X":
        x = [-0.222, 0.243, 0.243, 0.232, 0.232, -0.250]
        y = [0.323, -0.336, -0.336, 0.319, 0.319, -0.340]
        z = [penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "Y":
        x = [-0.253, -0.003, -0.003, -0.003, 0.246]
        y = [0.319, -0.042, -0.333, -0.049, 0.312]
    elif l == "Z":
        x = [-0.225, 0.239, -0.260, 0.250]
        y = [0.277, 0.281, -0.305, -0.305]
    elif l == "a":
        x = [-0.163, -0.003, 0.156, 0.173, -0.108, -0.170, -0.076, 0.166]
        y = [0.021, 0.111, 0.049, -0.316, -0.326, -0.194, -0.090, -0.069]
    elif l == "b":
        x = [-0.156, -0.156, 0.087, 0.170, 0.153, 0.003, -0.149]
        y = [0.316, -0.329, -0.316, -0.156, 0.042, 0.125, 0.003]
    elif l == "c":
        x = [0.177, 0.021, -0.142, -0.142, 0.024, 0.194]
        y = [-0.003, 0.114, 0.031, -0.215, -0.326, -0.184]
    elif l == "d":
        x = [0.153, 0.156, -0.073, -0.187, -0.173, -0.038, 0.156]
        y = [0.323, -0.333, -0.316, -0.170, 0.031, 0.114, 0.014]
    elif l == "e":
        x = [-0.170, 0.184, 0.101, -0.108, -0.191, -0.104, 0.090, 0.166]
        y = [-0.090, -0.087, 0.090, 0.097, -0.097, -0.295, -0.323, -0.232]
    elif l == "f":
        x = [-0.010, -0.007, 0.135, 0.135, 0.111, 0.111, -0.118]
        y = [-0.336, 0.215, 0.302, 0.302, 0.104, 0.104, 0.108]
        z = [penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "g":
        x = [0.156, -0.021, -0.177, -0.177, 0.000, 0.160, 0.149, -0.014, -0.177]
        y = [-0.212, -0.305, -0.166, 0.049, 0.121, 0.104, -0.420, -0.506, -0.427]
    elif l == "h":
        x = [-0.153, -0.149, -0.156, 0.045, 0.160, 0.160]
        y = [0.316, -0.336, -0.017, 0.121, 0.017, -0.340]
    elif l == "i":
        x = [0.003, 0.003, 0.003, 0.003, 0.003]
        y = [-0.340, 0.135, 0.135, 0.302, 0.302]
        z = [penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight]
    elif l == "j":
        x = [-0.003, -0.003, -0.003, -0.003, 0.000, -0.146]
        y = [0.277, 0.277, 0.111, 0.111, -0.413, -0.510]
        z = [penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight, penDownHeight]
    elif l == "k":
        x = [-0.121, -0.121, -0.121, 0.118, -0.021, 0.173]
        y = [0.323, -0.329, -0.142, 0.104, -0.038, -0.329]
    elif l == "l":
        x = [0.000, 0.000]
        y = [0.316, -0.336]
    elif l == "m":
        x = [-0.284, -0.277, -0.125, 0.000, 0.010, 0.014, 0.198, 0.298, 0.295]
        y = [-0.340, 0.080, 0.132, 0.066, -0.343, 0.024, 0.128, 0.014, -0.336]
    elif l == "n":
        x = [-0.146, -0.156, 0.038, 0.153, 0.156]
        y = [-0.343, 0.069, 0.132, 0.021, -0.336]
    elif l == "o":
        x = [0.000, -0.153, -0.184, -0.118, 0.003, 0.142, 0.187, 0.125, -0.010]
        y = [0.128, 0.059, -0.121, -0.284, -0.329, -0.264, -0.101, 0.073, 0.125]
    elif l == "p":
        x = [-0.156, -0.160, 0.042, 0.198, 0.059, -0.156]
        y = [-0.517, 0.114, 0.125, -0.101, -0.326, -0.246]
    elif l == "q":
        x = [0.163, 0.160, -0.073, -0.184, -0.146, -0.021, 0.156]
        y = [-0.524, 0.135, 0.125, -0.021, -0.260, -0.319, -0.229]
    elif l == "r":
        x = [-0.052, -0.055, 0.166]
        y = [-0.340, 0.132, 0.111]
    elif l == "s":
        x = [0.146, 0.000, -0.149, -0.097, 0.087, 0.163, 0.066, -0.097, -0.166]
        y = [0.024, 0.128, 0.031, -0.066, -0.121, -0.212, -0.323, -0.295, -0.212]
    elif l == "t":
        x = [0.135, -0.010, -0.014, -0.014, -0.108, -0.108, 0.108]
        y = [-0.312, -0.298, 0.281, 0.281, 0.108, 0.108, 0.108]
        z = [penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "u":
        x = [-0.153, -0.160, -0.062, 0.163, 0.160]
        y = [0.142, -0.212, -0.323, -0.291, 0.142]
    elif l == "v":
        x = [-0.170, -0.003, 0.173]
        y = [0.139, -0.336, 0.135]
    elif l == "w":
        x = [-0.291, -0.146, 0.000, 0.139, 0.288]
        y = [0.135, -0.336, 0.142, -0.340, 0.139]
    elif l == "x":
        x = [-0.153, 0.166, 0.166, 0.160, 0.160, -0.173]
        y = [0.135, -0.340, -0.340, 0.139, 0.139, -0.340]
        z = [penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "y":
        x = [-0.166, 0.014, 0.187, -0.083, -0.191]
        y = [0.135, -0.336, 0.135, -0.496, -0.492]
    elif l == "z":
        x = [-0.191, 0.205, -0.212, 0.205]
        y = [0.108, 0.111, -0.305, -0.302]
    elif l == ",":
        x = [0.003, -0.038]
        y = [-0.291, -0.451]
    elif l == ".":
        x = [0.000, 0.0]
        y = [-0.298, -0.298]
    elif l == "!":
        x = [0.003, 0.003, 0.003, 0.000, 0.000]
        y = [0.323, -0.166, -0.166, -0.298, -0.298]
        z = [penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight]
    elif l == "?":
        x = [-0.170, 0.010, 0.180, 0.003, -0.010, -0.010, -0.010, -0.010]
        y = [0.156, 0.312, 0.149, -0.049, -0.170, -0.170, -0.302, -0.302]
        z = [penDownHeight, penDownHeight, penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight]
    elif l == "'":
        x = [0.000, -0.007]
        y = [0.309, 0.094]
    elif l == "@":
        x = [0.111, -0.090, -0.191, -0.163, -0.017, 0.128, 0.104, 0.128, 0.284, 0.364, 0.368, 0.253, 0.118, -0.055, -0.260, -0.357, -0.406, -0.368, -0.298, -0.173, -0.045, 0.094, 0.225, 0.319, 0.395]
        y = [-0.163, -0.312, -0.212, 0.003, 0.135, 0.024, -0.215, -0.312, -0.246, -0.108, 0.108, 0.250, 0.316, 0.305, 0.218, 0.076, -0.094, -0.264, -0.378, -0.461, -0.503, -0.510, -0.472, -0.409, -0.343]
    elif l == "#":
        x = [-0.038, -0.173, -0.173, 0.052, 0.052, 0.177, 0.177, 0.243, 0.243, -0.243, -0.243, -0.246, -0.246, 0.250]
        y = [0.326, -0.347, -0.347, -0.347, -0.347, 0.323, 0.323, 0.104, 0.104, 0.108, 0.108, -0.125, -0.125, -0.132]
        z = [penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "$":
        x = [0.166, -0.007, -0.191, -0.114, 0.118, 0.184, -0.010, -0.184, -0.184, 0.0, 0.0, 0.0]
        y = [0.201, 0.312, 0.194, 0.024, -0.045, -0.198, -0.323, -0.180, -0.180, -0.45, -0.45, 0.45]
        z = [penDownHeight, penDownHeight, penDownHeight, penDownHeight, penDownHeight, penDownHeight, penDownHeight, penDownHeight, 0.0, 0.0, penDownHeight, penDownHeight]
    elif l == "/":
        x = [0.097, -0.097]
        y = [0.326, -0.347]
    elif l == ":":
        x = [0.000, 0.000, 0.003, 0.003]
        y = [0.101, 0.101, -0.305, -0.305]
        z = [penDownHeight, 0.0, 0.0, penDownHeight]
    elif l == " ":
        x = [0.0, 0.0]
        y = [0.0, 0.0]
        z = [0.0, 0.0]
    else:
        x=[0.0, 0.0]
        y=[0.0, 0.0]
    
    # code to interpolate points in the letter paths if the distance between consecutive points are too far apart
    longGapFound = True
    # repeat loop until no long gaps have been noted
    while longGapFound == True:
        longGapFound = False
        # loop through each pair on path
        for i in range(len(x)-1):
            gap = math.sqrt((x[i]-x[i+1])*(x[i]-x[i+1])+(y[i]-y[i+1])*(y[i]-y[i+1]))
            # if gap is greater than 0.1
            if gap > 0.1:
                # insert a mid-point
                x.insert(i+1, (x[i]+x[i+1])/2)
                y.insert(i+1, (y[i]+y[i+1])/2)
                if 'z' in locals():
                    z.insert(i+1, z[i+1])
                # set gap found flag
                longGapFound = True
                # break to start this loop from the start
                break
        
    # repeat the first and last entries in the vectors x and y
    x.insert(0, x[0])
    x.append(x[len(x)-1])
    y.insert(0, y[0])
    y.append(y[len(y)-1])
    
    # check if z has been defined
    if 'z' in locals():
        # z has been defined, so just extend z with zeros front and back
        z.insert(0, 0)
        z.append(0)
    else:
        # z hasn't been defined explicitly by the letter path lookup above
        # so start at zero, drop pen, finish on zero
        z=list(repeat(penDownHeight, len(x)))
        z[0]=0
        z[len(z)-1]=0
 
    return x, y, z
    # end of letterPath()
    
def moveLetterWidthRight(s):
    # direction (CCW from forwards)
    theta = - math.pi / 2

    # define movements to walk in a particular direction
    # step position 2, tripod 1 in upper mid position, tripod 2 in lower mid position
    hexyTripod1GlobalOffset(0,0,-14)
    hexyTripod2GlobalOffset(0,0,0)
    time.sleep(0.2)
    # step position 3, tripod 1 in rear position, tripod 2 in forward position
    hexyTripod1GlobalOffset(math.sin(theta)*s,-math.cos(theta)*s,0)
    hexyTripod2GlobalOffset(-math.sin(theta)*s,math.cos(theta)*s,0)
    time.sleep(0.2)
    # step position 4, tripod 1 in lower mid position, tripod 2 in upper mid position
    hexyTripod1GlobalOffset(0,0,0)
    hexyTripod2GlobalOffset(0,0,-14)
    time.sleep(0.2)
    # step position 1, tripod 1 in forward position, tripod 2 in rear position
    hexyTripod1GlobalOffset(-math.sin(theta)*s,math.cos(theta)*s,0)
    hexyTripod2GlobalOffset(math.sin(theta)*s,-math.cos(theta)*s,0)
    time.sleep(0.2)
    # step position 2, tripod 1 in upper mid position, tripod 2 in lower mid position
    hexyTripod1GlobalOffset(0,0,-14)
    hexyTripod2GlobalOffset(0,0,0)
    time.sleep(0.2)
    hexyGlobalOffset(0,0,0)

#######################################
#      start main program flow        #
#######################################
print "starting sign name"
userName = tkSimpleDialog.askstring("Write Name", "Name for Hexy to write: ")
#userName = "Hexy"

print "Name as entered: ", userName

# scale factor for letters
sf = 25

# loop through each letter of string
for c in userName:
    print "Next letter: ", c
    # call letterPath function
    letterRoute =  letterPath(c)
    # move Hexy along paths
    for i in range(len(letterRoute[0])):
        #print letterRoute[0][i],letterRoute[1][i],letterRoute[2][i]
        hexyGlobalOffset(sf*letterRoute[0][i],sf*letterRoute[1][i],letterRoute[2][i])
        time.sleep(0.1)
    # shuffle to right one letter space
    moveLetterWidthRight(sf*0.2)


