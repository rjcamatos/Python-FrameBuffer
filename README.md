# Python Virtual Frame Buffer

A Python Virtual Frame Buffer with ability to save as Bitmap`s.



# *** FrameBuffer v0.2 API ***

# -- Construct the main object, bits can be 8, 16, 24 or 32

FrameBuffer(columns,rows,bits=32)

# -- Set the the window area to be draw (Mandatory, at least once)

setWindow(startX,endX,startY,endY,copy=True)

# -- Set the current color, if "isFillColor=True" sets the fill color

setColor(R,G,B,isFillColor=False):

# -- Restore to last previous color, if "isFillColor=True" restore the fill color

restoreColor(isFillColor=False):

# -- Set current border thikness

setThikness(thikness):

# -- Restore to last previous border thikness

restoreThikness():

# -- Set rotation to given degress, with the given x and y as origin (x and y should be the center of the image to rotate) call with empty args to set normal painting

setRotation(degress=0,xOrigin=0,yOrigin=0):

# -- Set a pixel with the current color

setPixel(xPos,yPos):

# -- Draw a line

drawLine(startX,endX,startY,endY):

# -- Draw a horizontal line

drawLineH(xPos,yPos,size):

# -- Draw a vertical line

drawLineV(xPos,yPos,size):

# -- Draw a rectangle, if "fill=True", fill with the fill color

drawRectangle(xPos,yPos,width,height,fill=False):

# -- Draw a square, if "fill=True", fill with the fill color

drawSquare(xPos,yPos,size,fill=False):

# -- Draw a circle, if "fill=True", fill with the fill color

drawCircle(xPos,yPos,radius,fill=False):

# -- Load image at given position from raw bytes (need to be same bit depth)

loadRaw(xPos,yPos,width,height,bytes)

# -- Load image at given position (need to be same bit depth)

loadImage(xPos,yPos,file)

# -- Load a font to print charecters as it is (need to be same bit depth)

loadFont(file):

# -- Print a given charecter

printChar(xPos,yPos,char):

# -- Print a given string 

printChars(xPos,yPos,chars):

# -- Write the contents to main buffer

flush():

# -- Save the main buffer as a bitmap ( before use this call flush() )

saveBitmap(file):
