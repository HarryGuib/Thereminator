import numpy as np
import webbrowser
import rtmidi
import mido
import cv2
from numpy.lib.function_base import median

#cap = cv2.VideoCapture('Micro-dance_2_.avi')
cap = cv2.VideoCapture(0)

#webbrowser.open("C:\\Users\\Miles\\Documents\\AVPRG_W20\\Thereminator\\DataTransferTest\\PlayGround\\index.html")
print("MIDI output ports: ", mido.get_output_names())
midiList = mido.get_output_names()
for midi in midiList:
    if("MIDI 1" in midi ):
        midiOutput = mido.open_output(midi)

def do_nothing():
    return

cv2.namedWindow('HSV')
cv2.createTrackbar('Hue','HSV',44,179, do_nothing)
cv2.createTrackbar('Saturation','HSV',51,255, do_nothing)
cv2.createTrackbar('Value','HSV',37,255, do_nothing)

def sendControlchange(control, value):
	message = mido.Message('control_change', control=control, value=value)
	midiOutput.send(message)

def sendNoteOn(note, velocity):
	message = mido.Message('note_on', note=note, velocity=velocity)
	midiOutput.send(message)

def sendNoteOff(note, velocity):
	message = mido.Message('note_off', note=note, velocity=velocity)
	midiOutput.send(message)

# typicalRed =  np.array([175,160, 102])
typicalRed =  np.array([55,181, 255])

while(cap.isOpened()):

    ret, frame = cap.read()
    frame = cv2.flip(frame, +1)


    #HSV (nicht die Fußballmanschaft)
    #Hab die farben dadurch bekommen das ich die hsv werte abgelesen hab (GM2) und eine toleranz von +-10 gesetzt habe
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hue = cv2.getTrackbarPos('Hue','HSV')
    sat = cv2.getTrackbarPos('Saturation','HSV')
    val = cv2.getTrackbarPos('Value','HSV')

    schwellenWert = np.array([hue,sat,val])

#=============== Farbe auswählen für Marker ===================

    def click(event, x, y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            (b, g, r) = frame[y, x]
            print("Pixel Position ({}, {}) - Rot: {}, Grün: {}, Blau: {}".format(x,y,r,g,b))
            frame[0:10, 0:10] = [b,g,r]
            lupe[0:200, 0:200] = [b,g,r]
            cv2.imshow("Lupe", lupe)
            global typicalRed
            typicalRed =  np.array([b,g,r])

    lupe = np.zeros(shape=(200, 200, 3), dtype=np.uint8)
    cv2.setMouseCallback("FRAME", click)
    #print("typicalRed "+str(typicalRed))
#==============================================================

    redd = cv2.inRange(hsvFrame,typicalRed-schwellenWert,typicalRed+schwellenWert)
    kSize = 5
    medianFrame = cv2.medianBlur(redd,kSize)

    #Center
    contours,hierarchy = cv2.findContours(medianFrame, 1, 2)
    if (len(contours)>0):
        #soll alle contours durchgehen (alle figuren die auftauchen)
        for cnt in contours:
            cnt = contours[0]
            M = cv2.moments(cnt)
            if (M['m00']>0):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame,(cx,cy),2,(255,255,0),-1)
                valueX = (cx / 640) * 128
                valueY = (cy / 480) * 128
                sendNoteOn(int(valueX), int(valueY))

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

cap.release()
cv2.destroyAllWindows()