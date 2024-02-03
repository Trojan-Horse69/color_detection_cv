# Using the argparse library to create an argument parser.
# An image path is directly given from the command prompt

import argparse
import cv2
import pandas as pd

ap = argparse.ArgumentParser() #ArgumentParser is a tool in Python that makes it easy to write user-friendly command-line interfaces.

"""This line adds a command-line argument to the ArgumentParser. It specifies that the script expects an argument with either a short form -i or a long form --image. 
The required=True indicates that this argument must be provided by the user when running the script. 
The help parameter provides a description of what the argument is for."""
ap.add_argument('-i', '--image', required=True, help="Image Path")


"""This line parses the command-line arguments provided by the user when running the script. 
parse_args() returns an object containing the values of the command-line arguments. 
vars() converts this object into a dictionary, and the resulting dictionary is stored in the variable args."""
args = vars(ap.parse_args())

img_path = args['image']
img = cv2.imread(img_path)

#declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("C:/Users/j/OpenCV/data/colors.csv", names=index, header=None)


#d = abs(Red - ithRedColor) + (Green - ithGreenColor) + (Blue - ithBlueColor)

def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d<=minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

"""function to get x,y coordinates of mouse double click
The draw function calculates the rgb values of the pixel which we double click. 
The function parameters have the event name, (x,y) cordinates of the mouse position, etc. 
In the function, we check if the event is double clicked then we calculate and set the r,g,b values along with x,y positions of the mouse"""

def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Set a Mouse callback event on a window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


while(1):
    cv2.imshow("image", img)
    if (clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills the rectnagle entirely
        cv2.rectangle(img, (20,20), (750,60), (b,g,r), -1)

        #creating text string to display (Color name and RGB values)
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)

        #cv2.putText(img, text, start, font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, text, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        #For very light colors it will display text in black color
        if (r+g+b>=600):
            cv2.putText(img, text, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

        clicked=False

    #Loops break when user hits esc key
    if cv2.waitKey(20) & 0xFF == 27:
            break

cv2.destroyAllWindows()
