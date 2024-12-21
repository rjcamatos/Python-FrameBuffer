import struct
import random
import math
from io import BytesIO
from memory_profiler import profile #ADD @profile BEFORE FUNCTION NAME TO ANALYSE IT

class IOMem:

    def __init__(self):
        self._buffer = BytesIO()
        self._seekYES = 0
        self._seekNO = 0
        self._ignoreColor = None

    def getbuffer(self):
        return self._buffer.getbuffer()
    
    def read(self,len):
        return self._buffer.read(len)
    
    def setIgnoreColor(self,color = None):
        self._ignoreColor = color

    def write(self,bytes):
        self._buffer.write(bytes)

    def writeWindow(self,bytes,columnStart,columnEnd,rowStart,RowEnd):
        startX = columnStart
        endX = columnEnd
        n = 0
        pass
    
    def seek(self,pos):
        ## NOTE TO TRY ON ST7533 DISABLE DATA INPUT WITH PROPOSED PIN ... N writes to access to REQUERIED MEMORY -> TALVEZ FUNCIONE :P
        if pos == self._buffer.tell():
            self._seekNO += 1
            return
        self._seekYES += 1
        self._buffer.seek(pos)

class FrameBuffer:

    def __init__(self,width,height,bits=32,io=IOMem):
        
        self._io = io()
        
        self._height = height
        self._width = width
        self._bits = bits
        
        self._color = b'\x00'
        self._tmpColor = b'\x00'
        
        self._thikness = 4
        self._tmpThikness = 0

        self._charTable = None
        self._charTableMatrix = None
        self._charTableWidth = 0
        self._charTableHeight = 0
        self._charTableCharWidth = 0
        self._charTableCharHeight = 0


        #INITIALIZE A RANDOM BUFFER OF DATA
        n = 0
        while n < (self._height*self._width*(int(self._bits/8))):
            self._io.write(random.randbytes(int(self._bits/8)))
            n += int(self._bits/8)
        
    def getBuffer(self):
        return self._io.getbuffer()
   
    def getOffset(self,startX,startY):
        return (self._height-startY) * (self._width*int(self._bits/8)) - ( (self._width-startX)*int(self._bits/8) )


    def setRGBColor(self,R,G,B):
        
        if self._bits == 8: #NEED FIX
            self._color = int(((R & 0xF8) << 8) | ((G & 0xFC) << 8) | (B >> 3)).to_bytes(2,'little')

        if self._bits == 16: #OK
            self._color = int(((R&0xF8)<<8) | ((G&0xFC)<<3) | (B>>3)).to_bytes(2,'little')
            
        if self._bits == 24: #OK
            self._color = int( R<<16 | G<<8 | B ).to_bytes(3,'little')

        if self._bits == 32: #OK
            self._color = int( (R<<20|G<<10|B)&0xFFFFFFF3 ).to_bytes(4,'little')

        #print("BITS %i" % self._bits)
        #print(self._color)          

    def restoreRGBColor(self):
        self._color = self._tmpColor

    def setThikness(self,thikness):
        self._tmpThikness = thikness
        self._thikness = thikness

    def restoreThikness(self):
        self._thikness = self._tmpThikness
        

    def drawPixel(self,x,y):
        self._io.seek(self.getOffset(x,y))
        self._io.write(self._color)
        thikness = math.ceil(self._thikness/2) 

        row = 0
        while row < thikness:
            column = 0
            while column < thikness:
                self._io.seek(self.getOffset(x+column,y+row))
                self._io.write(self._color)
                self._io.seek(self.getOffset(x-column,y+row))
                self._io.write(self._color)
                self._io.seek(self.getOffset(x+column,y-row))
                self._io.write(self._color)
                self._io.seek(self.getOffset(x-column,y-row))
                self._io.write(self._color)
                column += 1
            row += 1

    def drawLine(self,startX,startY,endX,endY):        
        width = (endX-startX)
        height = (endY-startY)

        inc = 0
        len = 0
        lenW = 0
        lenH = 0
        if width < height:
            inc = width/height
            len = lenW = height            

        if height < width or height == width:
            inc = height/width
            len = lenH = width

        pos = 0
        incPos = 0
        while pos < len:
            incPos += inc
            if len == lenW:
                self.drawPixel(startX+math.ceil(incPos),startY+pos)
            if len == lenH:
                self.drawPixel(startX+pos,startY+math.ceil(incPos))
            pos +=1


    def drawLineH(self,xPos,yPos,size):
        n = 0
        while n < size:
            self.drawPixel(xPos+n,yPos)
            n += 1

    def drawLineV(self,xPos,yPos,size):
        n = 0
        while n < size:
            self.drawPixel(xPos,yPos+n)
            n += 1

    def drawRectangle(self,xPos,yPos,width,height, fill=False):
        self.drawLineH(xPos,yPos,width)
        self.drawLineH(xPos,yPos+height,width)
        self.drawLineV(xPos,yPos,height)
        self.drawLineV(xPos+width,yPos,height)
        if fill == True:
            self.setThikness(0)
            row = 0
            while row < height:
                self.drawLineH(xPos,yPos+row,width)
                row += 1
            self.restoreThikness()

    def drawSquare(self,xPos,yPos,size,fill=False):
        self.drawLineH(xPos,yPos,size)
        self.drawLineH(xPos,yPos+size,size)
        self.drawLineV(xPos,yPos,size)
        self.drawLineV(xPos+size,yPos,size)
        if fill == True:
            self.setThikness(0)
            row = 0
            while row < size:
                self.drawLineH(xPos,yPos+row,size)
                row += 1
            self.restoreThikness()

    def drawCircle(self,xPos,yPos,radius,fill=False):
        angle = 0
        while angle <= 360:
            x = math.ceil(radius * math.cos(angle))
            y = math.ceil(radius * math.sin(angle))
            self.drawPixel(xPos+x,yPos+y)
            if fill == True:
                self.setThikness(0)
                n = 0
                while n < radius:
                    x = math.ceil(n * math.cos(angle))
                    y = math.ceil(n * math.sin(angle))
                    self.drawPixel(xPos+x,yPos+y)
                    n += 1
                self.restoreThikness()
            angle += 0.2
        
        
    def flipHorizontal(self):
        row = self._height
        while row > 0:        
            ePos = row * self._width * 2    
            sPos = (row-1) * self._width * 2
            new = BytesIO()
            while ePos > sPos:
                ePos -= 2
                self._io.seek(ePos)
                new.write(self._io.read(2))
                
            self._io.seek(sPos)
            self._io.write(new.getbuffer())
            row -= 1

    def flipVertical(self):
        pos = self._width * self._height * 2
        buffer = BytesIO()
        while pos > 0 :
            pos -= 2
            self._io.seek(pos)
            buffer.write(self._io.read(2))
        self._io = buffer

    def saveBitmap(self,file):
        out_file = open(file,'wb')
        # --- THE BITMAP HEADER ---
        #--BMP HEADER
        bmp_header = struct.pack('<2s I 2s 2s I',
            b'BM',       #BmDescription
            54 + 16,      #FileSize #THE SISZE OF THE HEADER
            b'\x00\x00',  #ApplicationSpecific_1
            b'\x00\x00',  #ApplicationSpecific_2
            14+40        #PixelArrayOffset
        )
        #--DIB HEADER
        dib_header = struct.pack('<I I I H H I I I I I I',
            40,                     #DibHeaderBytes
            self._width,          #ImageWidth
            self._height,             #ImageHeight
            1,                      #ColorPlanes
            self._bits,             #BitsPerPixel
            0,                      #BiRGB
            self._width*self._height*int(self._bits/8),  #RawBitmapSize
            self._width,          #PrintResolutionH
            self._height,             #PrintResolutionV
            0,                      #NumberOfColorsInPallet
            0                       #ImportantColors
        )
        #WRITE TO FILE
        out_file.write(bmp_header)
        out_file.write(dib_header)
        out_file.write(data.getBuffer())

        #print("NO SEEK %i YES SEEK %i" % (self._io._seekNO, self._io._seekYES))

        #END
        out_file.close

    def to_little_endian(bytearr):
        fmt = f'<{len(bytearr)}B'
        return struct.pack(fmt, *bytearr)
    
    
        self._charTable = self.loadFromFile(file)

    def loadFont(self,file,debug=True):
        input_file = open(file,'rb')
        
        self._charTableMatrix = file[file.rfind('-')+1:file.rfind('.bmp')].split('X')
        self._charTableMatrix[0] = int(self._charTableMatrix[0])
        self._charTableMatrix[1] = int(self._charTableMatrix[1])

        self._charTable = FrameBuffer(300,75,self._bits)

        input_file.seek(14) #jump to dib header
        dib_header = struct.unpack_from('<I I I H H I I I I I I',input_file.read(40))
        self._charTableWidth = dib_header[1]
        self._charTableHeight = dib_header[2]
        self._charTableCharWidth = int(self._charTableWidth / self._charTableMatrix[0])
        self._charTableCharHeight = int(self._charTableHeight / self._charTableMatrix[1])

        self._charTable._io.seek(0)
        self._charTable._io.write(input_file.read())


    def printChar(self,xPos,yPos,char):
        charIndexs = b' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        charIndex = charIndexs.find(char)
        
        atRow = math.floor(charIndex / self._charTableMatrix[0])
        atColumn = charIndex - self._charTableMatrix[0]*atRow
        
        self._charTable._io.seek(0)
        y = 0
        while y < 15:
            self._io.seek(self.getOffset(xPos,yPos+y))
            self._charTable._io.seek(self._charTable.getOffset(atColumn*self._charTableCharWidth,y+(atRow*self._charTableCharHeight)))
            self._io.write(self._charTable._io.read(self._charTableCharWidth*int(self._charTable._bits/8)))
            y += 1

    def printChars(self,xPos,yPos,chars):
        for char in chars:
            self.printChar(xPos,yPos,char)
            xPos += self._charTableCharWidth



