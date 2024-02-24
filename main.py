import cv2
import numpy as np
import pandas as pd
import argparse

def map_image(event, x, y, flags, param):
    '''It will calculate the rgb values of the pixel which we double click. 
    The function parameters have the event name, (x,y) coordinates of the mouse position, etc. 
    In the function, we check if the event is double-clicked then we calculate and 
    set the R,G,B values along with x,y positions of the mouse.'''
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r, g, b, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        
def getColourName(R, G, B):
    '''The function will return the colour name from RGB values. 
       To get the color name, we calculate a distance(d) which tells us how 
       close we are to color and choose the one having minimum distance.

        Our distance is calculated by this formula:

        d = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor)'''
    min_dist = 10000
    for i in range(len(img_csv)):
        dist = abs(R - img_csv.loc[i, 'R']) + abs(G - img_csv.loc[i, 'G']) + abs(B - img_csv.loc[i, 'B'])
        if (dist < min_dist):
            min_dist = dist
            color_name = img_csv.loc[i, 'Colour Name']
    return color_name

#Create an ArgumentParser object
parser = argparse.ArgumentParser()

#`add_argument()`` method is used to specify which command-line options the program is willing to accept.
# '-i' or '--image' are the command-line options for specifying the path to the image file.
#`required=True`` indicates that the --image option is mandatory, meaning the user must provide it.
# `help="Image Path"` provides a description of what the argument is for.
parser.add_argument('-i', '--image', required=True, help="Image Path")

#Convert parsed information to dictionary for easier access
arguments = vars(parser.parse_args()) 

#Extracting Image Path
image_path = arguments['image']

#Reading image with opencv
img = cv2.imread(image_path)

clicked = False
r = g = b = xpos = ypos = 0

#Reading the '.csv' file containing the4 details of all colors
img_csv = pd.read_csv('colors.csv', names=["Colour", "Colour Name", "Hex", "R", "G", "B"], header=None)

#First, we created a window in which the input image will display. 
cv2.namedWindow('Image')

#Then, we set a callback function which will be called when a mouse event happens.
cv2.setMouseCallback('Image', map_image)
    
while(1):
    cv2.imshow("Image", img)
    if (clicked):
        
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        
        #Creating text string to display 'Colour name' and its RGB values
        op = getColourName(r, g, b) + ', R =' + str(r) + ', G = ' + str(g) + ', B = ' + str(b)
        
        #cv2.putText(img, text, start, font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, op, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        
        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, op, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
            
        clicked = False
    
    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27: 
        break
    
cv2.destroyAllWindows()