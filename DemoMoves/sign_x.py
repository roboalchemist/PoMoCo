import time
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


x = [-9.0, 9.0, 9.0, -9.0, -9.0, 9.0, 9.0, -11.7, -11.7, -9.0, 9.0, 11.7]
y = [-13.0, 13.0, 13.0, 13.0, 13.0, -13.0, -13.0, -4.5, -4.5, 0.0, 0.0, -4.5]
z = [-7.0, -7.0, 0.0, 0.0, -7.0, -7.0, 0.0, 0.0, -7.0, -7.0, -7.0, -7.0]


# code to interpolate points in the letter paths if the distance between consecutive points are too far apart
longGapFound = True
# repeat loop until no long gaps have been noted
while longGapFound == True:
    longGapFound = False
    # loop through each pair on path
    for i in range(len(x)-1):
        gap = math.sqrt((x[i]-x[i+1])*(x[i]-x[i+1])+(y[i]-y[i+1])*(y[i]-y[i+1]))
        # if gap is greater than 0.1
        if gap > 2:
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

sf=1
for i in range(len(x)):
    #print letterRoute[0][i],letterRoute[1][i],letterRoute[2][i]
    hexyGlobalOffset(sf*x[i],sf*y[i],z[i])
    time.sleep(0.1)