##DOWN HERE WRITE THE IMAGE FILE


import time
start_time = time.time()


#THE FRAME BUFFER
data = FrameBuffer(800,600,24)

data.setRGBColor(255,0,0)
data.drawSquare(25,25,300,True)
data.restoreRGBColor()
data.setRGBColor(0,0,255)
data.drawLineH(10,100,500)
data.restoreRGBColor()
data.setRGBColor(0,255,0)
data.drawLineV(50,60,500)
data.restoreRGBColor()
data.setThikness(6)

data.setRGBColor(255,255,255)
data.drawSquare(100,300,150,True)

data.setRGBColor(255,0,0)
data.setThikness(6)
data.drawRectangle(400,300,250,100,False)
data.restoreThikness()

data.restoreThikness()
data.setRGBColor(0,0,255)
data.setThikness(6)
data.drawLine(10,10,100,200)
data.drawLine(10,10,200,300)
data.restoreThikness()
data.setRGBColor(0,255,0)
data.drawPixel(10,10)
data.drawCircle(100,100,50)
data.drawCircle(160,200,50,False)
#data.flipHorizontal()
#data.flipVertical()

data.loadFont('./FrameBuffer-v0.1/font2bitmap24bits-20X5.bmp')
data.printChars(100,100,b'HEllo World')
data.printChars(100,115,b'I`m Ricardo Matos')

data.saveBitmap('image800X600.bmp')

#THE FRAME BUFFER
data = FrameBuffer(128,160,16) #FOR MY TFT SCREEN 160x128

data.setRGBColor(0,255,0)
data.drawSquare(25,25,50,True)
data.restoreRGBColor()
data.setRGBColor(0,0,255)
data.drawLineH(10,10,50)
data.restoreRGBColor()
data.setRGBColor(0,255,0)
data.drawLineV(5,6,50)
data.setThikness(4)
data.drawRectangle(40,30,25,10,False)
data.restoreThikness()
data.setRGBColor(0,0,255)
data.setThikness(4)
data.drawLine(10,10,10,20)
data.drawLine(10,10,20,30)
data.restoreThikness()
data.setRGBColor(255,0,0)
data.drawPixel(10,10)
data.drawCircle(10,10,10)
data.drawCircle(16,20,10,False)
#data.flipHorizontal()
#data.flipVertical()
data.loadFont('./FrameBuffer-v0.1/font2bitmap16bits-20X5.bmp',False)

data.saveBitmap('image128X160.bmp')


end_time = time.time()

print("TIME ", (end_time-start_time))


