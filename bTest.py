import pyautogui as pg
import pytesseract as pt
import time
# Variable #
sceneScreenshotCornerX  = 3070           #screeenshot bounds - bottom row   ***screen co-ords
sceneScreenshotCornerY  = 1169           #screeenshot bounds - bottom row   ***screen co-ords
sceneScreenshotWidth    = 1215           #screeenshot bounds - bottom row
sceneScreenshotHeight   = 60             #screeenshot bounds - bottom row
answerScreenshotCornerX = 4103           #screenshot bounds - answer box only   ***screen co-ords
answerScreenshotCornerY = 1151           #screenshot bounds - answer box only   ***screen co-ords
answerScreenshotWidth   = 174            #screenshot bounds - answer box only
answerScreenshotHeight  = 93             #screenshot bounds - answer box only
leftBorderToBox         = 8              #Pixels to first bit box border
boxToBox                = 122            #Pixels between bit boxes
boxEnd                  = 900            #last box, safe distance from first to ensure each is checked once
colorCheckX             = 17             #Co-ordinates for a spot inside the border (top left but anywhere away from middle number is fine)
colorCheckY             = 1              #Co-ordinates for a spot inside the border (top left but anywhere away from middle number is fine)
answerBoxX              = 4184           #pixel co-ordinates for clicking the answer box for 'green' questions. ***screen co-ords
boxY                    = 1208           #pixel co-ordinates for clicking the answer box for 'green' questions. ***screen co-ords
# -------------------------- #
pt.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe" 

def binaryToDecimal(n):
    return str(int(n,2))                #input binary string, convert to int for decimal conversion, return decimal string since pg.write expects string to iterate through.

def decimalToBinary(n, legnth = 8):
    return format(n,'08b')              #input decimal, return 8 bit binary, retaining leading 0's

def main():
    while True:
        screenshot = pg.screenshot(region=(sceneScreenshotCornerX,sceneScreenshotCornerY,sceneScreenshotWidth,sceneScreenshotHeight))       #screenshot the bottom row
        #screenshot.save("screenshot1.png")  #debugging                                 
        if (screenshot.getpixel((leftBorderToBox,colorCheckY))[0] == 110):              #check if border pixel is green (110), only first rgb value needed since theres only 2 possible colors
            binaryNum = ""                                                              #initialise variable
            for x in range(colorCheckX,boxEnd,boxToBox):                                #check each bit box
                for y in range(1,2):                                                    #technically redundant, placeholder for checking more than just bottom row
                    if (screenshot.getpixel((x,y))[0] == 110):                          #----------------------------------------------------------#
                        binaryNum = binaryNum + "1"                                     #if 'background' is green (110), append '1' to string
                    else:                                                               #else append '0'
                        binaryNum = binaryNum + "0"                                     #---------------------------------------------------------#
            binaryNum = binaryToDecimal(binaryNum)                                      #convert binary num to decimal, returns an int
            pg.click(answerBoxX,boxY)                                                   #click answer box
            pg.write(binaryNum)                                                         #iterate through binaryNum typing each value on the keyboard
            pg.press("enter")                                                           #press enter
        else:
            answerScreenshot = pg.screenshot(region=(answerScreenshotCornerX,answerScreenshotCornerY,answerScreenshotWidth,answerScreenshotHeight))     #screenshot the answer box
            #answerScreenshot.save("ansScreenhot1.png")  #debugging
            decimalNum = pt.image_to_string(answerScreenshot,config='--psm 10')         #uses OSR to convert answerbox screenshot PIL object to a string, config to help recognise single digits
            #print(decimalNum)                                                          #---------------------------------------------------debugging
            decimalNum = int(decimalNum)                                                #convert to int for decimalToBinary function
            #print(decimalNum)                                                          #---------------------------------------------------debugging
            decimalNum = decimalToBinary(decimalNum)                                    #call function to convert answerbox number to 8 bit binary, retaining leading zero's
            #print(decimalNum)                                                          #---------------------------------------------------debugging
            i = 0                                                                       #initialize count
            for x in range(colorCheckX,boxEnd,boxToBox):                                #check each bit box
                for y in range(1,2):                                                    #redundant, placeholder for checking more rows.
                    if (decimalNum[i] == '1'):                                          #check if box should be 1
                        if (screenshot.getpixel((x,y))[0] == 0):                        #if it is, check if box needs clicking. we check for blue background since that indicates 0 and needs to be clicked
                            pg.click((sceneScreenshotCornerX+x+10),boxY)                #click co-ords of the [i]'th box
                             #print('test1')                                            #debugging
                        #else:                                                          #debugging            no need for an else here since if box is already 1 we do nothing
                             #print('test2')                                            #debugging
                    else:                                                               #box is 0 automatically if not 1
                        if(screenshot.getpixel((x,y))[0] == 251):                       #check if background is orange (251). first rgb value, different enough from other colors.
                            pg.click((sceneScreenshotCornerX+x+10),boxY)                #click co-ords of the [i]'th box since orange means box shows 1 and needs to be 0
                            #print('test3')                                             #debugging
                        #else:                                                          #debugging              no need for else, if box is already 0 we do nothing
                            #print('test4')                                             #debugging
                i += 1                                                                  #increment count by 1 each loop, thereby checking 1st digit for box 1, 2nd digit for box 2 etc
        pg.click(3783,860)      #'hack' to constantly click spawn location of next level popup
        time.sleep(2)           #delay to allow for animation transintion/board clear transition 

### START ###
if __name__ == '__main__':
    main()