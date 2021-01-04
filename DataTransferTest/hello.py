import numpy as np
import cv2
import eel
from numpy.lib.function_base import median

firstCheck = True

#cap = cv2.VideoCapture('Micro-dance_2_.avi')
cap = cv2.VideoCapture(0)

eel.init('web')
# @eel.expose
# def fromPyToJS(x):
#     print('Hello from %s' % x)


def do_nothing():
    return

cv2.namedWindow('HSV')
cv2.createTrackbar('Hue','HSV',44,179, do_nothing)
cv2.createTrackbar('Saturation','HSV',51,255, do_nothing)
cv2.createTrackbar('Value','HSV',37,255, do_nothing)



while(cap.isOpened()):

    ret, frame = cap.read()

    #HSV (nicht die Fußballmanschaft)
    #Hab die farben dadurch bekommen das ich die hsv werte abgelesen hab (GM2) und eine toleranz von +-10 gesetzt habe
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #h, s, v = cv2.split(hsvFrame)

    hue = cv2.getTrackbarPos('Hue','HSV')
    sat = cv2.getTrackbarPos('Saturation','HSV')
    val = cv2.getTrackbarPos('Value','HSV')

    schwellenWert = np.array([hue,sat,val])

    #DANCE VIDEO (rote farbe vom Handschuh)
    typicalRed =  np.array([175,160, 102])

    #Color wonach gesucht wird in der Kamera
    #typicalRed = np.array([179*(350/360),255*0.88, 255*0.62])

    
    redd = cv2.inRange(hsvFrame,typicalRed-schwellenWert,typicalRed+schwellenWert)

    kSize = 5
    medianFrame = cv2.medianBlur(redd,kSize)


    #Center
    contours,hierarchy = cv2.findContours(medianFrame, 1, 2)
    if (len(contours)>0):
        #soll alle contours durchgehen (alle figuren die auftauchen)
        for cnt in contours:
            #cnt = contours[0]
            M = cv2.moments(cnt)
            if (M['m00']>0):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame,(cx,cy),2,(255,255,0),-1)

                #Box mit Winkel
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame,[box],0,(0,0,255),1)

                #Box ohne Winkel
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)                       


    #normale frame darstellen
    cv2.imshow("FRAME",frame)

    #Mask frame darstellen
    cv2.imshow("MASK",medianFrame)
    if cv2.waitKey(25)!=-1:
        break

eel.fromJsToPY('Python World')
eel.start("index.html")
cap.release()
cv2.destroyAllWindows()


